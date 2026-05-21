import logging
from config.default import ConfigManager
from engines.translate.base import BaseTranslate, TranslateResult
from engines.translate.openai_translate import OpenAITranslate

logger = logging.getLogger(__name__)


class TranslateService:

    def __init__(self, config: ConfigManager):
        self.config = config
        provider_cfgs = config.get("translation_provider", {}).get("providers", [])

        self._engines: dict[str, BaseTranslate] = {}
        for p in provider_cfgs:
            name = p.get("name", "")
            if not name:
                continue
            if name == "openai":
                api_key = p.get("api_key", "")
                base_url = p.get("url", "")
                model = p.get("model", "") or "gpt-4o-mini"
                self._engines[name] = OpenAITranslate(
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                )

    def get_available_engines(self) -> list[str]:
        return [name for name, engine in self._engines.items() if engine.is_available()]

    def reload_engines(self):
        provider_cfgs = self.config.get("translation_provider", {}).get("providers", [])
        for p in provider_cfgs:
            name = p.get("name", "")
            if name in self._engines:
                self._engines[name].update_config(
                    api_key=p.get("api_key", ""),
                    base_url=p.get("url", ""),
                    model=p.get("model", ""),
                )

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
        target_lang = target_lang or self.config.get("tLanguage", "英语")
        return await engine.translate(text, source_lang, target_lang, **kwargs)
