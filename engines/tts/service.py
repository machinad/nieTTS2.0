from config.default import ConfigManager
from engines.tts.base import BaseTTS, TTSResult
from engines.tts.edge_tts import EdgeTTS
from engines.tts.cosyvoice_tts import CosyVoiceTTS
from engines.tts.sambert_tts import SambertTTS
from engines.tts.matcha_tts import MatchaTTS


class TTSService:

    def __init__(self, config: ConfigManager):
        self.config = config
        save_dir = config.save_path
        ali_key = config.get("ali_api_key", "")

        matcha_cfg = config.get_provider_config("MatchaTTS")
        self._engines: dict[str, BaseTTS] = {
            "edge_tts": EdgeTTS(save_dir),
            "MatchaTTS": MatchaTTS(
                save_dir,
                acoustic_model=matcha_cfg.get("matcha_acoustic_model", ""),
                vocoder=matcha_cfg.get("matcha_vocoder", ""),
                tokens_path=matcha_cfg.get("matcha_tokens", ""),
                lexicon_path=matcha_cfg.get("matcha_lexicon", ""),
                data_dir=matcha_cfg.get("matcha_data_dir", ""),
                dict_dir=matcha_cfg.get("matcha_dict_dir", ""),
            ),
            "cosyvoice": CosyVoiceTTS(save_dir, ali_key),
            "sambert": SambertTTS(save_dir, ali_key),
        }

    def get_available_engines(self) -> list[str]:
        return [name for name, engine in self._engines.items() if engine.is_available()]

    async def synthesize(self, text: str, provider: str = None,
                         voice: str = "", **kwargs) -> TTSResult:
        provider = provider or self.config.get("tts_provider.provider", "edge_tts")
        engine = self._engines.get(provider)
        if engine is None:
            return TTSResult(success=False, text=text,
                             error=f"未知的 TTS 引擎: {provider}")
        if not engine.is_available():
            return TTSResult(success=False, text=text,
                             error=f"引擎 {provider} 不可用（未配置 API Key）")
        return await engine.synthesize(text, voice, **kwargs)
