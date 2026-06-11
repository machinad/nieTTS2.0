import asyncio
import json
import logging
import threading
import numpy as np
from quart import Quart, request, jsonify, websocket, send_from_directory
from quart_cors import cors
from config.default import ConfigManager
from config.notifier import ConfigNotifier
from engines.tts.service import TTSService
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.stt.vad.silero_vad import SileroVAD
from engines.pipeline import RequestPipeline
from engines.audio.playback import get_playback_devices
from scripts.download_models import Downloader, ModelRegistry, get_model_status
logger = logging.getLogger(__name__)

_WSS = set()
_WSS_LOCK = asyncio.Lock()
_MAX_TEXT_LENGTH = 5000


class WSLogHandler(logging.Handler):
    """将 Python 日志通过 WebSocket 广播到前端"""

    def __init__(self):
        super().__init__()
        self._loop = None

    def set_loop(self, loop):
        self._loop = loop

    def emit(self, record):
        if self._loop is None:
            return
        try:
            level = record.levelname.lower()
            if level == "warning":
                level = "warn"
            message = f"[{record.name}] {record.getMessage()}"
            coro = _broadcast({"type": "log", "level": level, "message": message})
            if threading.current_thread() is threading.main_thread():
                self._loop.create_task(coro)
            else:
                self._loop.call_soon_threadsafe(self._loop.create_task, coro)
        except Exception:
            import sys
            try:
                sys.stderr.write(f"WSLogHandler error: {record.getMessage()}\n")
            except Exception:
                pass


class WebServer:

    def __init__(self, config: ConfigManager, tts: TTSService,
                 translate: TranslateService, osc: OSCService,
                 pipeline: RequestPipeline,
                 notifier: ConfigNotifier | None = None):
        self.config = config
        self.tts = tts
        self.translate = translate
        self.osc = osc
        self.pipeline = pipeline
        self._notifier = notifier
        self._stt_result_ws_map: dict = {}
        if notifier:
            notifier.on_change(self._on_config_changed, source="gui")

        self.app = Quart(__name__, static_folder=None)
        self.app = cors(self.app)
        self._templates = self.config.project_root / "templates"

        self.app.route("/")(self.index)
        self.app.route("/tts", methods=["POST"])(self.tts_endpoint)
        self.app.route("/config", methods=["GET"])(self.get_config)
        self.app.route("/config", methods=["POST"])(self.update_config)
        self.app.route("/config/reload", methods=["POST"])(self.reload_config)
        self.app.route("/models/status", methods=["GET"])(self.models_status)
        self.app.route("/models/download", methods=["POST"])(self.models_download)
        self.app.websocket("/ws")(self.ws_handler)
        self.app.route("/assets/<path:filename>")(self.serve_assets)

        self._vad_instances: dict = {}
        self._download_task: asyncio.Task | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop

    def _make_vad(self) -> SileroVAD:
        vad_cfg = self.config.config.get("vad", {})
        return SileroVAD(
            model_path=vad_cfg.get("model_path", "models/silero_vad.onnx"),
            sample_rate=vad_cfg.get("sample_rate", 16000),
            threshold=vad_cfg.get("threshold", 0.5),
            min_silence_duration=vad_cfg.get("min_silence_duration", 0.25),
            min_speech_duration=vad_cfg.get("min_speech_duration", 0.25),
            max_speech_duration=vad_cfg.get("max_speech_duration", 15.0),
            window_size=vad_cfg.get("window_size", 512),
        )

    async def index(self):
        from quart import make_response
        index_path = self._templates / "index.html"
        if index_path.exists():
            response = await make_response(
                await send_from_directory(str(self._templates), "index.html")
            )
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        return "<h1>nieTTS 2.0</h1><p>请运行 <code>cd frontend && npm run build</code></p>"

    async def tts_endpoint(self):
        data = await request.get_json()
        if data is None:
            return jsonify({"error": "无效的 JSON 数据"}), 400

        text = (data.get("text") or "").strip()
        if not text:
            return jsonify({"error": "文本内容不能为空"}), 400
        if len(text) > _MAX_TEXT_LENGTH:
            return jsonify({"error": f"文本内容过长，最多 {_MAX_TEXT_LENGTH} 字符"}), 400

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

    async def get_config(self):
        from config.provider_voice import (
            Edge_TTS_voices,
            ali_tts_voices,
            sambert_tts_voices,
        )
        cfg = dict(self.config.config)
        try:
            cfg["available_devices"] = [
                {"name": d["name"]} for d in get_playback_devices()
            ]
        except Exception:
            cfg["available_devices"] = []
        cfg["voices"] = {
            "edge_tts": list(Edge_TTS_voices.keys()),
            "cosyvoice": list(ali_tts_voices.keys()),
            "sambert": list(sambert_tts_voices.keys()),
            "MatchaTTS": ["0"],
        }
        cfg["source_languages"] = ["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语", "俄语"]
        cfg["target_languages"] = ["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语", "俄语"]
        return jsonify(cfg)

    async def update_config(self):
        data = await request.get_json()
        if not data:
            return jsonify({"error": "无效的配置数据"}), 400
        ok = self.config.update(data)
        if ok and self._notifier:
            self._notifier.notify(source="webui")
        return jsonify({"success": ok})

    async def reload_config(self):
        await self.tts.reload_engines()
        await self.translate.reload_engines()
        if self.pipeline.stt:
            await self.pipeline.stt.reload_engines()
        self.osc.reload()
        return jsonify({"success": True})

    def _on_config_changed(self, source):
        if self._loop is None:
            return
        coro = _broadcast({"type": "config_changed"})
        if threading.current_thread() is threading.main_thread():
            self._loop.create_task(coro)
        else:
            self._loop.call_soon_threadsafe(self._loop.create_task, coro)

    async def models_status(self):
        from quart import make_response
        response = await make_response(jsonify(get_model_status()))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    async def models_download(self):
        data = await request.get_json()
        if not data or "source" not in data:
            return jsonify({"error": "缺少 source 参数"}), 400
        source = data["source"]
        if source not in ("huggingface", "huggingface_mirror", "modelscope"):
            return jsonify({"error": f"不支持的下载源: {source}"}), 400

        if self._download_task and not self._download_task.done():
            return jsonify({"error": "下载任务已在运行中"}), 409

        async def _run_download():
            try:
                registry = ModelRegistry()
                downloader = Downloader(source=source, registry=registry)
                ok, fail = await asyncio.to_thread(downloader.download_all)
                logger.info("模型下载完成: %d 成功, %d 失败", ok, fail)
                await _broadcast({"type": "download_done", "ok": ok, "fail": fail})
            except Exception as e:
                logger.error("模型下载异常: %s", e)
                await _broadcast({"type": "download_done", "ok": 0, "fail": -1})

        self._download_task = asyncio.create_task(_run_download())
        return jsonify({"status": "started"})

    async def ws_handler(self):
        ws_obj = websocket._get_current_object()
        async with _WSS_LOCK:
            _WSS.add(ws_obj)
        vad: SileroVAD | None = None

        def _on_stt_done(req_id, text):
            asyncio.ensure_future(ws_obj.send(json.dumps({
                "type": "stt_result", "text": text,
            }, ensure_ascii=False)))

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
                        vad = self._make_vad()
                        self._vad_instances[ws_obj] = vad
                    elif typ == "stop":
                        logger.info("WS: audio stream stop requested")
                        if vad is not None:
                            vad.flush()
                            while not vad.empty():
                                seg = vad.front
                                await self.pipeline.submit(
                                    audio_samples=seg.samples,
                                    sample_rate=seg.sample_rate,
                                    stt_callback=_on_stt_done,
                                )
                                vad.pop()
                        vad = None
                        self._vad_instances.pop(ws_obj, None)
                elif isinstance(raw, bytes):
                    if vad is None:
                        continue
                    try:
                        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
                        vad.accept_waveform(samples)
                        while not vad.empty():
                            seg = vad.front
                            await self.pipeline.submit(
                                audio_samples=seg.samples,
                                sample_rate=seg.sample_rate,
                                stt_callback=_on_stt_done,
                            )
                            vad.pop()
                    except Exception as e:
                        logger.error("WS audio processing error: %s", e)
        except Exception as e:
            logger.info("WS disconnected: %s", e)
        finally:
            async with _WSS_LOCK:
                _WSS.discard(ws_obj)
            self._vad_instances.pop(ws_obj, None)

    async def serve_assets(self, filename):
        return await send_from_directory(str(self._templates / "assets"), filename)


async def _broadcast(msg: dict):
    global _WSS
    data = json.dumps(msg, ensure_ascii=False)
    dead = set()
    async with _WSS_LOCK:
        targets = list(_WSS)
    for ws in targets:
        try:
            await ws.send(data)
        except Exception:
            dead.add(ws)
    if dead:
        async with _WSS_LOCK:
            _WSS -= dead
