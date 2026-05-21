from config.default import ConfigManager
from config.provider_voice import Edge_TTS_voices, ali_tts_voices, sambert_tts_voices
from engines.tts.base import BaseTTS, TTSResult
from engines.tts.edge_tts import EdgeTTS


_VOICE_MAPS = {
    "edge_tts": Edge_TTS_voices,
    "cosyvoice": ali_tts_voices,
    "sambert": sambert_tts_voices,
}


def _import_cosyvoice():
    from engines.tts.cosyvoice_tts import CosyVoiceTTS
    return CosyVoiceTTS


def _import_sambert():
    from engines.tts.sambert_tts import SambertTTS
    return SambertTTS


def _import_matcha():
    from engines.tts.matcha_tts import MatchaTTS
    return MatchaTTS


class TTSService:

    def __init__(self, config: ConfigManager):
        self.config = config
        self._build_engines()

    def _build_engines(self):
        save_dir = self.config.save_path
        ali_key = self.config.get("ali_api_key", "")
        matcha_cfg = self.config.get_provider_config("MatchaTTS")

        self._engines: dict[str, BaseTTS] = {
            "edge_tts": EdgeTTS(save_dir),
        }

        try:
            MatchaTTS = _import_matcha()
            self._engines["MatchaTTS"] = MatchaTTS(
                save_dir,
                acoustic_model=matcha_cfg.get("matcha_acoustic_model", ""),
                vocoder=matcha_cfg.get("matcha_vocoder", ""),
                tokens_path=matcha_cfg.get("matcha_tokens", ""),
                lexicon_path=matcha_cfg.get("matcha_lexicon", ""),
                data_dir=matcha_cfg.get("matcha_data_dir", ""),
                dict_dir=matcha_cfg.get("matcha_dict_dir", ""),
            )
        except Exception:
            pass

        try:
            CosyVoiceTTS = _import_cosyvoice()
            self._engines["cosyvoice"] = CosyVoiceTTS(save_dir, ali_key)
        except Exception:
            pass

        try:
            SambertTTS = _import_sambert()
            self._engines["sambert"] = SambertTTS(save_dir, ali_key)
        except Exception:
            pass

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

    def reload_engines(self):
        ali_key = self.config.get("ali_api_key", "")
        if "cosyvoice" in self._engines:
            self._engines["cosyvoice"].api_key = ali_key
        if "sambert" in self._engines:
            self._engines["sambert"].api_key = ali_key
        try:
            if "MatchaTTS" in self._engines:
                MatchaTTS = _import_matcha()
                self._engines["MatchaTTS"] = MatchaTTS(
                    self.config.save_path,
                    acoustic_model=self.config.get_provider_config("MatchaTTS").get("matcha_acoustic_model", ""),
                    vocoder=self.config.get_provider_config("MatchaTTS").get("matcha_vocoder", ""),
                    tokens_path=self.config.get_provider_config("MatchaTTS").get("matcha_tokens", ""),
                    lexicon_path=self.config.get_provider_config("MatchaTTS").get("matcha_lexicon", ""),
                    data_dir=self.config.get_provider_config("MatchaTTS").get("matcha_data_dir", ""),
                    dict_dir=self.config.get_provider_config("MatchaTTS").get("matcha_dict_dir", ""),
                )
        except Exception:
            pass

    async def synthesize(self, text: str, provider: str = None,
                         voice: str = "", **kwargs) -> TTSResult:
        provider = provider or self.config.get("tts_provider.provider", "edge_tts")
        engine = self._engines.get(provider)
        if engine is None:
            return TTSResult(success=False, text=text,
                             error=f"未知的 TTS 引擎: {provider}")
        if not engine.is_available():
            return TTSResult(success=False, text=text,
                             error=f"引擎 {provider} 不可用（请检查配置）: {engine.engine_name}")
        resolved_voice = self._resolve_voice(provider, voice)
        return await engine.synthesize(text, resolved_voice, **kwargs)
