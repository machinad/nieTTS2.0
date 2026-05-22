import asyncio
import logging
from pathlib import Path
import numpy as np
import sherpa_onnx
from engines.stt.base import BaseSTT, STTResult

logger = logging.getLogger(__name__)


class Qwen3STT(BaseSTT):
    engine_name = "Qwen3"

    def __init__(self, conv_frontend: str = "", encoder: str = "",
                 decoder: str = "", tokenizer: str = "",
                 sample_rate: int = 16000, num_threads: int = 4):
        self._conv_frontend = conv_frontend
        self._encoder = encoder
        self._decoder = decoder
        self._tokenizer = tokenizer
        self._sample_rate = sample_rate
        self._num_threads = num_threads
        self._recognizer = None

    def is_available(self) -> bool:
        cf = Path(self._conv_frontend) if self._conv_frontend else None
        enc = Path(self._encoder) if self._encoder else None
        dec = Path(self._decoder) if self._decoder else None
        tok = Path(self._tokenizer) if self._tokenizer else None
        return (cf and enc and dec and tok
                and cf.exists() and enc.exists() and dec.exists() and tok.is_dir())

    def _lazy_init(self):
        if self._recognizer is not None:
            return
        logger.info("Loading Qwen3 ASR model...")
        self._recognizer = sherpa_onnx.OfflineRecognizer.from_qwen3_asr(
            conv_frontend=self._conv_frontend,
            encoder=self._encoder,
            decoder=self._decoder,
            tokenizer=self._tokenizer,
            num_threads=self._num_threads,
            sample_rate=self._sample_rate,
            provider="cpu",
        )
        logger.info("Qwen3 ASR model loaded")

    async def transcribe(self, samples: np.ndarray, sample_rate: int) -> STTResult:
        if not self.is_available():
            return STTResult(
                success=False,
                error="Qwen3 ASR model not found",
            )
        if samples is None or len(samples) == 0:
            return STTResult(success=False, error="Audio data is empty")
        try:
            self._lazy_init()
            stream = self._recognizer.create_stream()
            stream.accept_waveform(sample_rate, samples)
            await asyncio.to_thread(self._recognizer.decode_stream, stream)
            text = stream.result.text.strip()
            logger.info("Qwen3 STT: %s", text[:80])
            return STTResult(success=True, text=text, language="zh")
        except Exception as e:
            logger.error("Qwen3 STT failed: %s", e)
            return STTResult(success=False, error=str(e))
