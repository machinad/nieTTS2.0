import edge_tts_server
import cosyvoice_tts_server
import samber_tts_server
from config.default import ConfigManager
from config.provider_voice import Edge_TTS_voices, ali_tts_voices, sambert_tts_voices
class tts_server:
    def __init__(self,Provider,Prompt):
        self.provider = Provider
        self.prompt = Prompt
        self.config_manager = ConfigManager()
    async def use_tts_server(self):
        if self.provider == "Edge TTS":
            return await edge_tts_server.EdgeTTS(voice=Edge_TTS_voices.get(self.config_manager.get("edge_tts_voice")), prompt=self.prompt).use_edge_tts()
        if self.provider == "阿里百炼cosyvoice":
            return await cosyvoice_tts_server.CosyVoiceTTS(voice=ali_tts_voices.get(self.config_manager.get("ali_tts_voice")), prompt=self.prompt).use_cosyvoice_tts()
        if self.provider == "阿里百炼Sambert":
            return await samber_tts_server.SamberTTS(voice=sambert_tts_voices.get(self.config_manager.get("sambert_voice")), prompt=self.prompt).use_samber_tts()