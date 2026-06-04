from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class TranslateResult:
    success: bool
    text: str = ""
    source_lang: str = ""
    target_lang: str = ""
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.success


class BaseTranslate(ABC):

    @abstractmethod
    async def translate(self, text: str, source_lang: str, target_lang: str, **kwargs) -> TranslateResult:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...

    @property
    @abstractmethod
    def engine_name(self) -> str:
        ...

    async def close(self):
        """释放引擎持有的资源（子进程、网络连接等）。子类按需覆盖。"""
        pass
