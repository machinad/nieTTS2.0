import pytest
import numpy as np
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from engines.tts.matcha_tts import MatchaTTS
from engines.tts.base import TTSResult


class TestMatchaTTS:
    @pytest.fixture
    def engine_no_models(self, temp_dir):
        return MatchaTTS(temp_dir)

    @pytest.fixture
    def engine_with_paths(self, tmp_path, temp_dir):
        am = tmp_path / "acoustic.onnx"
        vc = tmp_path / "vocoder.onnx"
        tk = tmp_path / "tokens.txt"
        am.touch()
        vc.touch()
        tk.touch()
        return MatchaTTS(
            temp_dir,
            acoustic_model=str(am),
            vocoder=str(vc),
            tokens_path=str(tk),
        )

    def test_engine_name(self, engine_no_models):
        assert engine_no_models.engine_name == "MatchaTTS"

    def test_is_available_no_models(self, engine_no_models):
        assert engine_no_models.is_available() is False

    def test_is_available_with_models(self, engine_with_paths):
        assert engine_with_paths.is_available() is True

    def test_is_available_partial_models(self, tmp_path, temp_dir):
        am = tmp_path / "acoustic.onnx"
        am.touch()
        engine = MatchaTTS(temp_dir, acoustic_model=str(am))
        assert engine.is_available() is False

    @pytest.mark.asyncio
    async def test_synthesize_not_available(self, engine_no_models):
        result = await engine_no_models.synthesize("Hello", voice="0")
        assert result.success is False
        assert "模型" in result.error

    @patch("engines.tts.matcha_tts.sherpa_onnx")
    @pytest.mark.asyncio
    async def test_synthesize_success(self, mock_sherpa, engine_with_paths):
        mock_tts = MagicMock()
        mock_tts.sample_rate = 22050
        mock_tts.num_speakers = 1
        mock_audio = MagicMock()
        mock_audio.samples = np.zeros(1000, dtype=np.float32)
        mock_audio.sample_rate = 22050
        mock_tts.generate.return_value = mock_audio
        mock_sherpa.OfflineTts.return_value = mock_tts

        result = await engine_with_paths.synthesize("Hello", voice="0")

        assert result.success is True
        assert result.path is not None
        assert result.path.suffix == ".wav"
        assert result.voice == "0"
        assert result.text == "Hello"

    @patch("engines.tts.matcha_tts.sherpa_onnx")
    @pytest.mark.asyncio
    async def test_synthesize_with_speed(self, mock_sherpa, engine_with_paths):
        mock_tts = MagicMock()
        mock_tts.sample_rate = 22050
        mock_tts.num_speakers = 0
        mock_audio = MagicMock()
        mock_audio.samples = np.zeros(500, dtype=np.float32)
        mock_audio.sample_rate = 22050
        mock_tts.generate.return_value = mock_audio
        mock_sherpa.OfflineTts.return_value = mock_tts

        result = await engine_with_paths.synthesize(
            "Test", voice="0", speed=1.5
        )

        assert result.success is True
        mock_tts.generate.assert_called_once_with("Test", sid=0, speed=1.5)

    @patch("engines.tts.matcha_tts.sherpa_onnx")
    @pytest.mark.asyncio
    async def test_synthesize_with_num_steps(self, mock_sherpa, engine_with_paths):
        mock_tts = MagicMock()
        mock_tts.sample_rate = 22050
        mock_tts.num_speakers = 0
        mock_audio = MagicMock()
        mock_audio.samples = np.zeros(500, dtype=np.float32)
        mock_audio.sample_rate = 22050
        mock_tts.generate.return_value = mock_audio
        mock_sherpa.OfflineTts.return_value = mock_tts

        result = await engine_with_paths.synthesize(
            "Test", voice="0", speed=1.0, num_steps=10
        )

        assert result.success is True
        # Should have called generate with config
        call_args = mock_tts.generate.call_args
        assert call_args[0][0] == "Test"

    @patch("engines.tts.matcha_tts.sherpa_onnx")
    @pytest.mark.asyncio
    async def test_synthesize_failure(self, mock_sherpa, engine_with_paths):
        mock_sherpa.OfflineTts.side_effect = Exception("Model load error")

        result = await engine_with_paths.synthesize("Hello", voice="0")

        assert result.success is False
        assert "Model load error" in result.error
