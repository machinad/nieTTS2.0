import sys
import asyncio
import logging

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
"""  # noqa: W291

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
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

    async def _startup():
        ws_log_handler.set_loop(asyncio.get_running_loop())
        logging.getLogger().addHandler(ws_log_handler)
        await pipeline.start()
        logger.info("Pipeline 已启动")

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
        qt_log_handler.disable()
        await pipeline.stop()
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
