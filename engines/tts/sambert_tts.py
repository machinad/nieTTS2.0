import asyncio
import logging
import dashscope
from dashscope.audio.tts import SpeechSynthesizer as SpeechSynthesizerV1
from engines.tts.base import BaseTTS, TTSResult

logger = logging.getLogger(__name__)


class SambertTTS(BaseTTS):
    engine_name = "阿里百炼Sambert"

    @classmethod
    def from_config(cls, cfg: dict, save_dir):
        return cls(save_dir, api_key=cfg.get("ali_api_key", ""))

    def __init__(self, save_dir, api_key: str = ""):
        super().__init__(save_dir)
        self.api_key = api_key
        self._lock = asyncio.Lock()

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def synthesize(self, text: str, voice: str, **kwargs) -> TTSResult:
        save_path = self._make_path(".mp3")
        try:
            async with self._lock:
                dashscope.api_key = self.api_key
                result = await asyncio.to_thread(
                    SpeechSynthesizerV1.call, model=voice, text=text,
                    sample_rate=48000, format="mp3",
                )
            audio_data = result.get_audio_data()
            if audio_data is not None:
                await asyncio.to_thread(save_path.write_bytes, audio_data)
                logger.info(f"Sambert TTS 生成成功: {save_path}")
                return TTSResult(success=True, path=save_path, voice=voice, text=text)
            else:
                return TTSResult(success=False, voice=voice, text=text, error="阿里百炼返回空数据")
        except Exception as e:
            logger.error(f"Sambert TTS 生成失败: {e}")
            return TTSResult(success=False, voice=voice, text=text, error=str(e))
