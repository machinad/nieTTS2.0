# nieTTS 2.0 API Contract (v2.1.2)

## 基础信息

- Base URL: `https://<host>:11451` (自签名证书)
- Content-Type: `application/json`
- WebSocket: `wss://<host>:11451/ws`

---

## 1. GET /voices

返回所有可用引擎和音色。

### Response (200)
```json
{
  "tts_engines": ["edge_tts"],
  "all_tts_engines": ["edge_tts", "cosyvoice", "sambert", "MatchaTTS"],
  "translate_engines": [],
  "stt_engines": [],
  "voices": {
    "edge_tts": ["zh-CN-XiaoxiaoNeural", "en-US-AriaNeural", "ja-JP-NanamiNeural", ...],
    "cosyvoice": ["龙婉-普通话-语音助手...", ...],
    "sambert": ["知琪-温柔女声-通用场景", ...],
    "MatchaTTS": ["0"]
  },
  "source_languages": ["中文", "英语", "日语"],
  "target_languages": ["英语"]
}
```

---

## 2. GET /config

返回当前完整配置和设备列表。

### Response (200)
```json
{
  "tts_provider": { "provider": "edge_tts", "providers": [...] },
  "stt_provider": { "provider": "Qwen3", "providers": [...] },
  "translation_provider": { ... },
  "device": "Headphones (...)",
  "tLanguage": "英语",
  "isplayaudio": true,
  "isTranslate": true,
  "isPlayTranslation": true,
  "osc_enabled": true,
  "osc_host": "127.0.0.1",
  "osc_port": 9000,
  "vad": { "threshold": 0.5, "sample_rate": 16000, ... },
  "available_devices": [
    { "name": "Headphones (...)" },
    { "name": "CABLE Input (...)" }
  ]
}
```

---

## 3. POST /config

更新配置（支持部分更新，deep merge）。

### Request
```json
{
  "tLanguage": "日语",
  "tts_provider": { "provider": "edge_tts" }
}
```

### Response (200)
```json
{ "success": true }
```

### Response (400)
```json
{ "error": "无效的配置数据" }
```

---

## 4. POST /tts

提交 TTS 合成请求，异步处理，返回 request_id。

### Request
```json
{
  "text": "你好世界",
  "tts_provider": "edge_tts",
  "voice": "zh-CN-XiaoxiaoNeural",
  "translate": true,
  "play_audio": true,
  "play_translation": true,
  "osc_enabled": true,
  "source_lang": "中文",
  "target_lang": "英语"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| text | string | 是 | 1-5000 字符 |
| tts_provider | string | 否 | 默认 "edge_tts" |
| voice | string | 否 | 默认从配置读取 |
| translate | bool | 否 | 默认 true |
| play_audio | bool | 否 | 默认 true |
| play_translation | bool | 否 | 默认 true |
| osc_enabled | bool | 否 | 默认 true |
| source_lang | string | 否 | 默认 "中文" |
| target_lang | string | 否 | 默认从配置读取 |

### Response (202)
```json
{ "request_id": "abc123def456" }
```

### Response (400)
```json
{ "error": "文本内容不能为空" }
```

---

## 5. WS /ws

WebSocket 音频流传输端点。

### 客户端 → 服务端

**JSON 消息：**
```json
{ "type": "start" }   // 开始音频流
{ "type": "stop" }    // 结束音频流，触发 VAD flush + STT
```

**二进制消息：** int16 PCM 音频数据 (16kHz mono)，每帧约 3200 bytes (100ms)

### 服务端 → 客户端

```json
{ "type": "stt_result", "text": "转写结果文本" }
{ "type": "status", "request_id": "abc123", "state": "queued" }
```

### 交互流程

```
Client                    Server
  |                          |
  |── WS connect ──────────>|
  |── {"type":"start"} ────>|  ← 开始音频采集
  |── <binary audio chunk>──>|  ← 持续发送 PCM 数据
  |── <binary audio chunk>──>|
  |── {"type":"stop"} ─────>|  ← 结束，flush VAD
  |<── {"type":"stt_result",|  ← STT 识别结果
  |       "text":"..."} ────|
```

### 断开重连

WebSocket 断开后应自动重连（建议 3 秒延迟）。

---

## 错误响应通用格式

```json
{ "error": "错误描述信息" }
```

HTTP 状态码：
- 200: 成功
- 202: TTS 请求已入队
- 400: 请求参数错误
- 404: 资源不存在
