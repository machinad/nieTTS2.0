import asyncio
import logging
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer as SpeechSynthesizerV2
from engines.tts.base import BaseTTS, TTSResult

logger = logging.getLogger(__name__)


class CosyVoiceTTS(BaseTTS):
    engine_name = "阿里百炼cosyvoice"

    def __init__(self, save_dir, api_key: str = ""):
        super().__init__(save_dir)
        self.api_key = api_key

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def synthesize(self, text: str, voice: str, **kwargs) -> TTSResult:
        save_path = self._make_path(".mp3")
        try:
            dashscope.api_key = self.api_key
            synthesizer = SpeechSynthesizerV2(model="cosyvoice-v1", voice=voice)
            audio = await asyncio.to_thread(synthesizer.call, text)
            await asyncio.to_thread(save_path.write_bytes, audio)
            logger.info(f"CosyVoice TTS 生成成功: {save_path}")
            return TTSResult(success=True, path=save_path, voice=voice, text=text)
        except Exception as e:
            logger.error(f"CosyVoice TTS 生成失败: {e}")
            return TTSResult(success=False, voice=voice, text=text, error=str(e))
