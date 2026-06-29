"""
⚠️ 此入口已废弃，不再维护。

main.py 为 nieTTS 的无 GUI（Headless）启动入口，仅作为历史参考保留。
当前唯一维护的启动入口是 gui_main.py（Qt6 桌面 GUI 模式）。
Web 前端由 gui_main.py 中内嵌的 Quart 服务器统一提供。

请勿基于此文件进行修改或提交 PR。如有需要，请使用 gui_main.py。
"""

import asyncio
import argparse
import logging

from config.default import ConfigManager
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.stt.service import STTService
from engines.pipeline import RequestPipeline
from web_server import WebServer, WSLogHandler
from certificates.certificates_server import CertificateServer

from version import VERSION

_parser = argparse.ArgumentParser(description="nieTTS 2.0")
_parser.add_argument("--debug", action="store_true", help="启用 debug 日志模式")
_args, _ = _parser.parse_known_args()

logging.basicConfig(
    level=logging.DEBUG if _args.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

_ws_log_handler = WSLogHandler()
logging.getLogger().addHandler(_ws_log_handler)

BANNER = r"""
███╗   ██╗  ██╗  ███████╗  ████████╗  ████████╗  ███████╗
████╗  ██║  ██║  ██╔════╝  ╚══██╔══╝  ╚══██╔══╝  ██╔════╝
██╔██╗ ██║  ██║  █████╗       ██║        ██║     ███████╗
██║╚██╗██║  ██║  ██╔══╝       ██║        ██║     ╚════██║
██║ ╚████║  ██║  ███████╗     ██║        ██║     ███████║
╚═╝  ╚═══╝  ╚═╝  ╚══════╝     ╚═╝        ╚═╝     ╚══════╝
"""  # noqa: W291


class nieTTS:

    def __init__(self):
        self.config = ConfigManager()
        self.tts = TTSService(self.config)
        self.translate = TranslateService(self.config)
        self.osc = OSCService(self.config)
        self.stt = STTService(self.config)
        self.pipeline = RequestPipeline(self.config, self.tts, self.translate, self.osc, stt=self.stt)
        self.web = WebServer(self.config, self.tts, self.translate, self.osc, self.pipeline)
        self.cert = CertificateServer()

        self._host = self.config.get("host", "0.0.0.0")
        self._port = int(self.config.get("port", 11451))

    async def start(self):
        _ws_log_handler.set_loop(asyncio.get_running_loop())
        self.web.set_loop(asyncio.get_running_loop())
        self._cleanup_orphan_files()
        logger.info("正在启动 Pipeline ...")
        await self.pipeline.start()

        cert_path = str(self.cert.cert_file_path)
        key_path = str(self.cert.key_path)

        logger.info(f"nieTTS {VERSION} 运行在 https://{self._host}:{self._port}")
        logger.info(f"局域网地址: https://{self.cert.ip_address}:{self._port}")

        self._shutdown_event = asyncio.Event()
        await self.web.app.run_task(
            host=self._host,
            port=self._port,
            certfile=cert_path,
            keyfile=key_path,
            shutdown_trigger=self._shutdown_trigger,
        )

    async def _shutdown_trigger(self):
        await self._shutdown_event.wait()

    def _cleanup_orphan_files(self):
        save_dir = self.config.save_path
        try:
            for f in save_dir.iterdir():
                if f.is_file():
                    f.unlink(missing_ok=True)
        except Exception as e:
            logger.debug(f"清理孤儿文件失败: {e}")

    async def stop(self):
        self._shutdown_event.set()
        await self.pipeline.stop()
        logger.info("nieTTS 已停止")


async def _run():
    logger.info(BANNER)
    logger.info(f"nieTTS {VERSION} 启动中...")

    app = nieTTS()
    try:
        await app.start()
    finally:
        await app.stop()


def main():
    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        logger.info("收到退出信号")


if __name__ == "__main__":
    main()
