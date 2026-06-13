import copy
import json
import threading
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

default_config = {
    "tts_provider": {
        "provider":"edge_tts",
        "providers":[
            {
                "name": "edge_tts",
                "voice":"汉语女声-晓晓-新闻小说-温柔",
                "description": "免费微软官方TTS在线服务（在线API）"
            },
            {
                "name": "cosyvoice",
                "voice": "龙婉-普通话-语音助手、导航播报、聊天数字人",
                "ali_api_key": "",
                "description": "阿里百炼CosyVoice语音合成服务，支持情感控制、语音克隆等功能（需要API Key）"
            },
            {
                "name":"sambert",
                "voice":"知琪-温柔女声-通用场景",
                "ali_api_key": "",
                "description": "阿里百炼Sambert语音合成服务，适用于通用场景（需要API Key）"
            },
            {
                "name":"MatchaTTS",
                "voice":"0",
                "matcha_acoustic_model": "models/matcha-icefall-zh-en/model-steps-3.onnx",
                "matcha_vocoder": "models/vocos-16khz-univ.onnx",
                "matcha_tokens": "models/matcha-icefall-zh-en/tokens.txt",
                "matcha_lexicon": "models/matcha-icefall-zh-en/lexicon.txt",
                "matcha_data_dir": "models/matcha-icefall-zh-en",
                "matcha_dict_dir": "",
                "description": "本地离线TTS，完全本地推理无需网络（需要模型文件）"
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
                "description": "通义千问Qwen3本地离线语音识别，基于0.6B参数量化模型（需要模型文件）"
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
                "url": "",
                "description": "OpenAI兼容大语言模型翻译，支持任意OpenAI API格式的模型（需要API Key）"
            },
            {
                "name": "hy_mt15",
                "model_path": "models/HY-mt/Hy-MT2-1.8B-2Bit.gguf",
                "server_url": "http://127.0.0.1:8081",
                "llama_cpp_path": "llama-cpp",
                "description": "HY-MT1.5本地离线翻译模型，基于1.8B参数GGUF量化模型（需要模型文件）"
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
    "device": "",
    "source_lang": "中文",
    "target_lang": "英语",
    "isPlayAudio": True,
    "isTranslate": True,
    "isPlayTranslation": True,
    "osc_enabled": True,
    "osc_host": "127.0.0.1",
    "osc_port": 9000,
    "port": 11451,
    "overlay_hotkey": {
        "ctrl": True,
        "shift": False,
        "alt": False,
        "key": 84,
        "display": "Ctrl+T"
    },
}


class ConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
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
        self.llama_cpp_path = self.project_root / "llama-cpp"
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
        # 追加新增的 translation provider（兼容已有 config.json）
        disk_names = {p.get("name") for p in config["translation_provider"]["providers"]}
        for p in default_config["translation_provider"]["providers"]:
            if p.get("name") not in disk_names:
                config["translation_provider"]["providers"].append(copy.deepcopy(p))
        # 补充新增的 provider 字段（兼容已有 config.json）
        for provider_key in ["tts_provider", "stt_provider", "translation_provider"]:
            for provider in config[provider_key]["providers"]:
                if not provider.get("description"):
                    for dp in default_config[provider_key]["providers"]:
                        if dp.get("name") == provider.get("name") and dp.get("description"):
                            provider["description"] = dp["description"]
                            break
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
            elif key in target and isinstance(target[key], list) and isinstance(value, list):
                # providers 列表按 name 字段合并，避免只修改一个 provider 时丢失其他
                if value and isinstance(value[0], dict) and "name" in value[0]:
                    by_name = {p["name"]: p for p in target[key] if isinstance(p, dict) and "name" in p}
                    for item in value:
                        if isinstance(item, dict) and "name" in item:
                            if item["name"] in by_name:
                                self._deep_update(by_name[item["name"]], item)
                            else:
                                by_name[item["name"]] = item
                    target[key] = list(by_name.values())
                else:
                    target[key] = value
            else:
                target[key] = value

    def update(self, data):
        # 从 disk 重新加载最新 config，避免 GUI/Web 端互相覆盖
        fresh = copy.deepcopy(default_config)
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    disk = json.load(f)
                self._deep_update(fresh, disk)
            except Exception:
                pass
        # 在最新内容上应用本次修改
        self._deep_update(fresh, data)
        # 补充缺失的 provider 描述（兼容旧 config）
        for provider_key in ["tts_provider", "stt_provider", "translation_provider"]:
            if provider_key in fresh:
                for provider in fresh[provider_key].get("providers", []):
                    if not provider.get("description"):
                        for dp in default_config[provider_key]["providers"]:
                            if dp.get("name") == provider.get("name") and dp.get("description"):
                                provider["description"] = dp["description"]
                                break
        # 保存并更新内存
        self._save_file(fresh)
        # 验证写入结果
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                verify = json.load(f)
            if verify != fresh:
                logger.error("配置验证失败! 写入内容与内存不一致")
                self.config = fresh
                return False
            else:
                logger.info("配置已保存并验证通过 %s", self.config_file)
        except Exception as e:
            logger.error("配置验证读取失败: %s", e)
            self.config = fresh
            return False
        self.config = fresh
        return True
