# nieTTS 2.0

> 面向 VR 社交平台的一体化 TTS + 翻译 + STT 桌面应用

[English](README_EN.md) | 中文

## 简介

nieTTS 2.0 是一款专为 VR 社交平台（如 VRChat）设计的桌面应用，集成了语音合成（TTS）、语音识别（STT）和翻译功能。支持多种在线和离线引擎，提供 PySide6 桌面 GUI 和 Vue 3 Web 界面，可通过 OSC 协议与 VRChat 无缝集成。

**当前版本**：v2.1.2  
**平台支持**：Windows

## 功能特性

### 语音合成（TTS）

| 引擎 | 类型 | 说明 |
|------|------|------|
| **Edge TTS** | 在线 | 微软官方免费 TTS 服务，40+ 中文音色，无需 API Key |
| **CosyVoice** | 在线 | 阿里百炼 CosyVoice，支持情感控制、语音克隆 |
| **Sambert** | 在线 | 阿里百炼 Sambert，通用场景 |
| **MatchaTTS** | 离线 | 完全本地推理，中英双语，基于 sherpa-onnx |

### 语音识别（STT）

| 引擎 | 类型 | 说明 |
|------|------|------|
| **Qwen3 ASR** | 离线 | 通义千问 Qwen3 本地离线语音识别，0.6B 参数 INT8 量化 |

### 翻译

| 引擎 | 类型 | 说明 |
|------|------|------|
| **OpenAI 兼容** | 在线 | 支持任意 OpenAI API 格式的大语言模型 |
| **HY-MT1.5** | 离线 | 腾讯混元本地离线翻译，1.8B 参数 GGUF 量化模型 |

### 其他功能

- **VAD 语音检测**：Silero VAD，精准检测语音起止
- **OSC 通信**：VRChat chatbox 集成，自动发送合成文本
- **覆盖层**：半透明悬浮窗口，全局热键（Ctrl+T）唤出
- **音频播放**：支持 WAV/MP3/OGG/FLAC/OPUS 格式，可选播放设备
- **请求管道**：双异步队列，翻译与 TTS 并行执行
- **多语言支持**：中文、英语、日语、韩语、法语、德语等 15 种语言

## 安装

### 前置要求

- Python 3.14.2
- Node.js (用于构建前端)

### 使用 uv 安装（推荐）

```bash
# 1. 安装 uv
pip install uv

# 2. 克隆项目
git clone https://github.com/machinad/nieTTS2.0.git
cd nieTTS2.0

# 3. 安装 Python 依赖
uv sync

# 4. 安装前端依赖
cd frontend
npm install
cd ..
```

### 使用 pip 安装

```bash
# 克隆项目
git clone https://github.com/machinad/nieTTS2.0.git
cd nieTTS2.0

# 安装依赖
pip install -e .

# 安装前端依赖
cd frontend
npm install
cd ..
```

## 启动

### GUI 模式（推荐）

```bash
python gui_main.py
# 或
uv run python gui_main.py
```

启动后将打开桌面应用，包含以下页面：
- **主页**：文本输入、语言选择、引擎状态、语音输入
- **设置**：引擎配置、音频设备、OSC 设置、模型下载
- **日志**：实时日志查看
- **关于**：版本信息

### Headless 模式

```bash
python main.py
# 或
uv run python main.py
```

仅启动 Web 服务（默认端口 11451），通过浏览器访问 Web 界面。

### 前端开发

```bash
cd frontend
npm run dev      # 启动 Vite 开发服务器
npm run build    # 构建到 ../templates/
npm run preview  # 预览构建结果
```

## 模型下载

部分引擎需要下载模型文件才能使用。提供两种下载方式：

### 方式一：软件内下载（推荐）

启动 GUI 后，进入 **设置 → 模型下载** 标签页：
- 选择下载源（HuggingFace / HuggingFace 镜像 / ModelScope）
- 点击"开始下载"按钮
- 查看各引擎模型下载进度

### 方式二：命令行下载

```bash
# 下载所有缺失模型
python scripts/download_models.py download

# 检查所有模型状态
python scripts/download_models.py check

# 快速检查（跳过 SHA256 校验）
python scripts/download_models.py check --fast

# 下载特定引擎模型
python scripts/download_models.py download --engine matcha_tts

# 强制重新下载
python scripts/download_models.py download --force
```

### 下载源

| 源 | 说明 | 推荐 |
|----|------|------|
| `huggingface` | HuggingFace 官方源 | 海外用户 |
| `huggingface_mirror` | HuggingFace 镜像（hf-mirror.com） | 国内用户（默认） |
| `modelscope` | ModelScope 源 | 国内用户 |

```bash
# 指定下载源
python scripts/download_models.py download --source modelscope
```

### 支持的模型

| 引擎 | 模型 | 大小 | 用途 |
|------|------|------|------|
| Silero VAD | `silero_vad.onnx` | ~2.2 MB | 语音活动检测 |
| MatchaTTS | `matcha-icefall-zh-en/` | ~130 MB | 本地 TTS |
| Qwen3 ASR | `qwen3-asr-0.6B-int8/` | ~1 GB | 本地 STT |
| HY-MT2 | `Hy-MT2-1.8B-2Bit.gguf` | ~600 MB | 本地翻译 |

## 自行构建

### 前端构建

```bash
cd frontend
npm install
npm run build    # 输出到 ../templates/
```

### PyInstaller 打包

```bash
# 完整打包
python build.py

# 先构建前端，再打包
python build.py --frontend

# 清理构建目录后重新打包
python build.py --clean
```

输出文件：`dist/nieTTS/nieTTS.exe`

## 开源项目声明

本项目使用了以下开源项目，特此感谢：

### 核心运行时

| 项目 | 许可证 | 用途 | 链接 |
|------|--------|------|------|
| **sherpa-onnx** | Apache-2.0 | 本地推理引擎，用于 MatchaTTS、Qwen3 ASR、Silero VAD | [GitHub](https://github.com/k2-fsa/sherpa-onnx) |
| **edge-tts** | MIT | 微软 Edge TTS 在线服务 Python 封装 | [GitHub](https://github.com/rany2/edge-tts) |
| **dashscope** | Apache-2.0 | 阿里百炼 SDK，用于 CosyVoice、Sambert | [GitHub](https://github.com/dashscope/dashscope-sdk-python) |
| **openai** | Apache-2.0 | OpenAI API Python 客户端 | [GitHub](https://github.com/openai/openai-python) |
| **numpy** | BSD-3-Clause | 数值计算、音频数据处理 | [GitHub](https://github.com/numpy/numpy) |
| **miniaudio** | Unlicense | 音频播放库 | [GitHub](https://github.com/mackron/miniaudio) |
| **python-osc** | MIT | OSC 协议实现，用于 VRChat 通信 | [GitHub](https://github.com/attwad/python-osc) |
| **httpx** | BSD-3-Clause | HTTP 客户端 | [GitHub](https://github.com/encode/httpx) |

### Web 服务

| 项目 | 许可证 | 用途 | 链接 |
|------|--------|------|------|
| **quart** | MIT | 异步 Web 框架（Flask 异步版） | [GitHub](https://github.com/pallets/quart) |
| **quart-cors** | MIT | Quart 跨域支持 | [GitHub](https://github.com/pallets/quart-cors) |
| **cryptography** | Apache-2.0/BSD-3-Clause | 自签名 HTTPS 证书生成 | [GitHub](https://github.com/pyca/cryptography) |

### GUI

| 项目 | 许可证 | 用途 | 链接 |
|------|--------|------|------|
| **PySide6** | LGPL-3.0 | Qt6 Python 绑定 | [官网](https://wiki.qt.io/Qt_for_Python) |
| **qasync** | BSD-2-Clause | Qt + asyncio 事件循环桥接 | [GitHub](https://github.com/gmarull/qasync) |

### 前端

| 项目 | 许可证 | 用途 | 链接 |
|------|--------|------|------|
| **Vue 3** | MIT | 渐进式 JavaScript 框架 | [GitHub](https://github.com/vuejs/core) |
| **Vue Router 4** | MIT | Vue.js 官方路由 | [GitHub](https://github.com/vuejs/router) |
| **Element Plus** | MIT | Vue 3 UI 组件库 | [GitHub](https://github.com/element-plus/element-plus) |
| **Vite** | MIT | 下一代前端构建工具 | [GitHub](https://github.com/vitejs/vite) |

### 模型下载

| 项目 | 许可证 | 用途 | 链接 |
|------|--------|------|------|
| **huggingface-hub** | Apache-2.0 | HuggingFace 模型下载 | [GitHub](https://github.com/huggingface/huggingface_hub) |
| **modelscope** | Apache-2.0 | ModelScope 模型下载 | [GitHub](https://github.com/modelscope/modelscope) |

### 开发工具

| 项目 | 许可证 | 用途 | 链接 |
|------|--------|------|------|
| **pytest** | MIT | Python 测试框架 | [GitHub](https://github.com/pytest-dev/pytest) |
| **pytest-asyncio** | Apache-2.0 | pytest 异步测试支持 | [GitHub](https://github.com/pytest-dev/pytest-asyncio) |
| **PyInstaller** | GPL-2.0 | Python 程序打包 | [GitHub](https://github.com/pyinstaller/pyinstaller) |

## 许可证

本项目基于 Apache License 2.0 开源。详见 [LICENSE](LICENSE) 文件。

## 致谢

感谢所有开源项目的开发者，是你们的工作让 nieTTS 2.0 成为可能。
