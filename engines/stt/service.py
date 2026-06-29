import asyncio
import logging

from config.default import ConfigManager
from engines.stt.base import BaseSTT, STTResult
from engines.stt.qwen3_stt import Qwen3STT

logger = logging.getLogger(__name__)

_REGISTRY: dict[str, type[BaseSTT]] = {
    "Qwen3": Qwen3STT,
}


class STTService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self._build_engines()
        self._close_task: asyncio.Task | None = None
        self._close_delay = 30  # 30秒后关闭

    def _build_engines(self):
        providers = self.config.get("stt_provider", {}).get("providers", [])
        self._engines: dict[str, BaseSTT] = {}
        for p in providers:
            name = p.get("name", "")
            cls = _REGISTRY.get(name)
            if cls is None:
                continue
            try:
                self._engines[name] = cls.from_config(p)
            except Exception as e:
                logger.warning("%s STT init skipped: %s", name, e)

    def get_available_engines(self) -> list[str]:
        return [n for n, e in self._engines.items() if e.is_available()]

    def get_all_engines(self) -> list[str]:
        providers = self.config.get("stt_provider", {}).get("providers", [])
        return [p["name"] for p in providers if p.get("name")]

    def get_engine_descriptions(self) -> dict[str, str]:
        providers = self.config.get("stt_provider", {}).get("providers", [])
        return {p["name"]: p.get("description", "") for p in providers if p.get("name")}

    async def reload_engines(self):
        self._cancel_close_timer()
        for eng in self._engines.values():
            await eng.close()
        self._build_engines()

    async def close(self):
        """立即关闭所有引擎"""
        self._cancel_close_timer()
        for eng in self._engines.values():
            try:
                await eng.close()
            except Exception:
                pass
        logger.info("STT 服务已关闭")

    def schedule_close(self):
        """调度延迟关闭（录音停止后30秒）"""
        self._cancel_close_timer()
        self._close_task = asyncio.create_task(self._delayed_close())
        logger.info("STT 服务将在 %d 秒后关闭", self._close_delay)

    def _cancel_close_timer(self):
        """取消延迟关闭定时器"""
        if self._close_task and not self._close_task.done():
            self._close_task.cancel()
            self._close_task = None

    async def _delayed_close(self):
        """延迟关闭协程"""
        try:
            await asyncio.sleep(self._close_delay)
            await self.close()
        except asyncio.CancelledError:
            pass  # 定时器被取消，正常情况

    async def transcribe(self, samples, sample_rate: int = 16000, provider: str = "") -> STTResult:
        self._cancel_close_timer()  # 使用时取消关闭定时器
        provider = provider or self.config.get("stt_provider.provider", "")
        if not provider:
            available = self.get_available_engines()
            provider = available[0] if available else ""
        engine = self._engines.get(provider)
        if engine is None:
            return STTResult(success=False, error=f"Unknown STT engine: {provider}")
        if not engine.is_available():
            return STTResult(success=False, error=f"Engine {provider} not available")
        return await engine.transcribe(samples, sample_rate)
