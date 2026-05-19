import json
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

default_config = {
    "provider": "Edge TTS",
    "edge_tts_voice": "汉语女声-晓晓-新闻小说-温柔",
    "device": "CABLE Input (VB-Audio Virtual Cable)",
    "ali_tts_voice": "",
    "sambert_tts_voice": "",
    "ali_api_key": "",
    "siliconflowApiKey": "",
    "tLanguage": "英语",
    "isdownload": False,
    "isplayaudio": True,
    "isTranslate": True,
    "isPlayTranslation": True
}


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True

        self.project_root = Path(__file__).parent.parent.resolve()
        self.config_dir = self.project_root / "config"
        self.models_path = self.project_root / "models"
        self.save_path = self.project_root / "save"
        self.templates_path = self.project_root / "templates"
        self.config_file = self.config_dir / "config.json"
        self._ensure_dirs()
        self.config = self._init_config()

    def _ensure_dirs(self):
        for p in [self.config_dir, self.models_path, self.save_path, self.templates_path]:
            p.mkdir(parents=True, exist_ok=True)

    def _init_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载配置失败: {e}")
        return self._create_default_config()

    def _create_default_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
        logger.info(f"已创建默认配置文件: {self.config_file}")
        return dict(default_config)

    def save_config(self, config=None):
        if config is None:
            config = self.config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False

    def get(self, key, default=None):
        return self.config.get(key, default)

    def update(self, data):
        self.config.update(data)
        return self.save_config()