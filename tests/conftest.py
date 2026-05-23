import sys
from pathlib import Path
import pytest
import tempfile
import numpy as np

# Ensure project root is on sys.path
_project_root = Path(__file__).parent.parent.resolve()
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


@pytest.fixture
def project_root():
    return _project_root


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def dummy_audio_samples():
    """Generate 1 second of silent 16kHz mono audio."""
    return np.zeros(16000, dtype=np.float32)


@pytest.fixture
def dummy_audio_stereo():
    """Generate 1 second of silent 16kHz stereo audio."""
    return np.zeros((16000, 2), dtype=np.float32)


@pytest.fixture
def dummy_audio_int16():
    """Generate 1 second of int16 audio."""
    return np.zeros(16000, dtype=np.int16)


@pytest.fixture
def sample_config_dict():
    return {
        "tts_provider": {
            "provider": "edge_tts",
            "providers": [
                {"name": "edge_tts", "voice": "zh-CN-XiaoxiaoNeural"},
                {"name": "cosyvoice", "voice": "longwan"},
                {"name": "sambert", "voice": "zhiqi"},
                {"name": "MatchaTTS", "voice": "0",
                 "matcha_acoustic_model": "models/test.onnx",
                 "matcha_vocoder": "models/test.onnx",
                 "matcha_tokens": "models/test.txt",
                 "matcha_lexicon": "models/test.txt",
                 "matcha_data_dir": "models",
                 "matcha_dict_dir": ""},
            ],
        },
        "stt_provider": {
            "provider": "Qwen3",
            "providers": [
                {"name": "Qwen3",
                 "conv_frontend": "models/test.onnx",
                 "encoder": "models/test.onnx",
                 "decoder": "models/test.onnx",
                 "tokenizer": "models/tokenizer"},
            ],
        },
        "translation_provider": {
            "provider": "openai",
            "providers": [{"name": "openai", "model": "", "api_key": "", "url": ""}],
        },
        "ali_api_key": "test-key",
        "vad": {
            "model_path": "models/silero_vad.onnx",
            "sample_rate": 16000,
            "threshold": 0.5,
            "min_silence_duration": 0.25,
            "min_speech_duration": 0.25,
            "max_speech_duration": 15.0,
            "window_size": 512,
        },
    }
