import logging
logger = logging.getLogger(__name__)
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer as SpeechSynthesizerV2
from dashscope.audio.tts import SpeechSynthesizer as SpeechSynthesizerV1
import uuid
import config.default as config

class SamberTTS:
    def __init__(self,voice,prompt):
        self.config_manager = config.ConfigManager()
        self.voice = voice
        self.prompt = prompt
        self.path = self.config_manager.save_path
    async def use_samber_tts(self):
        model = self.voice
        Key = self.config_manager.get("ali_api_key")
        save_path = self.path / f"{uuid.uuid4()}.mp3"
        SamberTTS_tts_task = {
            "voice": self.voice,
            "prompt": self.prompt,
            "path": save_path,
            "status": "running"
        }
        try:
            if Key == "":
                logger.error("阿里百炼API密钥为空")
                SamberTTS_tts_task["status"] = "failed"
                return SamberTTS_tts_task
            dashscope.api_key = Key
            result = SpeechSynthesizerV1.call(model=model,text=self.prompt,sample_rate=48000,format='mp3')
        except Exception as e:
            logger.error(f"阿里百炼转换失败: {e}")
            SamberTTS_tts_task["status"] = "failed"
            return SamberTTS_tts_task
        if result.get_audio_data() is not None:
            with open(save_path, 'wb') as f:
                f.write(result.get_audio_data())
            SamberTTS_tts_task["status"] = "success"
            return SamberTTS_tts_task
        else:
            logger.error("阿里百炼转换失败")
            SamberTTS_tts_task["status"] = "failed"
            return SamberTTS_tts_task
