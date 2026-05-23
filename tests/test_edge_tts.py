import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from engines.tts.edge_tts import EdgeTTS
from engines.tts.base import TTSResult


class TestEdgeTTS:
    @pytest.fixture
    def engine(self, temp_dir):
        return EdgeTTS(temp_dir)

    def test_engine_name(self, engine):
        assert engine.engine_name == "Edge TTS"

    def test_is_available(self, engine):
        assert engine.is_available() is True

    @patch("engines.tts.edge_tts.edge")
    @pytest.mark.asyncio
    async def test_synthesize_success(self, mock_edge, engine):
        mock_comm = MagicMock()
        mock_comm.save = AsyncMock()
        mock_edge.Communicate.return_value = mock_comm

        result = await engine.synthesize(
            text="Hello world", voice="zh-CN-XiaoxiaoNeural"
        )

        assert result.success is True
        assert result.voice == "zh-CN-XiaoxiaoNeural"
        assert result.text == "Hello world"
        assert result.path is not None
        assert result.path.suffix == ".mp3"
        mock_edge.Communicate.assert_called_once_with(
            "Hello world", "zh-CN-XiaoxiaoNeural"
        )
        mock_comm.save.assert_called_once()

    @patch("engines.tts.edge_tts.edge")
    @pytest.mark.asyncio
    async def test_synthesize_failure(self, mock_edge, engine):
        mock_edge.Communicate.side_effect = Exception("Network error")

        result = await engine.synthesize(
            text="Hello", voice="zh-CN-XiaoxiaoNeural"
        )

        assert result.success is False
        assert "Network error" in result.error
        assert result.text == "Hello"
        assert result.voice == "zh-CN-XiaoxiaoNeural"

    @patch("engines.tts.edge_tts.edge")
    @pytest.mark.asyncio
    async def test_synthesize_empty_text(self, mock_edge, engine):
        mock_comm = MagicMock()
        mock_comm.save = AsyncMock()
        mock_edge.Communicate.return_value = mock_comm

        result = await engine.synthesize(text="", voice="zh-CN-XiaoxiaoNeural")

        assert result.success is True
        mock_edge.Communicate.assert_called_once_with("", "zh-CN-XiaoxiaoNeural")
