# nieTTS2.0 项目上下文

## 项目概述

nieTTS2.0 是一个现代化的文本转语音（TTS）Web 应用，支持多种 TTS 引擎，提供 Web 界面和 REST API 接口。主要用于语音合成、语音识别、文本翻译，并通过 OSC 协议与 VRChat 集成。

## 技术栈

| 层级 | 技术 |
|------|------|
| Web 框架 | Quart (异步 Flask 兼容) |
| TTS 引擎 | Edge TTS, 阿里百炼 DashScope (CosyVoice/SamBert) |
| 音频播放 | pygame-ce |
| OSC 通信 | python-osc |
| 翻译服务 | 硅基流动 API (OpenAI 兼容) |
| 语音识别 | 硅基流动 ASR (TeleSpeechASR) |
| HTTP/HTTPS | 自签名证书支持 (cryptography) |
| 前端 | 原生 HTML/CSS/JavaScript |

## 项目结构

```
nieTTS2.0/
├── app.py              # 主应用入口，包含 TTSWebApp 类
├── config.json         # 用户配置文件（自动生成）
├── pyproject.toml      # 项目依赖和元数据
├── uv.lock             # uv 包管理器锁文件
├── templates/
│   └── index.html      # Web 前端界面
├── save/               # 临时音频文件存储
├── certificates/       # HTTPS 证书目录（运行时生成，退出时清理）
└── .venv/              # Python 虚拟环境
```

## 核心模块说明

### app.py - 主应用

`TTSWebApp` 类是核心，包含：

- **语音引擎配置**:
  - `Edge_TTS_voices`: Edge TTS 发音人映射 (16个发音人)
  - `ali_tts_voices`: 阿里百炼 CosyVoice 发音人 (20个发音人)
  - `sambert_tts_voices`: 阿里百炼 SamBert 发音人 (43个发音人)

- **主要路由**:
  - `GET /`: 渲染 Web 界面
  - `POST /tts`: 文本转语音 API

- **关键方法**:
  - `use_edge_tts()`: Edge TTS 转换
  - `use_ali_tts()`: 阿里百炼 CosyVoice 转换
  - `use_sambert_tts()`: 阿里百炼 SamBert 转换
  - `useTranslate()`: 调用翻译 API
  - `_play_worker()`: 后台音频播放队列
  - `cleanup_certificates()`: 程序退出时清理证书文件

- **音频队列机制**:
  - 请求级别的音频队列管理
  - 确保原文和译文连续播放
  - 使用 `asyncio.Queue` 实现异步播放

- **OSC 集成**:
  - 发送文本到 VRChat (`/chatbox/input`)
  - 默认目标: `127.0.0.1:9000`

### templates/index.html - 前端

- 单页应用，原生 JavaScript
- 支持语音识别 (MediaRecorder API + 硅基流动 ASR)
- 动态切换 TTS 服务商界面
- ASCII 艺术启动横幅 "NIE"

## 依赖项

### 运行依赖

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| pygame-ce | >=2.5.0 | 音频播放 |
| pywin32 | >=306 | Windows API 调用 |
| comtypes | >=1.4.0 | COM 接口支持 |
| edge-tts | >=6.1.0 | Edge TTS 引擎 |
| python-osc | >=1.8.0 | VRChat OSC 通信 |
| quart | >=0.19.0 | 异步 Web 框架 |
| httpx | >=0.27.0 | HTTP 客户端 |
| dashscope | >=1.20.0 | 阿里百炼 SDK |
| librosa | >=0.10.0 | 音频处理库 |
| pyyaml | >=6.0.1 | YAML 解析 |
| openai | >=1.30.0 | OpenAI 兼容 API |
| cryptography | >=42.0.0 | HTTPS 证书生成 |

### 开发依赖

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| ruff | >=0.4.0 | 代码检查和格式化 |
| mypy | >=1.10.0 | 静态类型检查 |

## AI 模型配置

| 功能 | 模型 | 服务商 |
|------|------|--------|
| 文本翻译 | Qwen/Qwen3-8B | 硅基流动 |
| 语音识别 (ASR) | TeleAI/TeleSpeechASR | 硅基流动 |

## 发音人列表

### Edge TTS (16个发音人)

| 类型 | 发音人 |
|------|--------|
| 汉语女声 | 晓晓、晓艺、晓贝(辽宁方言)、晓倪(西安方言) |
| 汉语男声 | 云间、云曦、云霞、云阳 |
| 台湾女声 | 晓晨、晓玉 |
| 台湾男声 | 云杰 |
| 粤语女声 | 晓佳、晓雯 |
| 粤语男声 | 云龙 |
| 日语男声 | 圭太 |
| 日语女声 | 七海 |

### 阿里百炼 CosyVoice (20个发音人)

| 类型 | 发音人 |
|------|--------|
| 中文 | 龙婉、龙橙、龙华、龙小淳、龙小夏、龙小诚、龙小白、龙老铁、龙书、龙硕、龙婧、龙妙、龙悦、龙媛、龙飞、龙杰力豆、龙彤、龙祥 |
| 英文 | Stella、Bella |

### 阿里百炼 SamBert (43个发音人)

| 类型 | 发音人 |
|------|--------|
| 中文女声 | 知琪、知佳、知茹、知倩、知薇、知婧、知娜、知莎、知婷、知笑、知雅、知媛、知颖、知悦、知柜、知妙、知猫、知楠、知厨 |
| 中文男声 | 知德、知祥、知浩、知茗、知墨、知树、知晔、知硕、知伦、知飞、知达 |
| 多语言 | Camila(西班牙语)、Perla(意大利语)、Indah(印尼语)、Clara(法语)、Hanna(德语)、Beth、Betty、Cally、Cindy、Eva、Donna、Brian、Waan(泰语) |

## 构建和运行

### 环境要求

- Python 3.10-3.13
- Windows 系统（音频设备依赖）

### 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 启动应用

```bash
python app.py
```

默认监听 `0.0.0.0:1145`，自动打开浏览器。

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `APP_HOST` | 监听地址 | `0.0.0.0` |
| `APP_PORT` | 监听端口 | `1145` |

## API 接口

### POST /tts

文本转语音合成接口。

**请求体 (JSON)**:
```json
{
  "text": "要转换的文本",
  "provider": "Edge TTS | 阿里百炼cosyvice | 阿里百炼sambert",
  "edge_tts_voice": "发音人名称",
  "ali_tts_voice": "阿里百炼 CosyVoice 发音人",
  "sambert_tts_voice": "阿里百炼 SamBert 发音人",
  "ali_api_key": "阿里百炼API密钥",
  "siliconflowApiKey": "硅基流动API密钥",
  "device": "音频输出设备",
  "tLanguage": "英语 | 日语",
  "isdownload": false,
  "isplayaudio": true,
  "isTranslate": false,
  "isPlayTranslation": false
}
```

**请求参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | 是 | 要转换的文本（最大5000字符） |
| `provider` | string | 是 | TTS 服务商 |
| `edge_tts_voice` | string | 条件 | Edge TTS 发音人（provider=Edge TTS 时必填） |
| `ali_tts_voice` | string | 条件 | CosyVoice 发音人（provider=阿里百炼cosyvice 时必填） |
| `sambert_tts_voice` | string | 条件 | SamBert 发音人（provider=阿里百炼sambert 时必填） |
| `ali_api_key` | string | 条件 | 阿里百炼 API 密钥（使用阿里百炼时必填） |
| `siliconflowApiKey` | string | 条件 | 硅基流动 API 密钥（启用翻译时必填） |
| `device` | string | 否 | 音频输出设备名称 |
| `tLanguage` | string | 否 | 翻译目标语言（默认：英语） |
| `isdownload` | boolean | 否 | 是否下载音频文件（默认：false） |
| `isplayaudio` | boolean | 否 | 是否播放音频（默认：true） |
| `isTranslate` | boolean | 否 | 是否启用翻译（默认：false） |
| `isPlayTranslation` | boolean | 否 | 是否播放译文（默认：false） |

**响应**:
- `isdownload=true`: 返回音频文件下载
- `isdownload=false`: 返回 JSON 状态信息

## 配置文件 (config.json)

```json
{
  "provider": "Edge TTS",
  "edge_tts_voice": "zh-CN-XiaoxiaoNeural",
  "device": "默认设备",
  "ali_tts_voice": "龙婉-普通话-语音助手、导航播报、聊天数字人",
  "sambert_tts_voice": "知婧-严厉女声-通用场景",
  "ali_api_key": "",
  "siliconflowApiKey": "",
  "tLanguage": "英语",
  "isdownload": false,
  "isplayaudio": true,
  "isTranslate": true,
  "isPlayTranslation": false
}
```

## 开发约定

### 代码风格

- 使用 Ruff 进行代码检查（配置见 `pyproject.toml`）
- 行长度限制: 120 字符
- 目标 Python 版本: 3.10-3.13

### 异步编程

- 使用 `async/await` 模式
- Quart 路由处理器必须为异步函数
- 音频播放使用 `asyncio.Queue` 队列管理

### 配置管理

- 使用 `config_lock` (asyncio.Lock) 保护配置文件读写
- 配置变更通过 Web 界面或 API 触发自动保存

### 安全考虑

- API 密钥通过请求体传递，不硬编码
- 输入验证：文本长度限制 5000 字符
- API 密钥格式检查（最小长度 10 字符）

## 常见开发任务

### 添加新的 TTS 引擎

1. 在 `TTSWebApp.__init__()` 中添加发音人映射
2. 实现 `async def use_xxx_tts(self, data, temp_file)` 方法
3. 在 `tts_endpoint()` 中添加引擎分支
4. 更新 `tts_providers` 列表
5. 更新前端界面

### 添加新的 API 端点

```python
def setup_routes(self):
    self.app.route('/new-endpoint', methods=['GET'])(self.new_endpoint)

async def new_endpoint(self):
    # 实现逻辑
    return jsonify({"status": "ok"})
```

### 修改默认端口

设置环境变量或修改 `app.py` 底部:
```python
port = int(os.environ.get('APP_PORT', 1145))
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 端口被占用 | 修改 `APP_PORT` 环境变量 |
| 音频无法播放 | 检查 `device` 配置和音频设备连接 |
| API 认证失败 | 验证 API 密钥有效性和配额 |
| HTTPS 证书警告 | 自签名证书，选择"继续访问" |
| API 密钥泄露风险 | `config.json` 存储明文密钥，请勿提交到版本控制系统，建议添加到 `.gitignore` |

## 相关链接

- GitHub: https://github.com/machinad/nieTTS2.0
- 阿里百炼: https://dashscope.aliyun.com/
- 硅基流动: https://siliconflow.cn/