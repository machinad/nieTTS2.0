import pytest
import numpy as np
from unittest.mock import AsyncMock, MagicMock, patch
from engines.stt.qwen3_stt import Qwen3STT
from engines.stt.base import STTResult


class TestQwen3STT:
    @pytest.fixture
    def engine_no_models(self):
        return Qwen3STT()

    @pytest.fixture
    def engine_with_paths(self, tmp_path):
        """Create dummy model files so is_available() returns True."""
        cf = tmp_path / "conv_frontend.onnx"
        enc = tmp_path / "encoder.onnx"
        dec = tmp_path / "decoder.onnx"
        tok = tmp_path / "tokenizer"
        cf.touch()
        enc.touch()
        dec.touch()
        tok.mkdir()
        return Qwen3STT(
            conv_frontend=str(cf),
            encoder=str(enc),
            decoder=str(dec),
            tokenizer=str(tok),
        )

    def test_engine_name(self, engine_no_models):
        assert engine_no_models.engine_name == "Qwen3"

    def test_is_available_no_models(self, engine_no_models):
        assert engine_no_models.is_available() is False

    def test_is_available_with_models(self, engine_with_paths):
        assert engine_with_paths.is_available() is True

    def test_is_available_partial_paths(self, tmp_path):
        cf = tmp_path / "cf.onnx"
        cf.touch()
        engine = Qwen3STT(conv_frontend=str(cf))
        assert engine.is_available() is False

    @pytest.mark.asyncio
    async def test_transcribe_not_available(self, engine_no_models, dummy_audio_samples):
        result = await engine_no_models.transcribe(dummy_audio_samples, 16000)
        assert result.success is False
        assert "not found" in result.error.lower()

    @pytest.mark.asyncio
    async def test_transcribe_empty_samples(self, engine_with_paths):
        result = await engine_with_paths.transcribe(
            np.array([], dtype=np.float32), 16000
        )
        assert result.success is False
        assert "empty" in result.error.lower()

    @pytest.mark.asyncio
    async def test_transcribe_none_samples(self, engine_with_paths):
        result = await engine_with_paths.transcribe(None, 16000)
        assert result.success is False
        assert "empty" in result.error.lower()
