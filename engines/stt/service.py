import logging
from config.default import ConfigManager
from engines.stt.base import BaseSTT, STTResult

logger = logging.getLogger(__name__)


def _import_qwen3():
    from engines.stt.qwen3_stt import Qwen3STT
    return Qwen3STT


class STTService:

    def __init__(self, config: ConfigManager):
        self.config = config
        self._build_engines()

    def _build_engines(self):
        self._engines: dict[str, BaseSTT] = {}
        qwen3_cfg = self.config.get_stt_provider_config("Qwen3")
        try:
            Qwen3STT = _import_qwen3()
            self._engines["Qwen3"] = Qwen3STT(
                conv_frontend=qwen3_cfg.get("conv_frontend", ""),
                encoder=qwen3_cfg.get("encoder", ""),
                decoder=qwen3_cfg.get("decoder", ""),
                tokenizer=qwen3_cfg.get("tokenizer", ""),
            )
        except Exception as e:
            logger.warning("Qwen3 STT init skipped: %s", e)

    def get_available_engines(self) -> list[str]:
        return [n for n, e in self._engines.items() if e.is_available()]

    def get_all_engines(self) -> list[str]:
        providers = self.config.get("stt_provider", {}).get("providers", [])
        return [p["name"] for p in providers if p.get("name")]

    def reload_engines(self):
        self._build_engines()

    async def transcribe(self, samples, sample_rate: int = 16000,
                         provider: str = "") -> STTResult:
        provider = provider or self.config.get("stt_provider.provider", "")
        if not provider:
            available = self.get_available_engines()
            provider = available[0] if available else ""
        engine = self._engines.get(provider)
        if engine is None:
            return STTResult(success=False,
                             error=f"Unknown STT engine: {provider}")
        if not engine.is_available():
            return STTResult(success=False,
                             error=f"Engine {provider} not available")
        return await engine.transcribe(samples, sample_rate)
