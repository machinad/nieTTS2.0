import logging
import edge_tts as edge
from engines.base import BaseTTS, TTSResult

logger = logging.getLogger(__name__)


class EdgeTTS(BaseTTS):
    engine_name = "Edge TTS"

    def is_available(self) -> bool:
        return True

    async def synthesize(self, text: str, voice: str, **kwargs) -> TTSResult:
        save_path = self._make_path(".mp3")
        try:
            communicate = edge.Communicate(text, voice)
            await communicate.save(save_path)
            logger.info(f"Edge TTS 生成成功: {save_path}")
            return TTSResult(success=True, path=save_path, voice=voice, text=text)
        except Exception as e:
            logger.error(f"Edge TTS 生成失败: {e}")
            return TTSResult(success=False, voice=voice, text=text, error=str(e))
