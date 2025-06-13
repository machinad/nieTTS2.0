# nieTTS 2.0

一个基于多种语音合成技术的综合语音工具箱。

## 功能特点

- 支持多种语音合成引擎:
  - Edge TTS
  - 阿里百炼 cosyvoice
  - 阿里百炼 sambert
  - GPT-SoVITS 本地推理
  - Index TTS
  - RVC 变声器

- 主要功能:
  - 文本转语音(TTS)
  - 实时语音变声
  - VRChat OSC消息推送
  - 本地模型推理
  - 音频设备管理

## 安装说明

1. 需要安装conda，并且配置好环境变量
2. 运行 `安装依赖.bat` 安装所需依赖包
3. 双击 `启动！！！.bat` 启动应用

## 目录结构

```
nieTTS2.0/
├── app.py                 # 主程序
├── gui_v1.py             # GUI 相关功能
├── requirements.txt      # 依赖包列表
├── assets/              # RVC模型资源文件
├── checkpoints/         # index TTS模型文件夹
├── configs/             # 配置文件
├── GPTvts/             # GPT-SoVITS 项目目录，请将整个GPT-SoVITS整合包放进去
├── GPTvts_voices/      # 语音样本文件夹
├── indextts/           # Index TTS 实现
├── models/             # GPT-SoVITS 模型文件
├── save/               # 音频输出目录
└── templates/          # Web 界面模板
```

## 使用说明

1. 启动程序后访问 web 界面
2. 选择所需的语音合成引擎
3. 根据需要配置相关参数:
   - 选择音频设备
   - 调整语音模型
   - 设置变声参数等
4. 输入文本即可进行语音合成

### Edge TTS

无需额外配置,直接使用微软的在线服务。

### 阿里百炼

需要配置 API Key 才能使用阿里云语音服务。

### GPT-SoVITS
 该服务直接使用的GPT-SoVITS项目：地址[GPT-SoVITS/github](https://github.com/RVC-Boss/GPT-SoVITS)

 该项目使用MIT协议

 [整合包、模型下载](https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e/dkxgpiy9zb96hob4#KTvnO)
1. 需要将整个GPT-SoVITS整合包解压并放在GPTvts目录下，才能使用，例如path\nieTTS2.0\GPTvts\GPT-SoVITS-v4-20250422fix
2. 必须要有音频参考文件，目录结构如下path\nieTTS2.0\GPTvts_voices\人物\中立\【中立】我不明白，为什么大家都在谈论着。项羽被困垓下，仿佛在中原古战场。.wav
3. 音频参考文件命名规范【语气】音频实际干声台词.wav
4. 使用的大模型和微调模型都放在models目录下，这样才能被加载出来
5. 启动本地推理服务
6. 选择所需的模型和参考音频
7. 调整参数进行推理

### index TTS
该服务使用了哔哩哔哩的开源项目indexTTS,项目地址：[indexTTS](https://github.com/index-tts/index-tts)

IndexTTS 是一种主要基于 XTTS 和 Tortoise 的 GPT 风格的文本转语音 （TTS） 模型。
该项目使用Apache-2.0 License开源协议

1. 使用该服务只需下载需要的模型即可

***下载模型***

使用镜像源
```
    set HF_ENDPOINT=https://hf-mirror.com
```

模型下载

```
    huggingface-cli download IndexTeam/IndexTTS-1.5 config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab --local-dir checkpoints --revision main
```
或者直接运行`下载模型.bat`

2. 同样需要选择GPTvts_voices/目录下的音频参考文件，indexTTS和GPT-SoVITS共享音频参考文件
3. 点击启动服务
### RVC 变声

1. 启动 RVC 服务
2. 选择变声模型
3. 调整音调等参数
4. 开启实时变声

## 配置文件说明

- `config.json` - 基础配置
- `configs/config.json` - RVC 变声器配置
- `GPT-SoVITS/config.py` - GPT-SoVITS 配置

## 注意事项

1. 首次使用需下载相应模型文件
2. GPU 加速需要 CUDA 支持
<<<<<<< HEAD
3. 音频设备建议使用虚拟声卡。
=======
3. 音频设备建议使用虚拟声卡
>>>>>>> d8ac5318321c1d755230f51377a34313879e25b0

## 技术支持

如有问题请提交 Issue。

## 许可证

本项目基于 [LICENSE](LICENSE) 开源协议。

## 致谢

- Edge-TTS
- 阿里百炼
- GPT-SoVITS
- index-tts
- RVC
