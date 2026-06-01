# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

nieTTS 2.0 — a TTS + Translation + STT web application for VR social platforms (primarily VRChat). Python async backend (Quart) with Vue 3 + TypeScript frontend. Licensed Apache 2.0.

## Commands

### Run the application
```bash
python main.py
```
Starts HTTPS server on port 11451 with self-signed certs.

### Build frontend
```bash
cd frontend
npm install
npm run build    # vue-tsc --noEmit && vite build → outputs to ../templates/
```

### Frontend dev server
```bash
cd frontend
npm run dev      # Vite dev server
```

### Run tests
```bash
python -m pytest tests/ -v --tb=short
python -m pytest tests/test_integration_pipeline.py -v -m integration --tb=long -s
```

Test config (`pytest.ini`): `asyncio_mode = auto`, `pythonpath = .`, marker `integration` for E2E pipeline tests.

### Package management
Uses `uv` (lockfile: `uv.lock`, venv: `.venv/`). No `pyproject.toml` or `requirements.txt` at root.

## Architecture

### Entry Point & Service Assembly (`main.py`)
The `nieTTS` class wires all services together. On startup it creates:
- `ConfigManager` (singleton) → `TTSService`, `TranslateService`, `STTService`, `OSCService` → `RequestPipeline` → `WebServer` + `CertificateServer`

### Engine Layer Pattern (`engines/`)
Each domain (TTS, Translate, STT) follows the same pattern:
- **Base ABC** with `is_available()`, `engine_name` property, and the main method (`synthesize`/`translate`/`transcribe`)
- **Concrete implementations** — one file per provider, all use `from_config(cfg, ...)` classmethod factory
- **Service class** — registry-based dispatcher (`_REGISTRY` dict) that selects and invokes the right engine
- **Result dataclass** — `TTSResult`, `TranslateResult`, `STTResult`, `SpeechSegment`

To add a new engine: create a file in the domain subfolder, implement the base ABC, register it in the service's `_REGISTRY`.

### Pipeline (`engines/pipeline.py`)
`RequestPipeline` uses two async FIFO queues:
1. **RequestQueue** — serial TTS processing (one request at a time)
2. **PlayQueue** — sequential audio playback via `miniaudio`

Per-request: TTS on original text + translation in parallel → translation triggers second TTS + OSC → audio files queued for playback in order → temp files deleted after play.

### Web Server (`web_server.py`)
Quart async server with CORS. Key routes: `GET /` (SPA), `POST /tts`, `GET/POST /config`, `WS /ws`, `GET /assets/<path>`. WebSocket handles log broadcast, audio stream input for STT (binary PCM), and VAD processing. `WSLogHandler` pushes Python logs to all connected WS clients.

### Frontend (`frontend/`)
Vue 3 + Element Plus + TypeScript SPA. Vite builds to `templates/`. State via `reactive()` store (`store.ts`), WebSocket with auto-reconnect (`ws.ts`), HTTP API layer (`api.ts`). Views: Home (TTS control), Settings, Logs, About.

### Configuration (`config/`)
`ConfigManager` singleton: deep-merges defaults (`default_config`) with disk config (`config/config.json`). Dot-notation access: `config.get("tts_provider.provider")`. Voice mappings in `provider_voice.py`.

## Key Conventions

- **Language**: Comments, log messages, config descriptions, and UI text are in **Chinese** (Simplified)
- **Async-first**: All services use `async/await`. Blocking ops wrapped in `asyncio.to_thread()`
- **Registry pattern**: Each service maps engine names → classes via `_REGISTRY`
- **`from_config` factory**: All engines instantiate from `from_config(cfg, ...)` classmethod
- **Singleton config**: `ConfigManager` uses `__new__` pattern
- **Temp files**: Audio output in `save/`, cleaned up after playback
- **No formal packaging**: Project runs directly via `python main.py`
