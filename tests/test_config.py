import copy
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from config.default import ConfigManager, default_config


class TestConfigManager:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset ConfigManager singleton between tests."""
        ConfigManager._instance = None

    @pytest.fixture
    def clean_cm(self):
        """ConfigManager with pure defaults (ignore disk config.json merge)."""
        ConfigManager._instance = None
        cm = ConfigManager()
        cm.config = copy.deepcopy(default_config)
        return cm

    def test_singleton(self):
        cm1 = ConfigManager()
        cm2 = ConfigManager()
        assert cm1 is cm2

    def test_default_config_values(self, clean_cm):
        assert clean_cm.get("tts_provider.provider") == "edge_tts"
        assert clean_cm.get("stt_provider.provider") == "Qwen3"
        assert clean_cm.get("translation_provider.provider") == "openai"
        assert clean_cm.get("vad.threshold") == 0.3
        assert clean_cm.get("vad.sample_rate") == 16000

    def test_get_with_dot_notation(self, clean_cm):
        assert clean_cm.get("vad") == default_config["vad"]
        assert clean_cm.get("stt_provider") == default_config["stt_provider"]

    def test_get_with_default(self):
        cm = ConfigManager()
        assert cm.get("nonexistent.key", "default") == "default"
        assert cm.get("nonexistent.key") is None

    def test_get_provider_config(self, clean_cm):
        edge_cfg = clean_cm.get_provider_config("edge_tts")
        assert edge_cfg["name"] == "edge_tts"
        assert "voice" in edge_cfg

    def test_get_provider_config_unknown(self):
        cm = ConfigManager()
        assert cm.get_provider_config("nonexistent") == {}

    def test_get_stt_provider_config(self, clean_cm):
        qwen_cfg = clean_cm.get_stt_provider_config("Qwen3")
        assert qwen_cfg["name"] == "Qwen3"
        assert "conv_frontend" in qwen_cfg

    def test_get_stt_provider_config_unknown(self):
        cm = ConfigManager()
        assert cm.get_stt_provider_config("nonexistent") == {}

    def test_get_translation_provider_config(self, clean_cm):
        openai_cfg = clean_cm.get_translation_provider_config("openai")
        assert openai_cfg["name"] == "openai"

    def test_get_translation_provider_config_unknown(self):
        cm = ConfigManager()
        assert cm.get_translation_provider_config("nonexistent") == {}

    def test_deep_update_merges_nested(self):
        cm = ConfigManager()
        cm._deep_update(cm.config, {
            "vad": {"threshold": 0.8},
            "new_key": "new_value",
        })
        assert cm.get("vad.threshold") == 0.8
        # Other VAD keys preserved
        assert cm.get("vad.sample_rate") == 16000
        assert cm.get("new_key") == "new_value"

    def test_project_root(self):
        cm = ConfigManager()
        assert cm.project_root.exists()
        assert (cm.project_root / "config").exists()

    def test_ensure_dirs_creates_directories(self, temp_dir):
        cm = ConfigManager()
        cm.config_dir = temp_dir / "cfg"
        cm.models_path = temp_dir / "models"
        cm.save_path = temp_dir / "save"
        cm.templates_path = temp_dir / "tpl"
        cm._ensure_dirs()
        assert cm.config_dir.exists()
        assert cm.models_path.exists()
        assert cm.save_path.exists()
        assert cm.templates_path.exists()
