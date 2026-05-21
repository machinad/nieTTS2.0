# nieTTS 2.0 开发计划

## 项目概述

nieTTS 2.0 是一个 **TTS + 翻译 + 语音识别** 的综合 Web 应用，支持多引擎异步并行处理，目标场景为 VRChat 等 VR 社交平台的实时语音交互。

### 核心能力

- **TTS 合成**：Edge TTS / MatchaTTS / CosyVoice / Sambert 四引擎
- **翻译**：OpenAI 兼容 API（联网）/ HY-MT1.5 本地模型（离线）
- **语音识别**：sherpa-onnx SenseVoice + Silero VAD
- **OSC 集成**：直接发送文本到 VRChat ChatBox
- **Web 前端**：Vue 3 + Vite，TTS 控制 + 语音识别控制

---

## 架构总览

```
┌───────────────────────────────────────────────────────────────────────────┐
│                              nieTTS 2.0                                    │
│                                                                            │
│  ┌─────────┐   HTTP POST /tts    ┌──────────────────────────────────┐     │
│  │         │────返回 202────────▶│           WebServer (Quart)       │     │
│  │  Vue 3  │                    │                                    │     │
│  │  前端   │◀── WebSocket /ws ──│  路由:  POST /tts                  │     │
│  │         │   日志/状态 (出)    │        GET  /voices               │     │
│  │         │                    │        GET  /config               │     │
│  │         │── WebSocket /ws ──▶│        POST /config               │     │
│  │         │   音频流 (进)       │        WS   /ws                   │     │
│  └─────────┘                    └────────────┬─────────────────────┘     │
│                                              │                            │
│  ┌───────────────────────────────────────────┼──────────────────────┐     │
│  │                          RequestPipeline  │                       │     │
│  │                                           ▼                       │     │
│  │  ┌──────────────────┐          ┌──────────────────────┐          │     │
│  │  │  RequestQueue    │─────────▶│  _process() 串行      │          │     │
│  │  │  (asyncio.Queue) │          │                      │          │     │
│  │  │  FIFO, 串行消费   │          │  asyncio.gather ────┤          │     │
│  │  └──────────────────┘          │                      │          │     │
│  │                                │  ┌── TTS(原文) ───────────┐     │     │
│  │                                │  │                       │     │     │
│  │                                │  ├── [if translate]     │     │     │
│  │                                │  │     translate(文本)   │     │     │
│  │                                │  │       ├── TTS(译文)───┤     │     │
│  │                                │  │       └── OSC(原文\n  │     │     │
│  │                                │  │           译文)       │     │     │
│  │                                │  └── [else] OSC(原文)    │     │     │
│  │                                │           │             │     │     │
│  │                                └───────────┼─────────────┘     │     │
│  │                                            │                   │     │
│  │                          ┌─────────────────┴──────────────┐    │     │
│  │                          │  按序 push: 原文 → 译文          │    │     │
│  │                          └─────────────────┬──────────────┘    │     │
│  │                                            ▼                   │     │
│  │                          ┌────────────────────────────────┐    │     │
│  │                          │  PlayQueue (asyncio.Queue)     │    │     │
│  │                          │  FIFO, 纯播放                  │    │     │
│  │                          └───────────────┬────────────────┘    │     │
│  │                                          ▼                     │     │
│  │                          ┌────────────────────────────────┐    │     │
│  │                          │  PlayWorker (asyncio.Task)     │    │     │
│  │                          │  miniaudio, 播完清理临时文件     │    │     │
│  │                          └────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                   WebSocket 音频输入链路 (Phase 2)                 │     │
│  │                                                                   │     │
│  │  前端麦克风 ──WS──▶ 音频流(bytes) ──▶ VAD(Silero) ──▶ 完整句子   │     │
│  │                                                    │              │     │
│  │                                           ┌────────▼─────────┐    │     │
│  │                                           │ STT(SenseVoice)  │    │     │
│  │                                           │ 识别文本          │    │     │
│  │                                           └────────┬─────────┘    │     │
│  │                                                    │              │     │
│  │                                          文本送入 RequestQueue    │     │
│  │                                          （复用全部 TTS+翻译管道）  │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │                      引擎层                                   │          │
│  │                                                              │          │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────┐          │          │
│  │  │TTSService│  │TranslateSvc  │  │  STTService  │          │          │
│  │  │──────────│  │──────────────│  │──────────────│          │          │
│  │  │ EdgeTTS  │  │OpenAITranslate│  │SenseVoiceSTT │          │          │
│  │  │MatchaTTS │  │HY-MT1.5 (P3) │  │              │          │          │
│  │  │CosyVoice │  │              │  │              │          │          │
│  │  │Sambert   │  │              │  │              │          │          │
│  │  └──────────┘  └──────────────┘  └──────────────┘          │          │
│  │                                                              │          │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────┐          │          │
│  │  │  OSC     │  │  Audio       │  │  Config      │          │          │
│  │  │  客户端   │  │  playback    │  │  Manager     │          │          │
│  │  │ VRChat   │  │  miniaudio   │  │              │          │          │
│  │  └──────────┘  └──────────────┘  └──────────────┘          │          │
│  └─────────────────────────────────────────────────────────────┘          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 数据流详解

### TTS 请求（文本输入）

```
POST /tts { text, tts_provider, voice, translate:bool, play_translation:bool, osc_enabled:bool }
  │
  ├─ 1. WebServer 验证参数，立即返回 202 { request_id }
  │
  └─ 2. 提交到 RequestQueue
       │
       └─ 3. _process() 串行消费
            │
            ├─ asyncio.gather: ──────────────────────────┐
            │                                             │
            │   TTS(原文) ──▶ audio_original              │
            │                                             │
            │   [if translate]                            │
            │     translate(text) ──▶ translated_text     │
            │       ├── [if play_translation]            │
            │       │     TTS(译文) ──▶ audio_translated │
            │       └── [if osc]                         │
            │             OSC.send(原文 + "\n" + 译文)    │
            │                                             │
            │   [if !translate && osc]                    │
            │     OSC.send(原文)                          │
            │                                             │
            └────────────────────────────────────────────┘
            │
            └─ 4. 按序 push 到 PlayQueue:
                  #1 audio_original
                  #2 audio_translated (如有)
            │
            └─ 5. PlayWorker 按序播放，播完删除临时文件
```

### 语音识别请求（音频输入，Phase 2）

```
WebSocket /ws 接收音频流
  │
  ├─ 前端: navigator.mediaDevices.getUserMedia → WebSocket binary
  │
  └─ 后端: VAD 累积音频
       │
       └─ VAD 检测到完整句子
            │
            └─ STT 识别 → 文本
                 │
                 └─ 文本送入 RequestQueue ──▶ 同 TTS 管道
```

### WebSocket 协议

```
方向: 前端 → 后端
┌──────────┬──────────────────────────────────────┐
│ bytes    │ 音频数据 (Int16 44.1kHz mono)         │
│ str JSON │ { type: "start" | "stop" }           │
└──────────┴──────────────────────────────────────┘

方向: 后端 → 前端
┌──────────┬──────────────────────────────────────┐
│ str JSON │ { type: "log", level, message }      │
│ str JSON │ { type: "status", request_id, state }│
│ str JSON │ { type: "stt_result", text }         │
└──────────┴──────────────────────────────────────┘
```

---

## 模块职责

### `engines/pipeline.py` — RequestPipeline

核心调度器，管理两层队列。

```python
class RequestPipeline:
    request_queue: asyncio.Queue   # 请求队列（串行消费）
    play_queue: asyncio.Queue      # 播放队列（纯 FIFO）

    async def submit_tts(text, opts)    # 提交文本 TTS 请求
    async def submit_stt_text(text)     # 提交 STT 识别文本（复用管道）

    async def _request_worker()         # 后台: 串行消费请求队列
    async def _process(req)             # 单请求: 并行 TTS + 翻译, 推送 PlayQueue
    async def _play_worker()            # 后台: 消费 PlayQueue, miniaudio 播放
```

关键行为：
- RequestQueue 串行：处理完当前请求的所有音频才处理下一个
- PlayQueue push 保序：先原文、后译文
- 原文 TTS 和翻译并行执行（`asyncio.gather`）

### `engines/audio/playback.py` — 音频播放

```python
async def play_file(path: Path) -> None:
    """用 miniaudio 播放音频文件（内部 asyncio.to_thread 避免阻塞）"""
```

支持格式：WAV / MP3 / OGG / FLAC（miniaudio 原生支持，无需 ffmpeg）

### `engines/osc/service.py` — OSC 客户端

```python
class OSCService:
    def send(text: str)                 # 发送文本到 VRChat
    def send_combined(original, trans)  # 发送原文+译文拼接
```

目标：`127.0.0.1:9000`，路径：`/chatbox/input`，参数：`[text, True]`

### `web_server.py` — Quart Web 服务

```
POST /tts          → pipeline.submit_tts() → 202
GET  /voices       → TTSService.get_available_engines() + 音色列表
GET  /config       → ConfigManager.get()
POST /config       → ConfigManager.update()
WS   /ws           → 双向: 日志/状态(出) + 音频流(进, Phase 2)
```

---

## 分阶段计划

### Phase 1: TTS + 翻译核心管道 [当前]

| # | 文件 | 状态 | 任务 |
|---|---|---|---|
| 1.1 | `engines/translate/service.py` | 🚧 | `TranslateService` 引擎分发器 |
| 1.2 | `engines/audio/playback.py` | 🚧 | miniaudio 异步音频播放 |
| 1.3 | `engines/osc/service.py` | 🚧 | OSC VRChat ChatBox 客户端 |
| 1.4 | `engines/pipeline.py` | 🚧 | RequestPipeline: RequestQueue(串行) + PlayQueue(FIFO) + PlayWorker + OSC |
| 1.5 | `web_server.py` | 🚧 | Quart 路由 + WS 端点(日志下行) |
| 1.6 | `main.py` | 🚧 | nieTTS 类, 组装所有服务, 启动入口 |
| 1.7 | `frontend/` | 🚧 | Vue 3 + Vite 前端, TTS 控制面板 |

**Phase 1 交付**：`python main.py` → 浏览器 → 输入文字 → TTS 播报 + 翻译 + OSC

---

### Phase 2: 语音输入 (STT + VAD)

| # | 文件 | 状态 | 任务 |
|---|---|---|---|
| 2.1 | `engines/stt/vad/silero_vad.py` | ⏳ | SileroVAD (sherpa-onnx VoiceActivityDetector) |
| 2.2 | `engines/stt/sensevoice_stt.py` | ⏳ | SenseVoiceSTT (sherpa-onnx OfflineRecognizer) |
| 2.3 | `engines/stt/service.py` | ⏳ | STTService 分发器 |
| 2.4 | `web_server.py` (扩展) | ⏳ | WS 接收音频流 → VAD → STT |
| 2.5 | `frontend/` (扩展) | ⏳ | 麦克风采集 + WS 上传 + 识别结果展示 |

**Phase 2 交付**：前端开监听 → 说话 → 自动识别 → 翻译 → TTS 播报

---

### Phase 3: 扩展与完善

| # | 文件 | 状态 | 任务 |
|---|---|---|---|
| 3.1 | `engines/translate/hy_mt15_translate.py` | ⏳ | HY-MT1.5 本地翻译 (llama-server HTTP API) |
| 3.2 | `engines/audio/device.py` | ⏳ | 音频设备枚举 (sounddevice) |
| 3.3 | `pyproject.toml` | ⏳ | 包定义、依赖声明、入口点 |
| 3.4 | `frontend/` (完善) | ⏳ | 设备选择、音量指示器、亮暗主题 |
| 3.5 | `tests/` | ⏳ | 引擎层单元测试 |

---

## 最终文件结构

```
nieTTS2.0/
├── main.py                       # 入口: nieTTS 类, 组装启动
├── web_server.py                 # Quart 路由 + WS handler
├── pyproject.toml                # 包定义 (Phase 3)
├── PLAN.md                       # 本文件
│
├── config/
│   ├── default.py                # ConfigManager (单例, JSON 配置)
│   └── provider_voice.py         # 三引擎音色字典
│
├── engines/
│   ├── pipeline.py               # RequestPipeline 核心管道
│   │
│   ├── tts/
│   │   ├── base.py               # BaseTTS + TTSResult
│   │   ├── edge_tts.py           # Edge TTS (edge-tts 库)
│   │   ├── matcha_tts.py         # MatchaTTS (sherpa-onnx)
│   │   ├── cosyvoice_tts.py      # CosyVoice (dashscope)
│   │   ├── sambert_tts.py        # Sambert (dashscope)
│   │   └── service.py            # TTSService 分发器
│   │
│   ├── translate/
│   │   ├── base.py               # BaseTranslate + TranslateResult
│   │   ├── openai_translate.py   # OpenAI 兼容 API 翻译
│   │   ├── hy_mt15_translate.py  # HY-MT1.5 本地翻译 (Phase 3)
│   │   └── service.py            # TranslateService 分发器
│   │
│   ├── stt/
│   │   ├── base.py               # BaseSTT + STTResult
│   │   ├── sensevoice_stt.py     # SenseVoice 识别 (Phase 2)
│   │   ├── service.py            # STTService 分发器 (Phase 2)
│   │   └── vad/
│   │       ├── base.py           # BaseVAD + SpeechSegment
│   │       └── silero_vad.py     # Silero VAD 实现 (Phase 2)
│   │
│   ├── audio/
│   │   ├── playback.py           # miniaudio 异步播放
│   │   └── device.py             # 设备枚举 (Phase 3)
│   │
│   └── osc/
│       └── service.py            # OSCService VRChat 客户端
│
├── frontend/                     # Vue 3 + Vite 前端
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.ts
│       ├── App.vue
│       ├── components/
│       │   ├── TTSControl.vue    # TTS 控制面板
│       │   ├── VoiceInput.vue    # 麦克风输入 (Phase 2)
│       │   ├── SettingsPanel.vue # 配置面板
│       │   └── LogView.vue       # 日志显示
│       └── api/
│           ├── index.ts          # HTTP + WS 请求封装
│           └── types.ts          # TS 类型定义
│
├── certificates/
│   └── certificates_server.py   # 自签名 HTTPS 证书
│
├── templates/                    # Vue build 产物 (生产环境)
│
├── models/                       # 模型文件 (gitignored)
└── save/                         # 临时音频 (gitignored)
```

---

## 依赖

### 运行时

| 包 | 用途 |
|---|---|
| `quart` | 异步 Web 框架 |
| `edge-tts` | Edge TTS 引擎 |
| `dashscope` | 阿里百炼 CosyVoice + Sambert |
| `sherpa-onnx` | MatchaTTS + VAD + STT (Phase 2) |
| `openai` | OpenAI 兼容 API 翻译 |
| `miniaudio` | 音频播放 (替代 pygame) |
| `python-osc` | VRChat OSC 通信 |
| `sounddevice` | 音频设备枚举 (Phase 3) |
| `httpx` | HY-MT1.5 HTTP 客户端 (Phase 3) |

### 开发

| 包 | 用途 |
|---|---|
| `vue` + `vite` | 前端 |
| `pytest` | 测试 (Phase 3) |
