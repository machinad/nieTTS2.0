from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np


@dataclass
class SpeechSegment:
    samples: np.ndarray
    start: int
    sample_rate: int = 16000

    @property
    def start_sec(self) -> float:
        return self.start / self.sample_rate

    @property
    def duration_sec(self) -> float:
        return len(self.samples) / self.sample_rate


class BaseVAD(ABC):

    @abstractmethod
    def accept_waveform(self, samples: np.ndarray):
        ...

    @abstractmethod
    def empty(self) -> bool:
        ...

    @property
    @abstractmethod
    def front(self) -> SpeechSegment:
        ...

    @abstractmethod
    def pop(self):
        ...

    @abstractmethod
    def flush(self):
        ...

    @property
    @abstractmethod
    def is_speech_detected(self) -> bool:
        ...

    @property
    @abstractmethod
    def engine_name(self) -> str:
        ...

    def preload(self):
        """预加载资源（可选覆盖）"""
        pass
