import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TTSResult:
    success: bool
    path: Path | None = None
    voice: str = ""
    text: str = ""
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.success


class BaseTTS(ABC):
    def __init__(self, save_dir: Path):
        self.save_dir = save_dir

    def _make_path(self, suffix: str = ".wav") -> Path:
        return self.save_dir / f"{uuid.uuid4()}{suffix}"

    @abstractmethod
    async def synthesize(self, text: str, voice: str, **kwargs) -> TTSResult: ...

    @abstractmethod
    def is_available(self) -> bool: ...

    async def close(self):
        """释放引擎持有的资源（模型、连接等）。子类按需覆盖。"""
        pass

    @property
    @abstractmethod
    def engine_name(self) -> str: ...
