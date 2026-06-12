import logging
from pathlib import Path
import numpy as np
import sherpa_onnx
from engines.stt.vad.base import BaseVAD, SpeechSegment

logger = logging.getLogger(__name__)


class SileroVAD(BaseVAD):
    engine_name = "SileroVAD"

    def __init__(self, model_path: str = "", sample_rate: int = 16000,
                 threshold: float = 0.5, min_silence_duration: float = 0.25,
                 min_speech_duration: float = 0.25, max_speech_duration: float = 15.0,
                 window_size: int = 512, num_threads: int = 4):
        self._model_path = model_path
        self._sample_rate = sample_rate
        self._threshold = threshold
        self._min_silence_duration = min_silence_duration
        self._min_speech_duration = min_speech_duration
        self._max_speech_duration = max_speech_duration
        self._window_size = window_size
        self._num_threads = num_threads
        self._vad = None

    def is_available(self) -> bool:
        if not self._model_path:
            return False
        return Path(self._model_path).exists()

    def _lazy_init(self):
        if self._vad is not None:
            return
        silero_config = sherpa_onnx.SileroVadModelConfig(
            model=self._model_path,
            threshold=self._threshold,
            min_silence_duration=self._min_silence_duration,
            min_speech_duration=self._min_speech_duration,
            max_speech_duration=self._max_speech_duration,
            window_size=self._window_size,
        )
        vad_config = sherpa_onnx.VadModelConfig(
            silero_vad=silero_config,
            sample_rate=self._sample_rate,
            num_threads=self._num_threads,
            provider="cpu",
        )
        self._vad = sherpa_onnx.VoiceActivityDetector(vad_config)
        logger.info("SileroVAD init OK, sr=%d", self._sample_rate)

    def preload(self):
        self._lazy_init()

    def accept_waveform(self, samples: np.ndarray):
        self._lazy_init()
        self._vad.accept_waveform(samples)

    def empty(self) -> bool:
        if self._vad is None:
            return True
        return self._vad.empty()

    @property
    def front(self):
        if self._vad is None or self._vad.empty():
            raise IndexError("VAD is empty")
        seg = self._vad.front
        return SpeechSegment(
            samples=seg.samples,
            start=seg.start,
            sample_rate=self._sample_rate,
        )

    def pop(self):
        if self._vad is not None:
            self._vad.pop()

    def flush(self):
        if self._vad is not None:
            self._vad.flush()

    @property
    def is_speech_detected(self) -> bool:
        if self._vad is None:
            return False
        return self._vad.is_speech_detected
