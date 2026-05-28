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
        self._build_engines()

    def _build_engines(self):
        providers = self.config.get("translation_provider", {}).get("providers", [])
        self._engines: dict[str, BaseTranslate] = {}
        for p in providers:
            name = p.get("name", "")
            cls = _REGISTRY.get(name)
            if cls is None:
                continue
            try:
                self._engines[name] = cls.from_config(p)
            except Exception as e:
                logger.warning("%s translate init skipped: %s", name, e)

    def get_available_engines(self) -> list[str]:
        return [name for name, engine in self._engines.items() if engine.is_available()]

    def get_all_engines(self) -> list[str]:
        providers = self.config.get("translation_provider", {}).get("providers", [])
        return [p["name"] for p in providers if p.get("name")]

    def reload_engines(self):
        self._build_engines()

    async def translate(self, text: str, provider: str = None,
                        source_lang: str = "中文", target_lang: str = "",
                        **kwargs) -> TranslateResult:
        provider = provider or self.config.get("translation_provider.provider", "openai")
        engine = self._engines.get(provider)
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
        target_lang = target_lang or self.config.get("target_lang", "英语")
        return await engine.translate(text, source_lang, target_lang, **kwargs)
