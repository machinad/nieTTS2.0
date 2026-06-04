"""
Unit tests for web server REST and WebSocket endpoints.

Uses Quart's built-in test client with mocked backend services.
"""
import json
import copy
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock

from config.default import ConfigManager, default_config
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.stt.service import STTService
from engines.pipeline import RequestPipeline
from web_server import WebServer


@pytest.fixture(autouse=True)
def reset_singleton():
    ConfigManager._instance = None


@pytest.fixture
def mock_config():
    ConfigManager._instance = None
    cm = ConfigManager()
    cm.config = copy.deepcopy(default_config)
    return cm


@pytest.fixture
def mock_tts():
    tts = MagicMock(spec=TTSService)
    tts.synthesize = AsyncMock()
    tts.get_available_engines.return_value = ["edge_tts"]
    tts.get_all_engines.return_value = ["edge_tts", "cosyvoice", "sambert", "MatchaTTS"]
    tts.reload_engines = AsyncMock()
    return tts


@pytest.fixture
def mock_translate():
    t = MagicMock(spec=TranslateService)
    t.translate = AsyncMock()
    t.get_available_engines.return_value = []
    t.reload_engines = AsyncMock()
    return t


@pytest.fixture
def mock_osc():
    osc = MagicMock(spec=OSCService)
    osc.send = MagicMock(return_value=True)
    osc.send_original = MagicMock(return_value=True)
    osc.send_translated = MagicMock(return_value=True)
    osc.reload = MagicMock()
    return osc


@pytest.fixture
def mock_pipeline():
    p = MagicMock(spec=RequestPipeline)
    p.submit_tts = AsyncMock(return_value="abc123def456")
    p.submit_stt_text = AsyncMock(return_value="stt_abc123")
    p.start = AsyncMock()
    p.stop = AsyncMock()
    return p


@pytest.fixture
def mock_stt():
    stt = MagicMock(spec=STTService)
    stt.transcribe = AsyncMock()
    stt.get_available_engines.return_value = []
    stt.get_all_engines.return_value = []
    stt.reload_engines = AsyncMock()
    return stt


@pytest.fixture
def app(mock_config, mock_tts, mock_translate, mock_osc, mock_pipeline, mock_stt):
    server = WebServer(mock_config, mock_tts, mock_translate, mock_osc,
                       mock_pipeline, mock_stt)
    return server.app


@pytest.fixture
def client(app):
    return app.test_client()


# ── GET / ──────────────────────────────────────────────────────────────

class TestIndexEndpoint:
    @pytest.mark.asyncio
    async def test_returns_html_when_index_exists(self, app):
        """When templates/index.html exists, should return it."""
        c = app.test_client()
        resp = await c.get("/")
        assert resp.status_code == 200
        body = await resp.get_data(as_text=True)
        assert len(body) > 0

    @pytest.mark.asyncio
    async def test_returns_fallback_when_no_index(self, app, tmp_path):
        """When templates/index.html missing, return fallback HTML."""
        server = WebServer(
            ConfigManager(), MagicMock(), MagicMock(), MagicMock(),
            MagicMock(), MagicMock()
        )
        server._templates = tmp_path  # empty dir, no index.html
        c = server.app.test_client()
        resp = await c.get("/")
        assert resp.status_code == 200
        body = await resp.get_data(as_text=True)
        assert "nieTTS" in body


# ── GET /assets/<filename> ──────────────────────────────────────────────

class TestAssetsEndpoint:
    @pytest.mark.asyncio
    async def test_serve_existing_asset(self, tmp_path):
        """Serving an existing asset file should return 200."""
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir()
        asset_file = assets_dir / "test.js"
        asset_file.write_text("console.log('hello');")

        server = WebServer(
            ConfigManager(), MagicMock(), MagicMock(), MagicMock(),
            MagicMock(), MagicMock()
        )
        server._templates = tmp_path
        c = server.app.test_client()
        resp = await c.get("/assets/test.js")
        assert resp.status_code == 200
        body = await resp.get_data(as_text=True)
        assert "hello" in body

    @pytest.mark.asyncio
    async def test_missing_asset_returns_404(self, app, tmp_path):
        """Missing asset should return 404."""
        server = WebServer(
            ConfigManager(), MagicMock(), MagicMock(), MagicMock(),
            MagicMock(), MagicMock()
        )
        server._templates = tmp_path
        c = server.app.test_client()
        resp = await c.get("/assets/nonexistent.js")
        assert resp.status_code == 404


# ── POST /tts ───────────────────────────────────────────────────────────

class TestTTSEndpoint:
    @pytest.mark.asyncio
    async def test_valid_request(self, client, mock_pipeline):
        resp = await client.post("/tts", json={
            "text": "你好世界",
            "tts_provider": "edge_tts",
            "voice": "zh-CN-XiaoxiaoNeural",
            "translate": True,
        })
        assert resp.status_code == 202
        data = await resp.get_json()
        assert "request_id" in data
        assert data["request_id"] == "abc123def456"
        mock_pipeline.submit_tts.assert_called_once()

    @pytest.mark.asyncio
    async def test_empty_text(self, client):
        resp = await client.post("/tts", json={"text": ""})
        assert resp.status_code == 400
        data = await resp.get_json()
        assert "文本" in data["error"]

    @pytest.mark.asyncio
    async def test_missing_text(self, client):
        resp = await client.post("/tts", json={})
        assert resp.status_code == 400
        data = await resp.get_json()
        assert "文本" in data["error"]

    @pytest.mark.asyncio
    async def test_text_too_long(self, client):
        resp = await client.post("/tts", json={"text": "x" * 5001})
        assert resp.status_code == 400
        data = await resp.get_json()
        assert "过长" in data["error"]

    @pytest.mark.asyncio
    async def test_text_at_limit(self, client, mock_pipeline):
        resp = await client.post("/tts", json={"text": "x" * 5000})
        assert resp.status_code == 202

    @pytest.mark.asyncio
    async def test_invalid_json(self, client):
        resp = await client.post("/tts", data="not json", headers={"Content-Type": "application/json"})
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_whitespace_only_text(self, client):
        resp = await client.post("/tts", json={"text": "   "})
        assert resp.status_code == 400
        data = await resp.get_json()
        assert "文本" in data["error"]


# ── GET /voices ─────────────────────────────────────────────────────────

class TestVoicesEndpoint:
    @pytest.mark.asyncio
    async def test_returns_voices_json(self, client):
        resp = await client.get("/voices")
        assert resp.status_code == 200
        data = await resp.get_json()
        assert "tts_engines" in data
        assert "all_tts_engines" in data
        assert "voices" in data
        assert "source_languages" in data
        assert "edge_tts" in data["voices"]
        assert "cosyvoice" in data["voices"]
        assert "sambert" in data["voices"]


# ── GET /config ─────────────────────────────────────────────────────────

class TestGetConfig:
    @pytest.mark.asyncio
    async def test_returns_config_json(self, client):
        resp = await client.get("/config")
        assert resp.status_code == 200
        data = await resp.get_json()
        assert "tts_provider" in data
        assert "stt_provider" in data
        assert "available_devices" in data
        assert isinstance(data["available_devices"], list)


# ── POST /config ────────────────────────────────────────────────────────

class TestUpdateConfig:
    @pytest.mark.asyncio
    async def test_valid_update(self, client):
        resp = await client.post("/config", json={"tLanguage": "日语"})
        assert resp.status_code == 200
        data = await resp.get_json()
        assert data["success"] is True

    @pytest.mark.asyncio
    async def test_empty_data(self, client):
        resp = await client.post("/config", json={})
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_no_json(self, client):
        resp = await client.post("/config", data="bad", headers={"Content-Type": "application/json"})
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_update_preserves_other_keys(self, client, mock_config):
        resp = await client.post("/config", json={"tLanguage": "日语"})
        assert resp.status_code == 200
        # TTS provider should still be present
        assert mock_config.get("tts_provider.provider") == "edge_tts"
        assert mock_config.get("tLanguage") == "日语"

    @pytest.mark.asyncio
    async def test_update_does_not_reload(self, client, mock_tts, mock_translate, mock_stt):
        """POST /config should only save, not reload engines."""
        resp = await client.post("/config", json={"target_lang": "日语"})
        assert resp.status_code == 200
        mock_tts.reload_engines.assert_not_called()
        mock_translate.reload_engines.assert_not_called()
        mock_stt.reload_engines.assert_not_called()


# ── POST /config/reload ─────────────────────────────────────────────────

class TestReloadConfig:
    @pytest.mark.asyncio
    async def test_reload(self, client, mock_tts, mock_translate, mock_stt, mock_osc):
        resp = await client.post("/config/reload")
        assert resp.status_code == 200
        data = await resp.get_json()
        assert data["success"] is True
        mock_tts.reload_engines.assert_called_once()
        mock_translate.reload_engines.assert_called_once()
        mock_stt.reload_engines.assert_called_once()
        mock_osc.reload.assert_called_once()


# ── WS /ws ──────────────────────────────────────────────────────────────

# quart_cors requires an Origin header for WebSocket upgrade in test mode
_WS_HEADERS = {"Origin": "http://localhost"}


class TestWebSocket:
    @pytest.mark.asyncio
    async def test_connect_and_disconnect(self, app):
        """WebSocket should connect and disconnect cleanly."""
        c = app.test_client()
        async with c.websocket("/ws", headers=_WS_HEADERS) as ws:
            pass  # just connect and disconnect
        # No exception = pass

    @pytest.mark.asyncio
    async def test_send_start_stop_json(self, app):
        """Send start/stop JSON messages via WebSocket."""
        c = app.test_client()
        async with c.websocket("/ws", headers=_WS_HEADERS) as ws:
            await ws.send(json.dumps({"type": "start"}))
            await ws.send(json.dumps({"type": "stop"}))

    @pytest.mark.asyncio
    async def test_send_unknown_json_type(self, app):
        """Unknown JSON type should be ignored, not crash."""
        c = app.test_client()
        async with c.websocket("/ws", headers=_WS_HEADERS) as ws:
            await ws.send(json.dumps({"type": "unknown", "data": 42}))
            await ws.send(json.dumps({"type": "stop"}))

    @pytest.mark.asyncio
    async def test_send_invalid_json(self, app):
        """Invalid JSON should be ignored, not crash."""
        c = app.test_client()
        async with c.websocket("/ws", headers=_WS_HEADERS) as ws:
            await ws.send("not json at all")
            await ws.send(json.dumps({"type": "stop"}))

    @pytest.mark.asyncio
    async def test_binary_without_start_ignored(self, app):
        """Binary audio data without prior 'start' should be ignored."""
        c = app.test_client()
        audio_bytes = np.zeros(3200, dtype=np.int16).tobytes()
        async with c.websocket("/ws", headers=_WS_HEADERS) as ws:
            await ws.send(audio_bytes)
            await ws.send(json.dumps({"type": "stop"}))

    @pytest.mark.asyncio
    async def test_start_then_binary_audio_flow(self, mock_stt):
        """Start -> binary audio -> stop should process pipeline without crash."""
        mock_stt.transcribe = AsyncMock()
        mock_stt.get_available_engines.return_value = ["Qwen3"]

        ConfigManager._instance = None
        server = WebServer(
            ConfigManager(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            mock_stt,
        )
        server._templates = Path(__file__).parent
        c = server.app.test_client()

        audio_chunk = np.zeros(4800, dtype=np.int16).tobytes()  # 300ms at 16kHz

        async with c.websocket("/ws", headers=_WS_HEADERS) as ws:
            await ws.send(json.dumps({"type": "start"}))
            for _ in range(3):
                await ws.send(audio_chunk)
            await ws.send(json.dumps({"type": "stop"}))

    @pytest.mark.asyncio
    async def test_multiple_websocket_clients_sequential(self, app):
        """Two sequential WebSocket connections should both work."""
        c = app.test_client()
        async with c.websocket("/ws", headers=_WS_HEADERS) as ws1:
            await ws1.send(json.dumps({"type": "start"}))
            await ws1.send(json.dumps({"type": "stop"}))
        async with c.websocket("/ws", headers=_WS_HEADERS) as ws2:
            await ws2.send(json.dumps({"type": "start"}))
            await ws2.send(json.dumps({"type": "stop"}))
