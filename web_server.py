import json
import logging
from pathlib import Path

from quart import Quart, request, jsonify, websocket, send_from_directory
from quart_cors import cors

from config.default import ConfigManager
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.pipeline import RequestPipeline
from engines.audio.playback import get_playback_devices

logger = logging.getLogger(__name__)

_WSS = set()


class WebServer:

    def __init__(self, config: ConfigManager, tts: TTSService,
                 translate: TranslateService, osc: OSCService,
                 pipeline: RequestPipeline):
        self.config = config
        self.tts = tts
        self.translate = translate
        self.osc = osc
        self.pipeline = pipeline

        self.app = Quart(__name__, static_folder=None)
        self.app = cors(self.app)
        self._templates = self.config.project_root / "templates"

        self.app.route("/")(self.index)
        self.app.route("/tts", methods=["POST"])(self.tts_endpoint)
        self.app.route("/voices")(self.voices_endpoint)
        self.app.route("/config", methods=["GET"])(self.get_config)
        self.app.route("/config", methods=["POST"])(self.update_config)
        self.app.route("/ws")(self.ws_handler)
        self.app.route("/assets/<path:filename>")(self.serve_assets)

    async def index(self):
        index_path = self._templates / "index.html"
        if index_path.exists():
            return await send_from_directory(str(self._templates), "index.html")
        return "<h1>nieTTS 2.0</h1><p>请运行 <code>cd frontend && npm run build</code></p>"

    async def tts_endpoint(self):
        data = await request.get_json()
        if data is None:
            return jsonify({"error": "无效的 JSON 数据"}), 400

        text = (data.get("text") or "").strip()
        if not text:
            return jsonify({"error": "文本内容不能为空"}), 400
        if len(text) > 5000:
            return jsonify({"error": "文本内容过长，最多 5000 字符"}), 400

        req_id = await self.pipeline.submit_tts(
            text=text,
            tts_provider=data.get("tts_provider", ""),
            voice=data.get("voice", ""),
            translate=bool(data.get("translate", True)),
            play_audio=bool(data.get("play_audio", True)),
            play_translation=bool(data.get("play_translation", True)),
            osc_enabled=bool(data.get("osc_enabled", True)),
            source_lang=data.get("source_lang", "中文"),
            target_lang=data.get("target_lang", ""),
        )

        await _broadcast({"type": "status", "request_id": req_id, "state": "queued"})
        return jsonify({"request_id": req_id}), 202

    async def voices_endpoint(self):
        from config.provider_voice import (
            Edge_TTS_voices,
            ali_tts_voices,
            sambert_tts_voices,
        )
        engines = self.tts.get_available_engines()
        all_engines = self.tts.get_all_engines()
        translate_engines = self.translate.get_available_engines()

        return jsonify({
            "tts_engines": engines,
            "all_tts_engines": all_engines,
            "translate_engines": translate_engines,
            "voices": {
                "edge_tts": list(Edge_TTS_voices.keys()),
                "cosyvoice": list(ali_tts_voices.keys()),
                "sambert": list(sambert_tts_voices.keys()),
                "MatchaTTS": ["0"],
            },
            "source_languages": ["中文", "英语", "日语"],
            "target_languages": [self.config.get("tLanguage", "英语")],
        })

    async def get_config(self):
        cfg = dict(self.config.config)
        try:
            cfg["available_devices"] = [
                {"name": d["name"]} for d in get_playback_devices()
            ]
        except Exception:
            cfg["available_devices"] = []
        return jsonify(cfg)

    async def update_config(self):
        data = await request.get_json()
        if not data:
            return jsonify({"error": "无效的配置数据"}), 400
        ok = self.config.update(data)
        if ok:
            self.tts.reload_engines()
            self.translate.reload_engines()
            self.osc.reload()
        return jsonify({"success": ok})

    async def ws_handler(self):
        ws_obj = websocket._get_current_object()
        _WSS.add(ws_obj)
        try:
            while True:
                raw = await websocket.receive()
                if isinstance(raw, str):
                    try:
                        msg = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    typ = msg.get("type")
                    if typ == "start":
                        logger.info("WS: 客户端请求开始音频流")
                    elif typ == "stop":
                        logger.info("WS: 客户端请求停止音频流")
                elif isinstance(raw, bytes):
                    logger.debug(f"WS: 收到音频数据 {len(raw)} bytes")
        except Exception as e:
            logger.info(f"WS 断开: {e}")
        finally:
            _WSS.discard(ws_obj)

    async def serve_assets(self, filename):
        return await send_from_directory(str(self._templates / "assets"), filename)


async def _broadcast(msg: dict):
    global _WSS
    data = json.dumps(msg, ensure_ascii=False)
    dead = set()
    for ws in _WSS:
        try:
            await ws.send(data)
        except Exception:
            dead.add(ws)
    _WSS -= dead
