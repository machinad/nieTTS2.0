from config.default import ConfigManager
from engines.base import BaseTTS, TTSResult
from engines.edge_tts import EdgeTTS
from engines.cosyvoice_tts import CosyVoiceTTS
from engines.sambert_tts import SambertTTS
from engines.matcha_tts import MatchaTTS


class TTSService:

    def __init__(self, config: ConfigManager):
        self.config = config
        save_dir = config.save_path
        ali_key = config.get("ali_api_key", "")

        self._engines: dict[str, BaseTTS] = {
            "Edge TTS": EdgeTTS(save_dir),
            "MatchaTTS": MatchaTTS(
                save_dir,
                acoustic_model=config.get("matcha_acoustic_model", ""),
                vocoder=config.get("matcha_vocoder", ""),
                tokens_path=config.get("matcha_tokens", ""),
                lexicon_path=config.get("matcha_lexicon", ""),
                data_dir=config.get("matcha_data_dir", ""),
                dict_dir=config.get("matcha_dict_dir", ""),
            ),
            "阿里百炼cosyvoice": CosyVoiceTTS(save_dir, ali_key),
            "阿里百炼Sambert": SambertTTS(save_dir, ali_key),
        }

    def get_available_engines(self) -> list[str]:
        return [name for name, engine in self._engines.items() if engine.is_available()]

    async def synthesize(self, text: str, provider: str = None,
                         voice: str = "", **kwargs) -> TTSResult:
        provider = provider or self.config.get("provider", "Edge TTS")
        engine = self._engines.get(provider)
        if engine is None:
            return TTSResult(success=False, text=text,
                             error=f"未知的 TTS 引擎: {provider}")
        if not engine.is_available():
            return TTSResult(success=False, text=text,
                             error=f"引擎 {provider} 不可用（未配置 API Key）")
        return await engine.synthesize(text, voice, **kwargs)
