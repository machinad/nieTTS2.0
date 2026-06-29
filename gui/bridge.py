import asyncio
import logging

from PySide6.QtCore import QObject, Signal

from config.default import ConfigManager
from config.notifier import ConfigNotifier
from config.provider_voice import Edge_TTS_voices, ali_tts_voices, sambert_tts_voices
from engines.audio.playback import get_playback_devices
from engines.osc.service import OSCService
from engines.pipeline import RequestPipeline
from engines.rime.service import RimeService
from engines.translate.service import TranslateService
from engines.tts.service import TTSService

logger = logging.getLogger(__name__)


class GuiBridge(QObject):
    config_changed = Signal()
    engine_changed = Signal()
    download_done = Signal(int, int)
    overlay_hotkey_changed = Signal()
    overlay_hotkey_suspend = Signal()
    overlay_hotkey_resume = Signal()

    def __init__(
        self,
        config: ConfigManager,
        tts: TTSService,
        translate: TranslateService,
        osc: OSCService,
        pipeline: RequestPipeline,
        rime: RimeService | None = None,
        notifier: ConfigNotifier | None = None,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.config = config
        self.tts = tts
        self.translate = translate
        self.osc = osc
        self.pipeline = pipeline
        self.rime = rime
        self.ip_address = "127.0.0.1"
        self.web_port = 11451
        self._notifier = notifier
        if notifier:
            notifier.on_change(self._on_remote_config_change, source="webui")

    def _on_remote_config_change(self, source):
        self.config_changed.emit()

    def update_config(self, data: dict) -> bool:
        ok = self.config.update(data)
        if not ok:
            logger.error("配置保存失败!")
        else:
            if self._notifier:
                self._notifier.notify(source="gui")
            if self._is_engine_config(data):
                self.engine_changed.emit()
        return ok

    def _is_engine_config(self, data: dict) -> bool:
        engine_keys = {"tts_provider", "stt_provider", "translation_provider"}
        return bool(engine_keys & set(data.keys()))

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
        self.download_done.emit(ok, fail)
        return ok, fail

    def build_submit_opts(self, source_lang: str | None = None, target_lang: str | None = None) -> dict:
        cfg = self.get_config()
        providers = cfg.get("tts_provider", {}).get("providers", [])
        engine = cfg.get("tts_provider", {}).get("provider", "edge_tts")
        voice = ""
        for p in providers:
            if p.get("name") == engine:
                voice = p.get("voice", "")
                break
        return {
            "tts_provider": engine,
            "voice": voice,
            "translate": cfg.get("isTranslate"),
            "play_audio": cfg.get("isPlayAudio"),
            "play_translation": cfg.get("isPlayTranslation"),
            "osc_enabled": cfg.get("osc_enabled"),
            "source_lang": source_lang or cfg.get("source_lang"),
            "target_lang": target_lang or cfg.get("target_lang"),
        }

    # ---- Rime 输入法（同步调用，librime 非线程安全） ----

    def rime_key(self, keycode: int, mask: int = 0) -> dict:
        """处理按键"""
        return self.rime.process_key(keycode, mask)

    def rime_select(self, index: int) -> dict:
        """选择候选词"""
        return self.rime.select_candidate(index)

    def rime_page(self, backward: bool = False) -> dict:
        """候选词翻页"""
        return self.rime.change_page(backward)

    def rime_toggle_mode(self) -> dict:
        """切换中英文模式"""
        return self.rime.toggle_ascii_mode()

    def rime_clear(self):
        """清除当前输入组合"""
        self.rime.clear()

    def rime_set_input(self, text: str) -> dict:
        """直接设置输入字符串（支持标点嵌入）"""
        return self.rime.set_input(text)

    def rime_status(self) -> dict:
        """获取 Rime 状态"""
        return self.rime.get_status()

    def rime_schema_list(self) -> list[dict]:
        """获取可用输入方案列表"""
        return self.rime.get_schema_list()

    def rime_current_schema(self) -> str | None:
        """获取当前输入方案 ID"""
        return self.rime.get_current_schema()

    def rime_switch_schema(self, schema_id: str) -> bool:
        """切换输入方案"""
        return self.rime.switch_schema(schema_id)

    def set_rime_schema(self, schema_id: str):
        """持久化当前输入方案到 config"""
        self.config.update({"rime_schema": schema_id})
