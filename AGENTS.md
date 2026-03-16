# nieTTS2.0 项目上下文

## 项目概述

nieTTS2.0 是一个现代化的文本转语音（TTS）Web 应用，支持多种 TTS 引擎，提供 Web 界面和 REST API 接口。主要用于语音合成、语音识别、文本翻译，并与 VRChat 通过 OSC 协议集成。

## 技术栈

| 层级 | 技术 |
|------|------|
| Web 框架 | Quart (异步 Flask 兼容) |
| TTS 引擎 | Edge TTS, 阿里百炼 DashScope (CosyVoice/SamBert) |
| 音频播放 | pygame-ce |
| OSC 通信 | python-osc |
| 翻译服务 | 硅基流动 API (OpenAI 兼容) |
| HTTP/HTTPS | 自签名证书支持 (cryptography) |
| 前端 | 原生 HTML/CSS/JavaScript |

## 项目结构

```
nieTTS2.0/
├── app.py              # 主应用入口，包含 TTSWebApp 类
├── config.json         # 用户配置文件（自动生成）
├── pyproject.toml      # 项目依赖和元数据
├── templates/
│   └── index.html      # Web 前端界面
├── save/               # 临时音频文件存储
├── certificates/       # HTTPS 证书目录（运行时生成）
└── .venv/              # Python 虚拟环境
```

## 核心模块说明

### app.py - 主应用

`TTSWebApp` 类是核心，包含：

- **语音引擎配置**:
  - `Edge_TTS_voices`: Edge TTS 发音人映射
  - `ali_tts_voices`: 阿里百炼 CosyVoice 发音人
  - `sambert_tts_voices`: 阿里百炼 SamBert 发音人

- **主要路由**:
  - `GET /`: 渲染 Web 界面
  - `POST /tts`: 文本转语音 API

- **关键方法**:
  - `use_edge_tts()`: Edge TTS 转换
  - `use_ali_tts()`: 阿里百炼 CosyVoice 转换
  - `use_sambert_tts()`: 阿里百炼 SamBert 转换
  - `useTranslate()`: 调用翻译 API
  - `_play_worker()`: 后台音频播放队列

### templates/index.html - 前端

- 单页应用，原生 JavaScript
- 支持语音识别 (MediaRecorder API + 硅基流动 ASR)
- 动态切换 TTS 服务商界面

## 构建和运行

### 环境要求

- Python 3.10+
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
  "ali_api_key": "阿里百炼API密钥",
  "siliconflowApiKey": "硅基流动API密钥",
  "device": "音频输出设备",
  "isdownload": false,
  "isplayaudio": true,
  "isTranslate": false,
  "tLanguage": "英语"
}
```

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
- 目标 Python 版本: 3.10+

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

## 相关链接

- GitHub: https://github.com/machinad/nieTTS2.0
- 阿里百炼: https://dashscope.aliyun.com/
- 硅基流动: https://siliconflow.cn/
