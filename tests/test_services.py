from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest

from config.default import ConfigManager
from engines.stt.base import STTResult
from engines.stt.service import STTService
from engines.tts.base import TTSResult
from engines.tts.service import TTSService


class TestSTTService:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        ConfigManager._instance = None

    @pytest.fixture
    def mock_config_with_qwen3(self, tmp_path):
        """Config with temporary model files so Qwen3STT.is_available() passes."""
        cf = tmp_path / "conv_frontend.onnx"
        enc = tmp_path / "encoder.onnx"
        dec = tmp_path / "decoder.onnx"
        tok = tmp_path / "tokenizer"
        cf.touch()
        enc.touch()
        dec.touch()
        tok.mkdir()

        cm = ConfigManager()
        cm.config["stt_provider"] = {
            "provider": "Qwen3",
            "providers": [
                {
                    "name": "Qwen3",
                    "conv_frontend": str(cf),
                    "encoder": str(enc),
                    "decoder": str(dec),
                    "tokenizer": str(tok),
                }
            ],
        }
        return cm

    @pytest.fixture
    def mock_config_no_providers(self):
        ConfigManager._instance = None
        cm = ConfigManager()
        cm.config["stt_provider"]["providers"] = []
        return cm

    def test_get_available_engines(self, mock_config_with_qwen3):
        service = STTService(mock_config_with_qwen3)
        available = service.get_available_engines()
        assert "Qwen3" in available

    def test_get_all_engines(self, mock_config_with_qwen3):
        service = STTService(mock_config_with_qwen3)
        all_engines = service.get_all_engines()
        assert "Qwen3" in all_engines

    def test_get_all_engines_empty(self, mock_config_no_providers):
        service = STTService(mock_config_no_providers)
        assert service.get_all_engines() == []

    @pytest.mark.asyncio
    async def test_transcribe_unknown_provider(self, mock_config_with_qwen3):
        service = STTService(mock_config_with_qwen3)
        result = await service.transcribe(np.zeros(100, dtype=np.float32), provider="UnknownEngine")
        assert result.success is False
        assert "Unknown" in result.error

    @pytest.mark.asyncio
    async def test_transcribe_auto_select(self, mock_config_with_qwen3):
        service = STTService(mock_config_with_qwen3)
        # Mock the underlying engine's transcribe to avoid actual model loading
        service._engines["Qwen3"].transcribe = AsyncMock(return_value=STTResult(success=True, text="hello"))
        result = await service.transcribe(np.zeros(100, dtype=np.float32))
        assert result.success is True
        assert result.text == "hello"

    @pytest.mark.asyncio
    async def test_reload_engines(self, mock_config_with_qwen3):
        service = STTService(mock_config_with_qwen3)
        len(service._engines)
        await service.reload_engines()
        # Should rebuild without error
        assert len(service._engines) > 0

    @pytest.mark.asyncio
    async def test_reload_calls_close(self, mock_config_with_qwen3):
        service = STTService(mock_config_with_qwen3)
        mock_engine = AsyncMock()
        mock_engine.is_available.return_value = True
        service._engines["Qwen3"] = mock_engine
        await service.reload_engines()
        mock_engine.close.assert_called_once()


class TestTTSService:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        ConfigManager._instance = None

    @pytest.fixture
    def mock_config(self):
        cm = ConfigManager()
        return cm

    def test_edge_tts_always_available(self, mock_config):
        service = TTSService(mock_config)
        available = service.get_available_engines()
        assert "edge_tts" in available

    def test_get_all_engines(self, mock_config):
        service = TTSService(mock_config)
        all_engines = service.get_all_engines()
        assert "edge_tts" in all_engines
        assert "cosyvoice" in all_engines
        assert "sambert" in all_engines
        assert "MatchaTTS" in all_engines

    @pytest.mark.asyncio
    async def test_synthesize_unknown_provider(self, mock_config):
        service = TTSService(mock_config)
        result = await service.synthesize("Hello", provider="UnknownEngine")
        assert result.success is False
        assert "未知" in result.error

    @pytest.mark.asyncio
    @patch("engines.tts.service.EdgeTTS")
    async def test_synthesize_edge_tts(self, mock_edge_cls, mock_config):
        mock_edge = MagicMock()
        mock_edge.synthesize = AsyncMock(return_value=TTSResult(success=True, text="Hello"))
        mock_edge.is_available.return_value = True
        mock_edge.engine_name = "Edge TTS"
        mock_edge_cls.return_value = mock_edge

        service = TTSService(mock_config)
        service._engines["edge_tts"] = mock_edge

        result = await service.synthesize("Hello", provider="edge_tts")
        assert result.success is True
        mock_edge.synthesize.assert_called_once()

    @pytest.mark.asyncio
    async def test_synthesize_default_provider(self, mock_config):
        service = TTSService(mock_config)
        mock_edge = MagicMock()
        mock_edge.synthesize = AsyncMock(return_value=TTSResult(success=True, text="test"))
        mock_edge.is_available.return_value = True
        service._engines["edge_tts"] = mock_edge

        result = await service.synthesize("test")
        assert result.success is True
        mock_edge.synthesize.assert_called_once()
