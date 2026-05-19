# nieTTS2.0 安装说明

## 系统要求
- Python 3.8 或更高版本
- Windows 10/11（支持音频设备）
- 网络连接（用于TTS服务和翻译功能）

## 快速安装

### 1. 克隆仓库
```bash
git clone https://github.com/machinad/nieTTS2.0.git
cd nieTTS2.0
```

### 2. 创建虚拟环境（推荐）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

## 依赖说明

### 主要依赖
| 包名 | 版本 | 用途 |
|------|------|------|
| `pygame-ce` | - | 音频播放 |
| `pywin32` | - | Windows音频设备控制 |
| `edge-tts` | - | Edge TTS服务 |
| `quart` | - | Web框架（异步Flask） |
| `dashscope` | - | 阿里百炼TTS服务 |
| `openai` | - | 翻译功能（硅基流动API） |
| **`cryptography`** | **>=41.0.0** | **HTTPS自签名证书生成** |

### 新增依赖说明
- **`cryptography`**: 用于生成自签名HTTPS证书，支持局域网设备使用录音功能

## 配置说明

### 1. API密钥配置
首次运行应用后，在Web界面中配置：
- 阿里百炼API密钥（用于阿里TTS服务）
- 硅基流动API密钥（用于翻译和语音识别）

### 2. HTTPS支持
应用会自动：
- 检测本机IP地址
- 生成自签名证书
- 启用HTTPS服务（端口1145）
- 退出时自动清理证书文件

## 运行应用

### 启动命令
```bash
python app.py
```

### 访问方式
1. **本地访问**: `https://127.0.0.1:1145`
2. **局域网访问**: `https://[本机IP]:1145`

### 浏览器安全警告
由于使用自签名证书，浏览器会显示安全警告：
1. 点击"高级"或"详细信息"
2. 点击"继续访问"或"访问此网站"
3. 这是正常现象，不影响功能使用

## 功能特性

### ✅ 已实现
- [x] 文字转语音（Edge TTS、阿里百炼）
- [x] 语音识别（录音转文字）
- [x] 文本翻译（多语言支持）
- [x] VRChat OSC集成
- [x] HTTPS支持（局域网录音功能）
- [x] 自签名证书自动生成
- [x] 音频设备选择
- [x] 配置保存

### 🔄 自动清理
- 每次启动生成新的证书
- 程序退出时自动清理证书文件
- 避免证书文件积累

## 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# 修改端口号
set APP_PORT=1146
python app.py
```

#### 2. 依赖安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 单独安装cryptography
pip install cryptography>=41.0.0
```

#### 3. 录音功能不可用
- 确保使用HTTPS访问（`https://`开头）
- 浏览器接受证书警告
- 授予麦克风权限

#### 4. 证书生成失败
- 检查网络连接（获取本机IP需要）
- 确保有写入权限
- 检查cryptography库版本

## 开发说明

### 项目结构
```
nieTTS2.0/
├── app.py              # 主应用
├── requirements.txt    # 依赖列表
├── templates/          # HTML模板
│   └── index.html     # 前端界面
├── certificates/       # 证书目录（自动生成）
├── save/              # 临时文件目录
└── config.json        # 用户配置（自动生成）
```

### 代码贡献
1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证
Apache-2.0 License

## 支持
- GitHub Issues: https://github.com/machinad/nieTTS2.0/issues
- 作者: machinad