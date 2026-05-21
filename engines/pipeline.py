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
from engines.translate.base import TranslateResult
from engines.osc.service import OSCService
from engines.audio.playback import play_file

logger = logging.getLogger(__name__)


@dataclass
class TTSRequest:
    text: str
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    tts_provider: str = ""
    voice: str = ""
    translate: bool = True
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
            req.target_lang = self.config.get("tLanguage", "英语")
        await self._request_queue.put(req)
        logger.info(f"请求入队: {req.request_id}  text={text[:40]}")
        return req.request_id

    async def submit_stt_text(self, text: str) -> str:
        return await self.submit_tts(text)

    async def _request_worker(self):
        while self._running:
            try:
                req = await self._request_queue.get()
                await self._process(req)
                self._request_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"_request_worker 异常: {e}")

    async def _process(self, req: TTSRequest) -> None:
        tts_original_task = asyncio.create_task(
            self.tts.synthesize(req.text, provider=req.tts_provider, voice=req.voice)
        )

        translate_future: Optional[asyncio.Task] = None

        if req.translate:
            translate_future = asyncio.create_task(
                self._handle_translate(req)
            )
        elif req.osc_enabled:
            translate_future = asyncio.create_task(
                self._handle_osc_only(req)
            )

        if translate_future:
            done, _ = await asyncio.wait(
                [tts_original_task, translate_future],
                return_when=asyncio.ALL_COMPLETED,
            )
        else:
            await tts_original_task

        original_result: TTSResult = tts_original_task.result()
        translated_audio: Optional[Path] = None
        if translate_future:
            translated_audio = translate_future.result()

        # Push to PlayQueue in fixed order: original first, then translated
        if original_result.is_success and original_result.path:
            await self._play_queue.put(original_result.path)
        else:
            logger.error(f"TTS(原文) 失败: {original_result.error}")

        if translated_audio:
            await self._play_queue.put(translated_audio)

    async def _handle_translate(self, req: TTSRequest) -> Optional[Path]:
        translate_result: TranslateResult = await self.translate.translate(
            req.text,
            source_lang=req.source_lang,
            target_lang=req.target_lang,
        )

        if translate_result.is_success and translate_result.text:
            if req.osc_enabled:
                self.osc.send_translated(req.text, translate_result.text)

            if req.play_translation:
                tts_result = await self.tts.synthesize(
                    translate_result.text,
                    provider=req.tts_provider,
                    voice=req.voice,
                )
                if tts_result.is_success and tts_result.path:
                    return tts_result.path
        else:
            logger.error(f"翻译失败: {translate_result.error}")
            if req.osc_enabled:
                self.osc.send_original(req.text)

        return None

    async def _handle_osc_only(self, req: TTSRequest) -> Optional[Path]:
        self.osc.send_original(req.text)
        return None

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
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
                self._play_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"_play_worker 异常: {e}")
