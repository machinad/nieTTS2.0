import copy
import json
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

default_config = {
    "tts_provider": {
        "provider":"edge_tts",
        "providers":[
            {
                "name": "edge_tts",
                "voice":"汉语女声-晓晓-新闻小说-温柔"
            },
            {
                "name": "cosyvoice",
                "voice": "龙婉-普通话-语音助手、导航播报、聊天数字人"
            },
            {
                "name":"sambert",
                "voice":"知琪-温柔女声-通用场景"
            },
            {
                "name":"MatchaTTS",
                "voice":"0",
                "matcha_acoustic_model": "models/matcha-icefall-zh-en/model-steps-3.onnx",
                "matcha_vocoder": "models/vocos-16khz-univ.onnx",
                "matcha_tokens": "models/matcha-icefall-zh-en/tokens.txt",
                "matcha_lexicon": "models/matcha-icefall-zh-en/lexicon.txt",
                "matcha_data_dir": "models/matcha-icefall-zh-en",
                "matcha_dict_dir": ""
            }

        ]
    },
    "stt_provider": {
        "provider":"Qwen3",
        "providers":[
            {
                "name": "Qwen3",
                "conv_frontend": "models/qwen3-asr-0.6B-int8/conv_frontend.onnx",
                "encoder": "models/qwen3-asr-0.6B-int8/encoder.int8.onnx",
                "decoder": "models/qwen3-asr-0.6B-int8/decoder.int8.onnx",
                "tokenizer": "models/qwen3-asr-0.6B-int8/tokenizer",
            }
        ]
    },
    "translation_provider": {
        "provider":"openai",
        "providers":[
            {
                "name": "openai",
                "model": "",
                "api_key": "",
                "url": ""
            },
        ]
    },
    "vad": {
        "model_path": "models/silero_vad.onnx",
        "sample_rate": 16000,
        "threshold": 0.5,
        "min_silence_duration": 0.25,
        "min_speech_duration": 0.25,
        "max_speech_duration": 15.0,
        "window_size": 512,
    },
    "device": "CABLE Input (VB-Audio Virtual Cable)",
    "ali_api_key": "",
    "tLanguage": "英语",
    "isPlayAudio": True,
    "isTranslate": True,
    "isPlayTranslation": True,
    "osc_enabled": True,
    "osc_host": "127.0.0.1",
    "osc_port": 9000,
}


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
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
        config = copy.deepcopy(default_config)
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    disk = json.load(f)
                self._deep_update(config, disk)
            except Exception as e:
                logger.error(f"加载配置失败: {e}")
        self._save_file(config)
        return config

    def _create_default_config(self):
        return copy.deepcopy(default_config)

    def _save_file(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def save_config(self, config=None):
        if config is None:
            config = self.config
        try:
            self._save_file(config)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_provider_config(self, name):
        providers = self.config.get("tts_provider", {}).get("providers", [])
        for p in providers:
            if p.get("name") == name:
                return p
        return {}

    def get_stt_provider_config(self, name):
        providers = self.config.get("stt_provider", {}).get("providers", [])
        for p in providers:
            if p.get("name") == name:
                return p
        return {}

    def get_translation_provider_config(self, name):
        providers = self.config.get("translation_provider", {}).get("providers", [])
        for p in providers:
            if p.get("name") == name:
                return p
        return {}

    def _deep_update(self, target, source):
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def update(self, data):
        self._deep_update(self.config, data)
        return self.save_config()