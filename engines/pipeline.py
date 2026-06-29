import asyncio
import logging
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from config.default import ConfigManager
from engines.audio.playback import play_file
from engines.osc.service import OSCService
from engines.translate.service import TranslateService
from engines.tts.base import TTSResult
from engines.tts.service import TTSService

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
class PipelineRequest:
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    # 输入（二选一）
    text: str = ""
    audio_samples: np.ndarray | None = field(default=None, repr=False)
    sample_rate: int = 16000
    # TTS 参数
    tts_provider: str = ""
    voice: str = ""
    translate: bool = True
    play_audio: bool = True
    play_translation: bool = True
    osc_enabled: bool = True
    source_lang: str = "中文"
    target_lang: str = ""
    # STT 结果回调（可选，优先于全局回调）
    _stt_callback: Callable[[str, str], None] | None = field(default=None, repr=False, compare=False)


# 向后兼容
TTSRequest = PipelineRequest


class RequestPipeline:
    def __init__(self, config: ConfigManager, tts: TTSService, translate: TranslateService, osc: OSCService, stt=None):
        self.config = config
        self.tts = tts
        self.translate = translate
        self.osc = osc
        self.stt = stt

        self._request_queue: asyncio.Queue[PipelineRequest] = asyncio.Queue()
        self._play_queue: asyncio.Queue[Path | None] = asyncio.Queue()

        self._running = False
        self._request_task: asyncio.Task | None = None
        self._play_task: asyncio.Task | None = None
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
        # 取消并等待 worker tasks
        worker_tasks = [t for t in (self._request_task, self._play_task) if t and not t.done()]
        for task in worker_tasks:
            task.cancel()
        if worker_tasks:
            await asyncio.gather(*worker_tasks, return_exceptions=True)
        # 取消并等待后台翻译 tasks
        bg_tasks = list(self._bg_tasks)
        for task in bg_tasks:
            if not task.done():
                task.cancel()
        if bg_tasks:
            await asyncio.gather(*bg_tasks, return_exceptions=True)
            self._bg_tasks.clear()
        logger.info("RequestPipeline 已停止")

    async def submit(
        self,
        *,
        text: str = "",
        audio_samples: np.ndarray | None = None,
        sample_rate: int = 16000,
        stt_callback: Callable | None = None,
        **opts,
    ) -> str:
        req = PipelineRequest(
            text=text,
            audio_samples=audio_samples,
            sample_rate=sample_rate,
            _stt_callback=stt_callback,
            **{k: v for k, v in opts.items() if k in PipelineRequest.__dataclass_fields__ and k != "request_id"},
        )
        if not req.tts_provider:
            req.tts_provider = self.config.get("tts_provider.provider")
        if not req.voice:
            provider_cfg = self.config.get_provider_config(req.tts_provider)
            req.voice = provider_cfg.get("voice", "")
        if not req.target_lang:
            req.target_lang = self.config.get("target_lang")
        await self._request_queue.put(req)
        if req.audio_samples is not None:
            logger.info("音频请求入队: %s", req.request_id)
        else:
            logger.info("请求入队: %s  text=%s", req.request_id, req.text[:40])
        return req.request_id

    async def _request_worker(self):
        while self._running:
            try:
                req = await self._request_queue.get()
                try:
                    if req.audio_samples is not None and self.stt is not None:
                        stt_result = await self.stt.transcribe(req.audio_samples, req.sample_rate)
                        if not stt_result.is_success or not stt_result.text:
                            logger.warning("STT 失败，跳过: %s", stt_result.error)
                            continue
                        req.text = stt_result.text
                        if req._stt_callback:
                            req._stt_callback(req.request_id, req.text)
                    if not req.text:
                        logger.warning("请求无文本内容，跳过: %s", req.request_id)
                        continue
                    await self._process(req)
                finally:
                    self._request_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("_request_worker 异常: %s", e)

    async def _process(self, req: PipelineRequest) -> None:
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
                    original_result = await self.tts.synthesize(req.text, provider=req.tts_provider, voice=req.voice)
                else:
                    logger.warning(f"{req.tts_provider} 不支持{req.source_lang}，自动使用 edge_tts")
                    edge_voice = _resolve_edge_voice(req.source_lang)
                    original_result = await self.tts.synthesize(req.text, provider="edge_tts", voice=edge_voice)
            except Exception as e:
                logger.exception(f"TTS(原文) 执行异常: {e}")
                original_result = TTSResult(success=False, text=req.text, error=str(e))

            if original_result.is_success and original_result.path:
                await self._play_queue.put(original_result.path)
            else:
                logger.error(f"TTS(原文) 失败: {original_result.error}")

        if not req.translate and req.osc_enabled:
            self.osc.send_original(req.text)

    async def _handle_translate_bg(self, req: PipelineRequest) -> None:
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
            except asyncio.CancelledError:
                break
            try:
                if path is None:
                    logger.debug("播放队列收到 None，跳过")
                    continue
                if path.exists():
                    device_name = self.config.get("device")
                    await play_file(path, device_name=device_name)
                else:
                    logger.warning(f"音频文件不存在，跳过播放: {path}")
                for _i in range(10):
                    try:
                        path.unlink(missing_ok=True)
                        break
                    except PermissionError:
                        await asyncio.sleep(0.05)
                else:
                    logger.warning("无法删除临时文件（可能被占用）: %s", path)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.exception(f"_play_worker 异常: {e}")
            finally:
                self._play_queue.task_done()
