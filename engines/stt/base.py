from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import numpy as np


@dataclass
class STTResult:
    success: bool
    text: str = ""
    language: str = ""
    emotion: str = ""
    error: str | None = None
    segments: list[dict] = field(default_factory=list)

    @property
    def is_success(self) -> bool:
        return self.success


class BaseSTT(ABC):

    @abstractmethod
    async def transcribe(self, samples: np.ndarray, sample_rate: int) -> STTResult:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...

    @property
    @abstractmethod
    def engine_name(self) -> str:
        ...
