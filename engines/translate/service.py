import logging
from config.default import ConfigManager
from engines.translate.base import BaseTranslate, TranslateResult
from engines.translate.openai_translate import OpenAITranslate
from engines.translate.hy_mt15_translate import HyMT15Translate

logger = logging.getLogger(__name__)

_REGISTRY: dict[str, type[BaseTranslate]] = {
    "openai": OpenAITranslate,
    "hy_mt15": HyMT15Translate,
}


class TranslateService:

    def __init__(self, config: ConfigManager):
        self.config = config
        self._active_provider = self.config.get("translation_provider.provider")
        self._build_engines()

    def _build_engines(self):
        providers = self.config.get("translation_provider", {}).get("providers", [])
        self.engines: dict[str, BaseTranslate] = {}
        for p in providers:
            name = p.get("name", "")
            cls = _REGISTRY.get(name)
            if cls is None:
                continue
            try:
                self.engines[name] = cls.from_config(p)
            except Exception as e:
                logger.warning("%s translate init skipped: %s", name, e)

    def get_available_engines(self) -> list[str]:
        return [name for name, engine in self.engines.items() if engine.is_available()]

    def get_all_engines(self) -> list[str]:
        providers = self.config.get("translation_provider", {}).get("providers", [])
        return [p["name"] for p in providers if p.get("name")]

    def get_engine_descriptions(self) -> dict[str, str]:
        providers = self.config.get("translation_provider", {}).get("providers", [])
        return {p["name"]: p.get("description", "") for p in providers if p.get("name")}

    async def reload_engines(self):
        await self.close()
        self.engines.clear()
        self._active_provider = self.config.get("translation_provider.provider")
        self._build_engines()

    async def close(self):
        for engine in self.engines.values():
            try:
                await engine.close()
            except Exception:
                pass

    async def translate(self, text: str, provider: str = None,
                        source_lang: str = "中文", target_lang: str = "",
                        **kwargs) -> TranslateResult:
        provider = provider or self.config.get("translation_provider.provider")
        engine = self.engines.get(provider)
        if engine is None:
            return TranslateResult(
                success=False,
                error=f"未知的翻译引擎: {provider}",
            )
        if not engine.is_available():
            return TranslateResult(
                success=False,
                error=f"翻译引擎 {provider} 不可用（未配置 API Key）",
            )
        target_lang = target_lang or self.config.get("target_lang")
        return await engine.translate(text, source_lang, target_lang, **kwargs)
