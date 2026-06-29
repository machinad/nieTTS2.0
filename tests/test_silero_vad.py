from unittest.mock import MagicMock

import pytest

from engines.stt.vad.silero_vad import SileroVAD


class TestSileroVAD:
    @pytest.fixture
    def vad_no_model(self):
        return SileroVAD()

    @pytest.fixture
    def vad_with_model(self, tmp_path):
        model_file = tmp_path / "silero_vad.onnx"
        model_file.touch()
        return SileroVAD(model_path=str(model_file))

    def test_engine_name(self, vad_no_model):
        assert vad_no_model.engine_name == "SileroVAD"

    def test_is_available_no_model(self, vad_no_model):
        assert vad_no_model.is_available() is False

    def test_is_available_with_model(self, vad_with_model):
        assert vad_with_model.is_available() is True

    def test_is_available_empty_path(self):
        vad = SileroVAD(model_path="")
        assert vad.is_available() is False

    def test_is_available_nonexistent(self):
        vad = SileroVAD(model_path="/nonexistent/path/model.onnx")
        assert vad.is_available() is False

    def test_empty_when_not_initialized(self, vad_no_model):
        assert vad_no_model.empty() is True

    def test_empty_when_initialized_no_model(self, vad_no_model):
        vad_no_model._lazy_init = MagicMock()
        assert vad_no_model.empty() is True

    def test_is_speech_detected_not_initialized(self, vad_no_model):
        assert vad_no_model.is_speech_detected is False

    def test_front_raises_when_not_initialized(self, vad_no_model):
        with pytest.raises(IndexError):
            _ = vad_no_model.front

    def test_constructor_params(self):
        vad = SileroVAD(
            model_path="test.onnx",
            sample_rate=8000,
            threshold=0.7,
            min_silence_duration=0.5,
            min_speech_duration=0.3,
            max_speech_duration=10.0,
            window_size=256,
            num_threads=2,
        )
        assert vad._sample_rate == 8000
        assert vad._threshold == 0.7
        assert vad._min_silence_duration == 0.5
        assert vad._min_speech_duration == 0.3
        assert vad._max_speech_duration == 10.0
        assert vad._window_size == 256
        assert vad._num_threads == 2

    def test_pop_and_flush_safe_when_not_initialized(self, vad_no_model):
        """pop() and flush() should not crash when VAD is not initialized."""
        vad_no_model.pop()
        vad_no_model.flush()
