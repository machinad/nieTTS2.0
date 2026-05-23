# nieTTS 2.0 前端重构规格书 v2

## 1. 项目概述

nieTTS 是 TTS + STT + 翻译一体化工具。
- **后端**: Python Quart + Hypercorn, `https://0.0.0.0:11451`（自签名证书）
- **前端**: SPA, Vite 构建到 `templates/`，Quart 直接服务
- **访问**: 浏览器 `https://localhost:11451`

---

## 2. 技术栈

| 层面 | 选择 | 说明 |
|------|------|------|
| 框架 | Vue 3 + Composition API + `<script setup>` | |
| 构建 | Vite | `outDir: "../templates"` |
| UI 库 | **Element Plus** | 组件前缀 `El` |
| 图标 | `@element-plus/icons-vue` | |
| 路由 | vue-router (hash mode) | |
| 语言 | TypeScript | |
| HTTP | fetch | |

**Element Plus 关键组件**: `ElMenu`, `ElInput`, `ElButton`, `ElSelect`, `ElSwitch`, `ElTabs`, `ElTabPane`, `ElTag`, `ElCard`, `ElCollapse`, `ElCollapseItem`, `ElMessage`, `ElTooltip`, `ElBadge`, `ElDrawer`

**Vite 配置** (`frontend/vite.config.ts`):
```ts
import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import ElementPlus from "unplugin-element-plus/vite"

export default defineConfig({
  plugins: [vue(), ElementPlus()],
  base: "/",
  build: {
    outDir: "../templates",
    emptyOutDir: true,
  },
})
```

> `unplugin-element-plus` 实现按需导入样式，不用手动 import CSS。

---

## 3. 布局架构

### 整体结构

```
┌──────────────┬──────────────────────────────────────────┐
│              │  header: nieTTS 2.0    ● WS            │
│   Sidebar    ├──────────────────────────────────────────┤
│   (可折叠)    │                                          │
│              │        <router-view>                     │
│  ● 主页       │                                          │
│  ● 设置       │                                          │
│  ● 日志       │                                          │
│  ● 关于       │                                          │
│              │                                          │
└──────────────┴──────────────────────────────────────────┘
```

### 侧边栏 (`ElMenu`)

- 折叠按钮（hamburger 图标），折叠后仅显示图标
- 菜单项：
  - 主页（图标: `House`）— `#/`
  - 设置（图标: `Setting`）— `#/settings`
  - 日志（图标: `Document`）— `#/logs`
  - 关于（图标: `InfoFilled`）— `#/about`
- **侧边栏底部**: WebSocket 连接状态指示灯
  - 绿点 + "已连接"
  - 红点 + "已断开"
  - 黄点 + "重连中..."

### 顶部条（精简）

- 应用标题 "nieTTS 2.0"
- 右端：WS 指示灯 (与侧边栏底部的同步)

---

## 4. API 参考（不变，仅列差异）

Base URL: 同源 `""`, Content-Type: `application/json`

### 4.1 GET /voices

```json
{
  "tts_engines": ["edge_tts"],
  "all_tts_engines": ["edge_tts", "cosyvoice", "sambert", "MatchaTTS"],
  "translate_engines": [],
  "stt_engines": ["Qwen3"],
  "voices": {
    "edge_tts": ["zh-CN-XiaoxiaoNeural", ...],
    "cosyvoice": ["龙婉-普通话-...", ...],
    "sambert": ["知琪-温柔女声-...", ...],
    "MatchaTTS": ["0"]
  },
  "source_languages": ["中文", "英语", "日语"],
  "target_languages": ["英语"]
}
```

### 4.2 GET /config

```json
{
  "tts_provider": {
    "provider": "edge_tts",
    "providers": [
      {"name": "edge_tts", "voice": "zh-CN-XiaoxiaoNeural"},
      {"name": "cosyvoice", "voice": ""},
      {"name": "sambert", "voice": ""},
      {"name": "MatchaTTS", "voice": "0", ...}
    ]
  },
  "stt_provider": { "provider": "Qwen3", "providers": [...] },
  "translation_provider": { "provider": "openai", "providers": [...] },
  "device": "Headphones (...)",
  "tLanguage": "英语",
  "isPlayAudio": true,
  "isTranslate": true,
  "isPlayTranslation": true,
  "osc_enabled": true,
  "osc_host": "127.0.0.1",
  "osc_port": 9000,
  "vad": { "threshold": 0.5, ... },
  "ali_api_key": "",
  "available_devices": [{"name": "..."}, ...]
}
```

### 4.3 POST /config

部分更新，deep merge。任何配置变更立即调用。

```json
// Request
{ "isPlayAudio": false }

// Response 200
{ "success": true }
```

### 4.4 POST /tts

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 1-5000 字符 |
| tts_provider | string | 否 | |
| voice | string | 否 | |
| translate | bool | 否 | |
| play_audio | bool | 否 | |
| play_translation | bool | 否 | |
| osc_enabled | bool | 否 | |
| source_lang | string | 否 | |
| target_lang | string | 否 | |

---

## 5. WebSocket 协议

连接: `wss://<host>:<port>/ws`

### 客户端 → 服务端
```json
{ "type": "start" }
{ "type": "stop" }
```
二进制: int16 PCM, 16kHz mono

### 服务端 → 客户端
```json
{ "type": "stt_result", "text": "..." }
{ "type": "status", "request_id": "...", "state": "queued|processing|playing|done" }
{ "type": "log", "level": "info|warn|error", "message": "..." }
```

### 自动管线
```
录音 → binary PCM → WS → 后端: VAD→STT→TTS
                  ← WS: stt_result, status
```
前端不需要手动确认，不需要手动调 POST /tts。

---

## 6. 全局状态 (store)

```ts
// store.ts
import { reactive } from "vue"

export type LogEntry = {
  time: string
  level: "info" | "warn" | "error"
  message: string
}

export const appStore = reactive({
  engine: "edge_tts",
  voice: "",
  langs: { source: "中文", target: "英语" },
  config: {} as Record<string, any>,     // 全量配置缓存
  voices: {} as Record<string, string[]>, // 音色列表缓存
  logs: [] as LogEntry[],
  wsConnected: false,
})

export function addLog(level: LogEntry["level"], message: string) {
  const d = new Date()
  appStore.logs.push({ time: d.toTimeString().slice(0, 8), level, message })
  if (appStore.logs.length > 200) appStore.logs.shift()
}
```

---

## 7. 页面规格

### 7.1 主页 (`#/`): TTS 操作面板

极致精简。只保留操作相关元素，所有配置项去设置页。

**UI 布局**（垂直居中，max-width: 640px）:

```
┌─────────────────────────────────────────┐
│                                         │
│   [文本输入框 ElInput type=textarea]      │
│   autosize: minRows=6, maxRows=12       │
│                                         │
│   源语言 [ElSelect] → 目标语言 [ElSelect] │
│                                         │
│   当前引擎: edge_tts / zh-CN-XiaoXiao    │
│   (ElTag + 文字, 点击可跳转设置页)         │
│                                         │
│   [🔊 发送]  [🎤 语音输入]               │
│   (ElButton  type=primary)              │
│                                         │
│   ── LogBar 日志条 ──                    │
└─────────────────────────────────────────┘
```

**行为**:
- 文本框输入文字 → 点击 "发送" → `POST /tts`
  - 请求参数中的 `tts_provider`/`voice`/`translate`/`play_audio`/`play_translation`/`osc_enabled` 均从 `appStore.config` 读取
- "语音输入"按钮 → 浏览器弹出语音采集面板（见 7.5）
- 源语言/目标语言选择器选项来自 `appStore.voices.source_languages` / `target_languages`
- **每次发送 TTS 前/语言选择变更时**: 自动 `POST /config` 保存当前语言选择和应用配置（确保后端语音管线也用同样配置）

### 7.2 设置 (`#/settings`)

**即时保存**——所有配置变更立即 `POST /config`，不需要"保存"按钮。

**布局结构**:
```
┌──────────────────────────────────────────┐
│  ElTabs (tab-position="left" 或 top)      │
│                                          │
│  [TTS] [STT] [翻译] [音频&OSC]             │
│                                          │
│  ── TTS 面板 ──                           │
│  ElTabs (sub-tabs):                       │
│  [edge_tts] [cosyvoice] [sambert]         │
│  [MatchaTTS]                              │
│                                          │
│  ── edge_tts 子面板 ──                    │
│  默认引擎: [ElSwitch 是否设为默认]          │
│  音色: [ElSelect 下拉搜索]                 │
│                                          │
└──────────────────────────────────────────┘
```

**各分类面板规格**:

#### TTS 面板
- 顶部 `ElTabs`：edge_tts / cosyvoice / sambert / MatchaTTS
- 每个子 tab 内容：
  - "设为默认引擎" `ElSwitch`（选中则更新 `tts_provider.provider`，同时取消其他引擎的默认状态）
  - 音色选择 `ElSelect`（filterable, clearable, 选项来自 `/voices` 对应引擎列表）
  - **Edge TTS**: 仅音色选择
  - **CosyVoice / Sambert**: 音色 + 阿里 API Key (ElInput type=password)
  - **MatchaTTS**: 音色（speaker id）+ 模型路径系列（acoustic_model, vocoder, tokens, lexicon, data_dir, dict_dir）
- 变更即时 POST /config

#### STT 面板
- 显示当前 STT 引擎名称和模型信息（只读，Phase 2 开放配置）
- Qwen3: 显示 conv_frontend/encoder/decoder/tokenizer 路径
- VAD 参数（可编辑）: threshold, min_silence_duration, min_speech_duration, max_speech_duration

#### 翻译面板
- 翻译引擎选择 `ElSelect`（openai 等）
- API Key `ElInput` (type=password, show-password)
- API URL `ElInput`
- Model `ElInput`
- 目标翻译语言 `ElSelect`（中文/英语/日语/法语/德语...）

#### 音频 & OSC 面板
- 播放设备 `ElSelect`（选项来自 `available_devices`）
- 默认行为:
  - 播放音频 `ElSwitch` — `isPlayAudio`
  - 翻译 `ElSwitch` — `isTranslate`
  - 播放译文 `ElSwitch` — `isPlayTranslation`
- OSC:
  - OSC 启用 `ElSwitch` — `osc_enabled`
  - OSC Host `ElInput`
  - OSC Port `ElInputNumber` (1-65535)

**行为**:
- 任何一个控件值变更 → 立即 `POST /config` 该字段
- 如果 POST 失败，回滚该控件值并 `ElMessage.error` 提示
- 如果更新 `tts_provider.provider`（默认引擎切换），同步更新 `appStore.engine`
- 如果更新音色，同步更新 `appStore.voice`

### 7.3 日志 (`#/logs`)

- 全屏日志视图
- 顶部过滤按钮：全部 / info / warn / error
- 日志列表（虚拟滚动或简单 overflow-y: auto）
- 每条日志：`[时间] [级别标签] 消息`
- 清空按钮
- 自动滚动到最新
- 最多 500 条

### 7.4 关于 (`#/about`)

- 版本号: v2.1.2
- 技术栈简介
- 后端 API 地址
- WebSocket 状态

### 7.5 语音输入（内嵌在主页面）

集成在主页面板中，不单独占一个路由。

**触发方式**: 主页的 "语音输入" `ElButton`。
点击后展开一个嵌入式区域（或 ElDrawer 从底部弹出），包含：

- 录音按钮（圆形，红色脉冲动画，`ElButton` circle + 自定义 CSS）
- 录音状态文字: "点击开始录音" / "录音中..." / "识别中..."
- 实时识别文本展示
- 停止按钮

**实现**: 同之前规格（AudioContext → ScriptProcessorNode → int16 PCM → WS binary）。

---

## 8. 配置自动保存机制

核心原则：**用户在任何地方改变任何配置，立刻持久化，不需要手动保存按钮。**

实现方式：

```ts
// useConfig.ts — composable
import { watch } from "vue"
import { postConfig } from "../api"
import { appStore } from "../store"

export function useAutoSave(form: Record<string, any>, exclude: string[] = []) {
  let dirty = false
  const save = async () => {
    if (!dirty) return
    const payload: Record<string, any> = {}
    for (const [k, v] of Object.entries(form)) {
      if (!exclude.includes(k)) payload[k] = v
    }
    try {
      await postConfig(payload)
      dirty = false
    } catch {
      ElMessage.error("配置保存失败")
    }
  }
  return { save, markDirty: () => { dirty = true } }
}
```

**触发时机**:
| 操作 | 触发保存 |
|------|---------|
| 主页发送 TTS | 发送前保存当前语言选择 |
| 主页语言下拉变更 | 变更时保存 |
| 设置页任何 Switch/Select/Input 变更 | `@change` / `@update:model-value` 保存 |
| 主页"语音输入"按钮点击 | 开关状态变更时保存 |

设置页不需要 "保存/取消" 按钮。每次变更独立 POST。

---

## 9. WebSocket 管理器（全局单例）

```ts
// ws.ts
type MessageHandler = (msg: WSMessage) => void

class WSManager {
  private ws: WebSocket | null = null
  private handlers = new Set<MessageHandler>()
  private reconnectTimer: number | null = null
  private _cleanedUp = false
  connected = false

  connect() { /* ... */ }
  disconnect() { /* ... */ }
  onMessage(fn: MessageHandler): () => void {
    this.handlers.add(fn)
    return () => this.handlers.delete(fn)
  }
  send(data: string | ArrayBuffer) { /* ... */ }
}

export const wsManager = new WSManager()
```

- `wsManager.connected` 绑定到 store: `appStore.wsConnected`，驱动侧边栏指示灯
- 主页 `onMounted` 时注册 status/log 处理器
- 语音输入激活时注册 stt_result 处理器
- 重连时更新 `appStore.wsConnected` 状态

---

## 10. 组件树

```
App.vue
├── AppLayout.vue
│   ├── SideBar.vue
│   │   ├── ElMenu (折叠菜单)
│   │   │   ├── MenuItem: 主页
│   │   │   ├── MenuItem: 设置
│   │   │   ├── MenuItem: 日志
│   │   │   └── MenuItem: 关于
│   │   └── WSIndicator (连接状态灯)
│   └── <router-view>
│       ├── HomeView.vue (主页 #/)
│       │   ├── TextInput (ElInput textarea)
│       │   ├── LangSelectors (源/目标语言 ElSelect)
│       │   ├── EngineBadge (ElTag + 音色名)
│       │   ├── ActionButtons (发送 + 语音输入)
│       │   ├── VoicePanel.vue (录音区域，条件渲染)
│       │   └── LogBar.vue (最近日志)
│       ├── SettingsView.vue (设置 #/settings)
│       │   ├── ElTabs (分类)
│       │   └── 各子面板:
│       │       ├── TTSSettings.vue
│       │       │   └── ElTabs (子引擎) + 各引擎配置
│       │       ├── STTSettings.vue
│       │       ├── TranslateSettings.vue
│       │       └── AudioOSCSettings.vue
│       ├── LogsView.vue (日志 #/logs)
│       └── AboutView.vue (关于 #/about)
```

---

## 11. 数据流

```
启动:
  App.vue onMounted
    ├── GET /voices ──→ appStore.voices
    ├── GET /config ──→ appStore.config, engine, voice, langs
    └── wsManager.connect() ──→ appStore.wsConnected = true

主页发送 TTS:
  用户输入文字 → 点击发送
    ├── POST /config { source_lang, target_lang } (if changed)
    └── POST /tts { text, ...from config }
      └── WS → status/log → LogBar

语音输入:
  点击语音按钮 → VoicePanel 展开
    → getUserMedia → AudioContext
    → WS send { type:"start" }
    → ScriptProcessorNode → WS binary chunks
    → 点击停止 → WS send { type:"stop" }
    ← WS: stt_result { text } → 展示
    ← WS: status { state } → 展示管道进度

设置页:
  任何控件变更 → @change handler
    ├── 更新本地 form 状态
    ├── POST /config { changed_field }
    └── 如果涉及 engine/voice → 同步 appStore
```

---

## 12. 样式设计原则

- **色彩**: Element Plus 默认主题变量，CSS 变量覆盖
  - 主色: `--el-color-primary: #409EFF`
  - 暗色模式可选（通过 `ElSwitch` 切换 `dark` 类）
- **侧边栏**: 宽度 220px（展开）/ 64px（折叠），深色背景，过渡动画
- **主内容区**: flex-grow, 居中 max-width: 720px, padding: 24px
- **语音按钮**: 圆形 72px, 红色脉冲动画, box-shadow pulse
- **日志栏**: 固定在页面底部，半透明背景，最大高度 200px, overflow-y: auto
- **响应式**: 侧边栏在小屏自动折叠

---

## 13. 注意

1. `available_devices` 是只读字段，POST /config 时排除
2. 不使用 Vite 代理，所有请求同源
3. URL/WS 地址使用 `location.host`，不硬编码
4. 语音输入不需要手动确认步骤（后端已自动 STT→TTS）
5. 配置即时保存，无需手动 "保存" 按钮
6. 证书自签名，首次访问需手动信任
7. 错误处理：API 返回 `{ error: "..." }` 时 `ElMessage.error`
8. 构建产物输出到 `../templates/`，`emptyOutDir: true`
