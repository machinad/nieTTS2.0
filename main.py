import asyncio
import logging
import sys

from hypercorn.config import Config as HypercornConfig
from hypercorn.asyncio import serve

from config.default import ConfigManager
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.pipeline import RequestPipeline
from web_server import WebServer
from certificates.certificates_server import CertificateServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

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
        self.pipeline = RequestPipeline(self.config, self.tts, self.translate, self.osc)
        self.web = WebServer(self.config, self.tts, self.translate, self.osc, self.pipeline)
        self.cert = CertificateServer()

        self._host = self.config.get("host", "0.0.0.0")
        self._port = int(self.config.get("port", 11451))

    async def start(self):
        logger.info("正在启动 Pipeline ...")
        await self.pipeline.start()

        cert_path = str(self.cert.cert_file_path)
        key_path = str(self.cert.key_path)

        hc = HypercornConfig()
        hc.bind = [f"{self._host}:{self._port}"]
        hc.certfile = cert_path
        hc.keyfile = key_path

        logger.info(f"nieTTS {VERSION} 运行在 https://{self._host}:{self._port}")
        logger.info(f"局域网地址: https://{self.cert.ip_address}:{self._port}")

        await serve(self.web.app, hc, shutdown_trigger=self._shutdown_trigger)

    async def _shutdown_trigger(self):
        while True:
            await asyncio.sleep(3600)

    async def stop(self):
        await self.pipeline.stop()
        logger.info("nieTTS 已停止")


def main():
    logger.info(BANNER)
    logger.info(f"nieTTS {VERSION} 启动中...")

    app = nieTTS()

    try:
        asyncio.run(app.start())
    except KeyboardInterrupt:
        logger.info("收到退出信号")
    finally:
        asyncio.run(app.stop())


if __name__ == "__main__":
    main()
