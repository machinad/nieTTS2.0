import os
import sys
import asyncio
import argparse
import logging

# PyInstaller 打包后 CWD 不是应用目录，导致相对路径（如 models/...）失效
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# PyInstaller GUI 模式下 stdout/stderr 为 None，tqdm 等库会崩溃
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')

from PySide6.QtWidgets import QApplication
import qasync
from config.default import ConfigManager
from config.notifier import ConfigNotifier
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.stt.service import STTService
from engines.pipeline import RequestPipeline
from web_server import WebServer, WSLogHandler
from certificates.certificates_server import CertificateServer
from version import VERSION
from gui.main import MainWindow
from gui.log_handler import QtLogHandler
from gui.bridge import GuiBridge
from gui.theme import apply_theme

BANNER = r"""
███╗   ██╗  ██╗  ███████╗  ████████╗  ████████╗  ███████╗
████╗  ██║  ██║  ██╔════╝  ╚══██╔══╝  ╚══██╔══╝  ██╔════╝
██╔██╗ ██║  ██║  █████╗       ██║        ██║     ███████╗
██║╚██╗██║  ██║  ██╔══╝       ██║        ██║     ╚════██║
██║ ╚████║  ██║  ███████╗     ██║        ██║     ███████║
╚═╝  ╚═══╝  ╚═╝  ╚══════╝     ╚═╝        ╚═╝     ╚══════╝
""" 

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="nieTTS 2.0")
    parser.add_argument("--debug", action="store_true", help="启用 debug 日志模式")
    args, _ = parser.parse_known_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    qt_log_handler = QtLogHandler()
    logging.getLogger().addHandler(qt_log_handler)

    ws_log_handler = WSLogHandler()

    app = QApplication(sys.argv)
    app.setApplicationName("nieTTS 2.0")
    app.setApplicationVersion(VERSION)

    apply_theme(app)

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    logger.info(BANNER)
    logger.info("nieTTS %s (GUI 模式) 启动中...", VERSION)

    config = ConfigManager()

    save_dir = config.save_path
    try:
        for f in save_dir.iterdir():
            if f.is_file():
                f.unlink(missing_ok=True)
    except Exception:
        pass

    tts = TTSService(config)
    translate = TranslateService(config)
    osc = OSCService(config)
    stt = STTService(config)
    pipeline = RequestPipeline(config, tts, translate, osc, stt=stt)

    notifier = ConfigNotifier()
    bridge = GuiBridge(config, tts, translate, osc, pipeline, notifier=notifier)

    window = MainWindow(bridge, qt_log_handler)
    window.show()

    # VR 覆盖层
    vr_manager = None

    async def _startup():
        nonlocal vr_manager
        ws_log_handler.set_loop(asyncio.get_running_loop())
        logging.getLogger().addHandler(ws_log_handler)
        await pipeline.start()
        logger.info("Pipeline 已启动")

        # VR 覆盖层（OpenVR + 感应式射线）
        vr_cfg = config.get("vr_overlay", {})
        if vr_cfg.get("enabled", False):
            from gui.vr_overlay import VROverlayManager, VROverlayTestWidget
            vr_manager = VROverlayManager()
            vr_widget = VROverlayTestWidget(manager=vr_manager)
            asyncio.create_task(vr_manager.run(vr_widget, config.config))
            logger.info("VR 覆盖层任务已创建")

        cert_server = CertificateServer()
        host = config.get("host", "0.0.0.0")
        port = int(config.get("port", 11451))
        cert_path = str(cert_server.cert_file_path)
        key_path = str(cert_server.key_path)
        logger.info("Web 服务启动在 https://%s:%s", host, port)
        logger.info("局域网地址: https://%s:%s", cert_server.ip_address, port)

        bridge.ip_address = cert_server.ip_address
        bridge.web_port = port

        window._header.update_web_url()

        web = WebServer(config, tts, translate, osc, pipeline, notifier=notifier)
        web.set_loop(asyncio.get_running_loop())

        shutdown_event = asyncio.Event()

        async def _web_shutdown_trigger():
            await shutdown_event.wait()

        asyncio.create_task(
            web.app.run_task(
                host=host,
                port=port,
                certfile=cert_path,
                keyfile=key_path,
                shutdown_trigger=_web_shutdown_trigger,
            )
        )

    async def _shutdown():
        nonlocal vr_manager
        qt_log_handler.disable()
        await pipeline.stop()
        await translate.close()
        # 清理 VR 覆盖层
        if vr_manager is not None:
            await vr_manager.stop()
            vr_manager = None
            logger.info("VR 覆盖层已关闭")
        logger.info("nieTTS 已停止")

    try:
        with loop:
            loop.call_soon(lambda: asyncio.create_task(_startup()))
            loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            loop.run_until_complete(_shutdown())
        except Exception:
            pass
        loop.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
