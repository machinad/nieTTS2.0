# nieTTS 2.0

> An all-in-one TTS + Translation + STT desktop application for VR social platforms

English | [中文](README.md)

## Introduction

nieTTS 2.0 is a desktop application designed for VR social platforms (such as VRChat), integrating Text-to-Speech (TTS), Speech-to-Text (STT), and translation capabilities. It supports multiple online and offline engines, provides a PySide6 desktop GUI and a Vue 3 web interface, and can seamlessly integrate with VRChat via the OSC protocol.

**Current Version**: v2.1.2  
**Platform Support**: Windows

## Features

### Text-to-Speech (TTS)

| Engine | Type | Description |
|--------|------|-------------|
| **Edge TTS** | Online | Microsoft's official free TTS service with 40+ Chinese voices, no API key required |
| **CosyVoice** | Online | Alibaba Bailian CosyVoice, supports emotion control and voice cloning |
| **Sambert** | Online | Alibaba Bailian Sambert, general-purpose |
| **MatchaTTS** | Offline | Fully local inference, Chinese-English bilingual, based on sherpa-onnx |

### Speech-to-Text (STT)

| Engine | Type | Description |
|--------|------|-------------|
| **Qwen3 ASR** | Offline | Alibaba Qwen3 local offline speech recognition, 0.6B parameters INT8 quantized |

### Translation

| Engine | Type | Description |
|--------|------|-------------|
| **OpenAI Compatible** | Online | Supports any OpenAI API format LLM |
| **HY-MT1.5** | Offline | Tencent Hunyuan local offline translation, 1.8B parameters GGUF quantized model |

### Other Features

- **VAD Voice Detection**: Silero VAD for precise speech onset/offset detection
- **OSC Communication**: VRChat chatbox integration, auto-sends synthesized text
- **Overlay**: Semi-transparent floating window, summoned via global hotkey (Ctrl+T)
- **Audio Playback**: Supports WAV/MP3/OGG/FLAC/OPUS formats with selectable playback devices
- **Request Pipeline**: Dual async queues, parallel translation and TTS execution
- **Multi-language Support**: 15 languages including Chinese, English, Japanese, Korean, French, German, etc.

## Installation

### Prerequisites

- Python 3.14.2
- Node.js (for building the frontend)

### Install with uv (Recommended)

```bash
# 1. Install uv
pip install uv

# 2. Clone the project
git clone https://github.com/machinad/nieTTS2.0.git
cd nieTTS2.0

# 3. Install Python dependencies
uv sync

# 4. Install frontend dependencies
cd frontend
npm install
cd ..
```

### Install with pip

```bash
# Clone the project
git clone https://github.com/machinad/nieTTS2.0.git
cd nieTTS2.0

# Install dependencies
pip install -e .

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Launch

### GUI Mode (Recommended)

```bash
python gui_main.py
# or
uv run python gui_main.py
```

After launch, a desktop application will open with the following pages:
- **Home**: Text input, language selection, engine status, voice input
- **Settings**: Engine configuration, audio devices, OSC settings, model download
- **Logs**: Real-time log viewer
- **About**: Version information

### Headless Mode

```bash
python main.py
# or
uv run python main.py
```

Only starts the web service (default port 11451), access the web interface via browser.

### Frontend Development

```bash
cd frontend
npm run dev      # Start Vite dev server
npm run build    # Build to ../templates/
npm run preview  # Preview build result
```

## Model Download

Some engines require downloading model files before use. Two download methods are available:

### Method 1: In-App Download (Recommended)

After launching the GUI, go to **Settings → Model Download** tab:
- Select download source (HuggingFace / HuggingFace Mirror / ModelScope)
- Click the "Start Download" button
- View download progress for each engine's models

### Method 2: Command Line Download

```bash
# Download all missing models
python scripts/download_models.py download

# Check all model status
python scripts/download_models.py check

# Quick check (skip SHA256 verification)
python scripts/download_models.py check --fast

# Download specific engine model
python scripts/download_models.py download --engine matcha_tts

# Force re-download
python scripts/download_models.py download --force
```

### Download Sources

| Source | Description | Recommended For |
|--------|-------------|-----------------|
| `huggingface` | HuggingFace official | International users |
| `huggingface_mirror` | HuggingFace mirror (hf-mirror.com) | China users (default) |
| `modelscope` | ModelScope | China users |

```bash
# Specify download source
python scripts/download_models.py download --source modelscope
```

### Supported Models

| Engine | Model | Size | Purpose |
|--------|-------|------|---------|
| Silero VAD | `silero_vad.onnx` | ~2.2 MB | Voice Activity Detection |
| MatchaTTS | `matcha-icefall-zh-en/` | ~130 MB | Local TTS |
| Qwen3 ASR | `qwen3-asr-0.6B-int8/` | ~1 GB | Local STT |
| HY-MT2 | `Hy-MT2-1.8B-2Bit.gguf` | ~600 MB | Local Translation |

## Build from Source

### Frontend Build

```bash
cd frontend
npm install
npm run build    # Output to ../templates/
```

### PyInstaller Packaging

```bash
# Full packaging
python build.py

# Build frontend first, then package
python build.py --frontend

# Clean build directory and repackage
python build.py --clean
```

Output file: `dist/nieTTS/nieTTS.exe`

## Third-Party Acknowledgements

This project uses the following open-source projects. Special thanks to their developers:

### Core Runtime

| Project | License | Purpose | Link |
|---------|---------|---------|------|
| **sherpa-onnx** | Apache-2.0 | Local inference engine for MatchaTTS, Qwen3 ASR, Silero VAD | [GitHub](https://github.com/k2-fsa/sherpa-onnx) |
| **edge-tts** | MIT | Microsoft Edge TTS online service Python wrapper | [GitHub](https://github.com/rany2/edge-tts) |
| **dashscope** | Apache-2.0 | Alibaba Bailian SDK for CosyVoice, Sambert | [GitHub](https://github.com/dashscope/dashscope-sdk-python) |
| **openai** | Apache-2.0 | OpenAI API Python client | [GitHub](https://github.com/openai/openai-python) |
| **numpy** | BSD-3-Clause | Numerical computing, audio data processing | [GitHub](https://github.com/numpy/numpy) |
| **miniaudio** | Unlicense | Audio playback library | [GitHub](https://github.com/mackron/miniaudio) |
| **python-osc** | MIT | OSC protocol implementation for VRChat communication | [GitHub](https://github.com/attwad/python-osc) |
| **httpx** | BSD-3-Clause | HTTP client | [GitHub](https://github.com/encode/httpx) |

### Web Service

| Project | License | Purpose | Link |
|---------|---------|---------|------|
| **quart** | MIT | Async web framework (async Flask) | [GitHub](https://github.com/pallets/quart) |
| **quart-cors** | MIT | Quart CORS support | [GitHub](https://github.com/pallets/quart-cors) |
| **cryptography** | Apache-2.0/BSD-3-Clause | Self-signed HTTPS certificate generation | [GitHub](https://github.com/pyca/cryptography) |

### GUI

| Project | License | Purpose | Link |
|---------|---------|---------|------|
| **PySide6** | LGPL-3.0 | Qt6 Python bindings | [Website](https://wiki.qt.io/Qt_for_Python) |
| **qasync** | BSD-2-Clause | Qt + asyncio event loop bridge | [GitHub](https://github.com/gmarull/qasync) |

### Frontend

| Project | License | Purpose | Link |
|---------|---------|---------|------|
| **Vue 3** | MIT | Progressive JavaScript framework | [GitHub](https://github.com/vuejs/core) |
| **Vue Router 4** | MIT | Vue.js official router | [GitHub](https://github.com/vuejs/router) |
| **Element Plus** | MIT | Vue 3 UI component library | [GitHub](https://github.com/element-plus/element-plus) |
| **Vite** | MIT | Next generation frontend build tool | [GitHub](https://github.com/vitejs/vite) |

### Model Download

| Project | License | Purpose | Link |
|---------|---------|---------|------|
| **huggingface-hub** | Apache-2.0 | HuggingFace model download | [GitHub](https://github.com/huggingface/huggingface_hub) |
| **modelscope** | Apache-2.0 | ModelScope model download | [GitHub](https://github.com/modelscope/modelscope) |

### Development Tools

| Project | License | Purpose | Link |
|---------|---------|---------|------|
| **pytest** | MIT | Python testing framework | [GitHub](https://github.com/pytest-dev/pytest) |
| **pytest-asyncio** | Apache-2.0 | pytest async test support | [GitHub](https://github.com/pytest-dev/pytest-asyncio) |
| **PyInstaller** | GPL-2.0 | Python program packaging | [GitHub](https://github.com/pyinstaller/pyinstaller) |

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Thanks to all the developers of the open-source projects that made nieTTS 2.0 possible.
