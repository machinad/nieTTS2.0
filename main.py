import asyncio
import logging
import sys

from config.default import ConfigManager
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.stt.service import STTService
from engines.pipeline import RequestPipeline
from web_server import WebServer, WSLogHandler
from certificates.certificates_server import CertificateServer

logging.basicConfig(
    level=logging.INFO,
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

VERSION = "v2.1.2"


class nieTTS:

    def __init__(self):
        self.config = ConfigManager()
        self.tts = TTSService(self.config)
        self.translate = TranslateService(self.config)
        self.osc = OSCService(self.config)
        self.stt = STTService(self.config)
        self.pipeline = RequestPipeline(self.config, self.tts, self.translate, self.osc)
        self.web = WebServer(self.config, self.tts, self.translate, self.osc, self.pipeline, self.stt)
        self.cert = CertificateServer()

        self._host = self.config.get("host", "0.0.0.0")
        self._port = int(self.config.get("port", 11451))

    async def start(self):
        _ws_log_handler.set_loop(asyncio.get_running_loop())
        self._cleanup_orphan_files()
        logger.info("正在启动 Pipeline ...")
        await self.pipeline.start()

        cert_path = str(self.cert.cert_file_path)
        key_path = str(self.cert.key_path)

        logger.info(f"nieTTS {VERSION} 运行在 https://{self._host}:{self._port}")
        logger.info(f"局域网地址: https://{self.cert.ip_address}:{self._port}")

        await self.web.app.run_task(
            host=self._host,
            port=self._port,
            certfile=cert_path,
            keyfile=key_path,
            shutdown_trigger=self._shutdown_trigger,
        )

    async def _shutdown_trigger(self):
        while True:
            await asyncio.sleep(3600)

    def _cleanup_orphan_files(self):
        save_dir = self.config.save_path
        try:
            for f in save_dir.iterdir():
                if f.is_file():
                    f.unlink(missing_ok=True)
        except Exception:
            pass

    async def stop(self):
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
