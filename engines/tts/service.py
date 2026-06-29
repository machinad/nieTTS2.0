import logging

from config.default import ConfigManager
from config.provider_voice import Edge_TTS_voices, ali_tts_voices, sambert_tts_voices
from engines.tts.base import BaseTTS, TTSResult
from engines.tts.cosyvoice_tts import CosyVoiceTTS
from engines.tts.edge_tts import EdgeTTS
from engines.tts.matcha_tts import MatchaTTS
from engines.tts.sambert_tts import SambertTTS

logger = logging.getLogger(__name__)

_VOICE_MAPS = {
    "edge_tts": Edge_TTS_voices,
    "cosyvoice": ali_tts_voices,
    "sambert": sambert_tts_voices,
}

_REGISTRY: dict[str, type[BaseTTS]] = {
    "edge_tts": EdgeTTS,
    "MatchaTTS": MatchaTTS,
    "cosyvoice": CosyVoiceTTS,
    "sambert": SambertTTS,
}


class TTSService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self._build_engines()

    def _build_engines(self):
        save_dir = self.config.save_path
        providers = self.config.get("tts_provider", {}).get("providers", [])
        self._engines: dict[str, BaseTTS] = {}
        for p in providers:
            name = p.get("name", "")
            cls = _REGISTRY.get(name)
            if cls is None:
                continue
            try:
                self._engines[name] = cls.from_config(p, save_dir)
            except Exception as e:
                logger.warning("%s TTS init skipped: %s", name, e)

    def _resolve_voice(self, engine_name: str, voice: str) -> str:
        if not voice:
            return voice
        voice_map = _VOICE_MAPS.get(engine_name)
        if voice_map is not None:
            return voice_map.get(voice, voice)
        return voice

    def get_available_engines(self) -> list[str]:
        return [name for name, engine in self._engines.items() if engine.is_available()]

    def get_all_engines(self) -> list[str]:
        providers = self.config.get("tts_provider", {}).get("providers", [])
        return [p["name"] for p in providers if p.get("name")]

    def get_engine_descriptions(self) -> dict[str, str]:
        providers = self.config.get("tts_provider", {}).get("providers", [])
        return {p["name"]: p.get("description", "") for p in providers if p.get("name")}

    async def reload_engines(self):
        for eng in self._engines.values():
            await eng.close()
        self._build_engines()

    async def synthesize(self, text: str, provider: str = None, voice: str = "", **kwargs) -> TTSResult:
        provider = provider or self.config.get("tts_provider.provider")
        engine = self._engines.get(provider)
        if engine is None:
            return TTSResult(success=False, text=text, error=f"未知的 TTS 引擎: {provider}")
        if not engine.is_available():
            return TTSResult(
                success=False, text=text, error=f"引擎 {provider} 不可用（请检查配置）: {engine.engine_name}"
            )
        resolved_voice = self._resolve_voice(provider, voice)
        return await engine.synthesize(text, resolved_voice, **kwargs)
