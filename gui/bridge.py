import asyncio
import logging
from PySide6.QtCore import QObject, Signal
from config.default import ConfigManager
from config.notifier import ConfigNotifier
from config.provider_voice import Edge_TTS_voices, ali_tts_voices, sambert_tts_voices
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.pipeline import RequestPipeline
from engines.audio.playback import get_playback_devices

logger = logging.getLogger(__name__)


class GuiBridge(QObject):
    config_changed = Signal()
    stt_result_ready = Signal(str)

    def __init__(
        self,
        config: ConfigManager,
        tts: TTSService,
        translate: TranslateService,
        osc: OSCService,
        pipeline: RequestPipeline,
        notifier: ConfigNotifier | None = None,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.config = config
        self.tts = tts
        self.translate = translate
        self.osc = osc
        self.pipeline = pipeline
        self.ip_address = "127.0.0.1"
        self.web_port = 11451
        self._notifier = notifier
        if notifier:
            notifier.on_change(self._on_remote_config_change, source="webui")
        if pipeline:
            pipeline.on_stt_result(self._on_stt_result)

    def _on_remote_config_change(self, source):
        self.config_changed.emit()

    def _on_stt_result(self, request_id, text):
        self.stt_result_ready.emit(text)

    def update_config(self, data: dict) -> bool:
        ok = self.config.update(data)
        if not ok:
            logger.error("配置保存失败!")
        elif self._notifier:
            self._notifier.notify(source="gui")
        return ok

    def get_config(self) -> dict:
        cfg = dict(self.config.config)
        cfg["voices"] = {
            "edge_tts": list(Edge_TTS_voices.keys()),
            "cosyvoice": list(ali_tts_voices.keys()),
            "sambert": list(sambert_tts_voices.keys()),
            "MatchaTTS": ["0"],
        }
        return cfg

    def get_provider_config(self, name: str) -> dict:
        return self.config.get_provider_config(name)

    def get_playback_devices(self) -> list[dict]:
        try:
            return [{"name": d["name"]} for d in get_playback_devices()]
        except Exception:
            return []

    async def reload_engines(self):
        await self.tts.reload_engines()
        await self.translate.reload_engines()
        if self.pipeline.stt:
            await self.pipeline.stt.reload_engines()
        self.osc.reload()

    async def download_models(self, source: str):
        from scripts.download_models import Downloader, ModelRegistry
        registry = ModelRegistry()
        downloader = Downloader(source=source, registry=registry)
        ok, fail = await asyncio.to_thread(downloader.download_all)
        return ok, fail
