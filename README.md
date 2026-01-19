# nieTTS 2.0

一个现代化的文本转语音（TTS）Web应用，支持多种TTS引擎，提供Web界面和API接口。

## 功能特性

- 🎤 **多引擎支持**
  - Edge TTS（微软语音合成）
  - 阿里百炼 CosyVoice（阿里云语音合成）
  - 阿里百炼 SamBert（阿里云语音合成）

- 🎨 **Web界面** - 提供友好的Web UI进行文本转语音

- 🔊 **灵活的输出选项**
  - 直接播放音频
  - 下载音频文件
  - 通过OSC协议发送数据到VRCHAT

- 📝 **丰富的音色选择**
  - Edge TTS：8种中文发音人
  - 阿里百炼CosyVoice：20+种发音人
  - 阿里百炼SamBert：40+种发音人

## 系统要求

- Python 3.8+
- Windows系统（需要Windows音频驱动支持）

## 安装

### 1. 安装依赖

**推荐方式：使用 `启动.bat` 文件**

直接双击运行 `启动.bat` 文件，脚本会自动安装依赖并启动应用。

**手动方式：**
```bash
pip install -r requirements.txt
```

依赖包括：
- `pygame-ce` - 音频播放
- `quart` - 异步Web框架
- `edge-tts` - 微软Edge TTS
- `dashscope` - 阿里百炼SDK
- `librosa` - 音频处理
- `python-osc` - OSC协议支持

### 2. 配置API密钥（可选）

如需使用阿里百炼TTS，在Web界面中输入API密钥即可，无需修改配置文件。

**在Web界面输入API密钥：**
1. 启动应用后，打开 `http://localhost:1145`
2. 在Web界面的设置面板中找到 "API密钥" 输入框
3. 粘贴您的阿里百炼API密钥
4. 保存设置

**获取API密钥：** 访问[阿里云DashScope官网](https://dashscope.aliyun.com/)

## 使用方法

### 启动应用

**推荐方式：使用批处理文件（Windows）**

直接双击运行 `启动.bat` 文件，脚本会自动完成以下操作：
1. 检查并安装Python依赖
2. 启动TTS Web应用
3. 自动打开浏览器访问应用

**手动启动方式：**
```bash
python app.py
```

应用启动后，打开浏览器访问：`http://localhost:1145`

> 💡 **提示**：首次运行时，`启动.bat` 会自动安装所有必要的依赖，之后可以直接双击启动。

### 配置说明

#### Web界面配置

在Web界面上可以配置以下选项：
- **TTS引擎** - 选择使用的TTS服务
- **发音人** - 根据选择的引擎显示对应的发音人列表
- **API密钥** - 输入阿里百炼的API密钥（如使用阿里百炼TTS）
- **输出设备** - 选择音频输出设备
- **自动播放** - 是否自动播放合成的语音
- **下载音频** - 是否同时保存音频文件

#### 配置文件说明

编辑 `config.json` 可配置以下基础选项（大多数设置可在Web界面修改）：

| 配置项 | 说明 | 默认值 |
|-------|------|-------|
| `provider` | 选择TTS引擎 | `Edge TTS` |
| `edge_tts_voice` | Edge TTS发音人 | `zh-CN-XiaoxiaoNeural` |
| `ali_tts_voice` | 阿里百炼CosyVoice发音人 | `龙婉-普通话-语音助手、导航播报、聊天数字人` |
| `sambert_tts_voice` | 阿里百炼SamBert发音人 | `知婧-严厉女声-通用场景` |
| `device` | 音频输出设备 | `默认设备` |
| `isplayaudio` | 是否自动播放音频 | `true` |
| `isdownload` | 是否下载音频文件 | `false` |

#### 虚拟声卡配置（搭配直播/录制使用）

若需要将TTS输出用于直播或录制，推荐使用虚拟声卡：

**1. 安装虚拟声卡软件**
   - **VB-Audio Virtual Cable**（推荐，免费版可用）
   - **Virtual Audio Cable**（付费）

**2. 配置虚拟声卡**
   - 在Windows中设置虚拟声卡为默认播放设备
   - 在应用Web界面的"输出设备"选项中选择虚拟声卡
   - 测试语音输出

**3. 在直播/录制软件中**
   - 设置音频输入源为虚拟声卡
   - 进行直播或录制

**示例流程**：
- 安装 VB-Cable → 设为默认设备 → 在本应用中选择 VB-Audio Virtual Cable → 在OBS/直播软件中选择该虚拟设备作为输入源

## 发音人列表

### Edge TTS 中文发音人

**女声：**
- zh-CN-XiaoxiaoNeural（晓晓，温暖）
- zh-CN-XiaoyiNeural（晓伊，活泼）
- zh-CN-liaoning-XiaobeiNeural（辽宁晓北，幽默）
- zh-CN-shaanxi-XiaoniNeural（陕西晓妮，明亮）

**男声：**
- zh-CN-YunjianNeural（云健，热情）
- zh-CN-YunxiNeural（云希，活泼/阳光）
- zh-CN-YunxiaNeural（云笑，可爱）
- zh-CN-YunyangNeural（云阳，专业/可靠）

### 阿里百炼 CosyVoice 发音人

包含20+种发音人，如：
- 龙婉（语音助手、导航播报、聊天数字人）
- 龙橙（语音助手、导航播报、聊天数字人）
- 龙华（语音助手、导航播报、聊天数字人）
- 龙小淳（普通话+英文）
- 龙老铁（东北口音）
- 等等...

### 阿里百炼 SamBert 发音人

包含40+种发音人，支持中文、英文、西班牙语、意大利语、印尼语、法语、德语、泰语等多语言，如：
- 知琪（温柔女声）
- 知佳（标准女声）
- 知茹（新闻女声）
- 知楠（广告男声）
- Clara（法语女声）
- Beth（咨询女声）
- 等等...

## 目录结构

```
nieTTS2.0/
├── app.py              # 主应用文件
├── config.json         # 配置文件
├── requirements.txt    # 依赖列表
├── README.md          # 项目说明
├── 启动.bat            # Windows启动脚本
├── templates/         # Web模板文件夹
│   └── index.html     # Web界面
└── save/              # 音频保存文件夹
```

## API接口

应用提供以下REST API端点（具体见 Web 界面）：

- `GET /` - Web界面主页
- `POST /synthesize` - 文本转语音合成
- `GET /voices` - 获取可用发音人列表
- `GET /config` - 获取当前配置

## 许可证

见 LICENSE 文件

## 注意事项

1. **Edge TTS**：无需额外配置，开箱即用
2. **阿里百炼TTS**：需要有效的API密钥，可在Web界面输入框中输入（推荐）或修改config.json
3. **音频播放**：需要Windows系统支持，建议在操作系统中正确配置音频设备
4. **输出设备选择**：
   - 若要直接播放：选择扬声器或耳机
   - 若要用于直播/录制：选择虚拟声卡（VB-Cable等）
   - 若要发送到VRChat：需配置虚拟声卡后，在VRChat中选择对应的麦克风设备
5. **OSC功能**：默认向本地127.0.0.1:9000发送OSC数据（用于VRChat等支持OSC的应用）

## 故障排除

### 音频无法播放
- 检查音频设备是否正确连接
- 确认 `config.json` 中的 `device` 设置正确
- 尝试重新启动应用

### API认证失败
- 确认已在Web界面输入正确的API密钥
- 检查API密钥是否过期或无效
- 确保API密钥对应的账户有充足的配额
- 访问阿里云DashScope官网更新密钥或查看配额

### 输出设备不显示
- 确保音频设备已正确连接或虚拟声卡已安装
- 重新启动应用以刷新设备列表
- 在Windows设备管理器中检查音频设备状态

### 虚拟声卡无声
- 检查虚拟声卡是否正确安装
- 确认Web界面已选择正确的虚拟声卡设备
- 在Windows音频设置中将虚拟声卡设为默认设备
- 尝试重新启动应用

### 端口被占用
- 修改应用中的端口配置（需修改app.py中的监听端口）
- 或关闭占用该端口的其他应用

## 贡献

欢迎提交Issue和Pull Request！

---

**最后更新**: 2026年1月17日
