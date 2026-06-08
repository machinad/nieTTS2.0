import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from config.default import ConfigManager
from engines.tts.service import TTSService
from engines.tts.base import TTSResult
from engines.translate.service import TranslateService
from engines.osc.service import OSCService
from engines.audio.playback import play_file

logger = logging.getLogger(__name__)

_LANG_EDGE_VOICE = {
    "英语": "en-US-AriaNeural",
    "日语": "ja-JP-NanamiNeural",
    "韩语": "ko-KR-SunHiNeural",
    "中文": "zh-CN-XiaoxiaoNeural",
    "法语": "fr-FR-DeniseNeural",
    "德语": "de-DE-KatjaNeural",
    "西班牙语": "es-ES-ElviraNeural",
    "俄语": "ru-RU-SvetlanaNeural",
    "葡萄牙语": "pt-BR-FranciscaNeural",
    "意大利语": "it-IT-ElsaNeural",
    "阿拉伯语": "ar-SA-ZariyahNeural",
    "印尼语": "id-ID-GadisNeural",
    "泰语": "th-TH-PremwadeeNeural",
    "越南语": "vi-VN-HoaiMyNeural",
    "粤语": "zh-HK-HiuGaaiNeural",
}
_DEFAULT_EDGE_VOICE = "en-US-AriaNeural"

_ENGINE_LANGS = {
    "edge_tts": {"中文", "英语"},
    "MatchaTTS": {"中文", "英语"},
    "cosyvoice": {"中文", "英语", "日语", "韩语"},
    "sambert": {"中文", "英语"},
}


def _resolve_edge_voice(target_lang: str) -> str:
    return _LANG_EDGE_VOICE.get(target_lang, _DEFAULT_EDGE_VOICE)


def _engine_supports_lang(engine: str, lang: str) -> bool:
    langs = _ENGINE_LANGS.get(engine)
    if langs is None:
        return False
    return lang in langs


@dataclass
class TTSRequest:
    text: str
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    tts_provider: str = ""
    voice: str = ""
    translate: bool = True
    play_audio: bool = True
    play_translation: bool = True
    osc_enabled: bool = True
    source_lang: str = "中文"
    target_lang: str = ""


class RequestPipeline:

    def __init__(self, config: ConfigManager, tts: TTSService,
                 translate: TranslateService, osc: OSCService):
        self.config = config
        self.tts = tts
        self.translate = translate
        self.osc = osc

        self._request_queue: asyncio.Queue[TTSRequest] = asyncio.Queue()
        self._play_queue: asyncio.Queue[Path | None] = asyncio.Queue()

        self._running = False
        self._request_task: Optional[asyncio.Task] = None
        self._play_task: Optional[asyncio.Task] = None
        self._bg_tasks: set[asyncio.Task] = set()

    async def start(self):
        if self._running:
            return
        self._running = True
        self._request_task = asyncio.create_task(self._request_worker())
        self._play_task = asyncio.create_task(self._play_worker())
        logger.info("RequestPipeline 已启动")

    async def stop(self):
        self._running = False
        for task in (self._request_task, self._play_task):
            if task and not task.done():
                task.cancel()
        for task in list(self._bg_tasks):
            if not task.done():
                task.cancel()
        if self._bg_tasks:
            await asyncio.gather(*self._bg_tasks, return_exceptions=True)
            self._bg_tasks.clear()
        logger.info("RequestPipeline 已停止")

    async def submit_tts(self, text: str, **opts) -> str:
        req = TTSRequest(text=text, **{
            k: v for k, v in opts.items()
            if k in TTSRequest.__dataclass_fields__ and k != "request_id"
        })
        if not req.tts_provider:
            req.tts_provider = self.config.get("tts_provider.provider", "edge_tts")
        if not req.voice:
            provider_cfg = self.config.get_provider_config(req.tts_provider)
            req.voice = provider_cfg.get("voice", "")
        if not req.target_lang:
            req.target_lang = self.config.get("target_lang", "英语")
        await self._request_queue.put(req)
        logger.info(f"请求入队: {req.request_id}  text={text[:40]}")
        return req.request_id

    async def submit_stt_text(self, text: str) -> str:
        return await self.submit_tts(text)

    async def _request_worker(self):
        while self._running:
            try:
                req = await self._request_queue.get()
                try:
                    await self._process(req)
                finally:
                    self._request_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"_request_worker 异常: {e}")

    async def _process(self, req: TTSRequest) -> None:
        # 先启动翻译（异步），与原文 TTS 并行执行
        if req.translate or req.play_translation:
            task = asyncio.create_task(self._handle_translate_bg(req))
            self._bg_tasks.add(task)
            task.add_done_callback(self._bg_tasks.discard)
            await asyncio.sleep(0)  # 让出控制权，确保翻译任务立即启动

        if req.play_audio:
            original_result: TTSResult
            try:
                if _engine_supports_lang(req.tts_provider, req.source_lang):
                    original_result = await self.tts.synthesize(
                        req.text, provider=req.tts_provider, voice=req.voice
                    )
                else:
                    logger.warning(f"{req.tts_provider} 不支持{req.source_lang}，自动使用 edge_tts")
                    edge_voice = _resolve_edge_voice(req.source_lang)
                    original_result = await self.tts.synthesize(
                        req.text, provider="edge_tts", voice=edge_voice
                    )
            except Exception as e:
                logger.exception(f"TTS(原文) 执行异常: {e}")
                original_result = TTSResult(success=False, text=req.text, error=str(e))

            if original_result.is_success and original_result.path:
                await self._play_queue.put(original_result.path)
            else:
                logger.error(f"TTS(原文) 失败: {original_result.error}")

        if not req.translate and req.osc_enabled:
            self.osc.send_original(req.text)

    async def _handle_translate_bg(self, req: TTSRequest) -> None:
        try:
            translate_result = await self.translate.translate(
                req.text,
                source_lang=req.source_lang,
                target_lang=req.target_lang,
            )

            if translate_result.is_success and translate_result.text:
                if req.osc_enabled:
                    self.osc.send_translated(req.text, translate_result.text)

                if req.play_translation:
                    if _engine_supports_lang(req.tts_provider, req.target_lang):
                        tts_result = await self.tts.synthesize(
                            translate_result.text,
                            provider=req.tts_provider,
                            voice=req.voice,
                        )
                    else:
                        logger.warning(f"{req.tts_provider} 不支持{req.target_lang}，译文自动使用 edge_tts")
                        voice = _resolve_edge_voice(req.target_lang)
                        tts_result = await self.tts.synthesize(
                            translate_result.text,
                            provider="edge_tts",
                            voice=voice,
                        )
                    if tts_result.is_success and tts_result.path:
                        await self._play_queue.put(tts_result.path)
            else:
                logger.error(f"翻译失败: {translate_result.error}")
                if req.osc_enabled:
                    self.osc.send_original(req.text)
        except Exception as e:
            logger.exception(f"_handle_translate_bg 异常: {e}")

    async def _play_worker(self):
        while self._running:
            try:
                path = await self._play_queue.get()
                if path is None:
                    self._play_queue.task_done()
                    continue
                if path.exists():
                    device_name = self.config.get("device", "")
                    await play_file(path, device_name=device_name)
                else:
                    logger.warning(f"音频文件不存在，跳过播放: {path}")
                for _ in range(10):
                    try:
                        path.unlink(missing_ok=True)
                        break
                    except PermissionError:
                        await asyncio.sleep(0.05)
                self._play_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"_play_worker 异常: {e}")
                self._play_queue.task_done()
