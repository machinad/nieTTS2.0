import logging
logger = logging.getLogger(__name__)
import edge_tts as edge
import uuid
import os
import config.default as config
class EdgeTTS:
    def __init__(self,voice,prompt):
        self.voice = voice
        self.prompt = prompt
        self.path = config.ConfigManager().save_path
    async def use_edge_tts(self):
        save_path = self.path / f"{uuid.uuid4()}.mp3"
        edge_tts_task = {
            "voice": self.voice,
            "prompt": self.prompt,
            "path": save_path,
            "status": "running"
        }
        try:
            communicate = edge.Communicate(self.prompt, self.voice)
            await communicate.save(save_path)
            edge_tts_task["status"] = "success"
            edge_tts_task["path"] = save_path
            logging.info(f"Edge TTS 生成成功: {save_path}")
            return edge_tts_task
        except Exception as e:
            logging.error(f"Edge TTS 生成失败: {e}")
            edge_tts_task["status"] = "failed"
            return edge_tts_task