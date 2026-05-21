import logging
from pythonosc import udp_client
from config.default import ConfigManager

logger = logging.getLogger(__name__)

_PATH = "/chatbox/input"
_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = 9000


class OSCService:

    def __init__(self, config: ConfigManager):
        self.config = config
        host = config.get("osc_host", _DEFAULT_HOST)
        port = int(config.get("osc_port", _DEFAULT_PORT))
        self.client = udp_client.SimpleUDPClient(host, port)

    @property
    def host(self) -> str:
        return self.client._address

    @property
    def port(self) -> int:
        return self.client._port

    def send(self, text: str) -> bool:
        try:
            self.client.send_message(_PATH, [text, True])
            logger.info(f"OSC 已发送到 {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"OSC 发送失败: {e}")
            return False

    def send_original(self, text: str) -> bool:
        return self.send(text)

    def send_translated(self, original: str, translated: str) -> bool:
        return self.send(f"{original}\n{translated}")
