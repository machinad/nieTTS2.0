import logging
from openai import AsyncOpenAI
from engines.translate.base import BaseTranslate, TranslateResult

logger = logging.getLogger(__name__)


class OpenAITranslate(BaseTranslate):
    engine_name = "OpenAI"

    @classmethod
    def from_config(cls, cfg: dict):
        return cls(
            api_key=cfg.get("api_key", ""),
            base_url=cfg.get("url", ""),
            model=cfg.get("model", "") or "gpt-4o-mini",
        )

    def __init__(self, api_key: str = "", base_url: str = "", model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=30.0) if api_key else None
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def translate(self, text: str, source_lang: str, target_lang: str, **kwargs) -> TranslateResult:
        model = kwargs.get("model", self.model)
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"你是一个专业的翻译引擎。将以下文本从{source_lang}翻译成{target_lang}。"
                            "只返回翻译结果，不要添加任何解释或额外内容。"
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                temperature=0.3,
            )
            translated = response.choices[0].message.content.strip()
            logger.info(f"OpenAI 翻译成功: {source_lang} -> {target_lang}")
            return TranslateResult(
                success=True,
                text=translated,
                source_lang=source_lang,
                target_lang=target_lang,
            )
        except Exception as e:
            logger.error(f"OpenAI 翻译失败: {e}")
            return TranslateResult(
                success=False,
                source_lang=source_lang,
                target_lang=target_lang,
                error=str(e),
            )
