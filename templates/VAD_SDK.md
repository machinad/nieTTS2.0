# VAD Web 本地化开发文档

基于 `@ricky0123/vad-web` 的浏览器端语音活动检测方案。

## 文件清单

| 文件 | 版本 | 大小 | 说明 |
|------|------|------|------|
| `ort.min.js` | 1.14.0 | ~550KB | ONNX Runtime Web 运行时 |
| `ort-wasm-simd.wasm` | 1.14.0 | ~10MB | WebAssembly 二进制文件 |
| `vad.bundle.min.js` | 0.0.18 | ~17KB | VAD 核心库 |
| `vad.worklet.bundle.min.js` | 0.0.18 | ~10KB | AudioWorklet 模块 |
| `silero_vad.onnx` | - | ~1.8MB | Silero VAD 模型文件 |

**依赖关系：** `vad-web 0.0.18` 依赖 `onnxruntime-web ^1.14.0`，版本需匹配。

## 基本用法

### 1. 引入文件

```html
<script src="ort.min.js"></script>
<script src="vad.bundle.min.js"></script>
<script>
  // 配置 WASM 路径
  ort.env.wasm.wasmPaths = './';
</script>
```

### 2. 初始化

```javascript
const myvad = await vad.MicVAD.new({
  workletURL: 'vad.worklet.bundle.min.js',
  modelURL: 'silero_vad.onnx',
  onSpeechStart: () => {
    console.log('检测到语音开始');
  },
  onSpeechEnd: (audio) => {
    // audio: Float32Array, 16kHz 单声道
    console.log('语音结束，采样数:', audio.length);
  }
});
```

### 3. 控制检测

```javascript
myvad.start();  // 开始检测
myvad.pause();  // 暂停检测
```

## API 参考

### `vad.MicVAD.new(options)`

创建 VAD 实例。

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `workletURL` | string | 自动检测 | worklet 文件路径 |
| `modelURL` | string | 自动检测 | ONNX 模型文件路径 |
| `onSpeechStart` | function | - | 语音开始回调 |
| `onSpeechEnd` | function | - | 语音结束回调，参数为 `Float32Array` |
| `onFrameProcessed` | function | - | 每帧处理回调，参数为 `{ isSpeech: number }` |
| `onVADMisfire` | function | - | 误触发回调 |
| `positiveSpeechThreshold` | number | 0.5 | 语音检测阈值 (0-1)，越高越严格 |
| `negativeSpeechThreshold` | number | 0.35 | 非语音检测阈值 |
| `redemptionFrames` | number | 8 | 语音结束后保留帧数 |
| `minSpeechFrames` | number | 3 | 最小语音帧数，过滤短噪音 |
| `frameSamples` | number | 1536 | 每帧采样数，可选 512/1024/1536 |

**返回：** Promise<MicVAD>

### 实例方法

| 方法 | 说明 |
|------|------|
| `start()` | 开始语音检测 |
| `pause()` | 暂停语音检测 |

## 音频数据格式

- **采样率：** 16000 Hz
- **格式：** Float32Array
- **值范围：** [-1, 1]
- **声道：** 单声道

## 工具函数

### Float32Array 转 WAV

```javascript
function float32ToWav(float32Array, sampleRate = 16000) {
  const buffer = new ArrayBuffer(44 + float32Array.length * 2);
  const view = new DataView(buffer);
  
  const writeString = (view, offset, string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };
  
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + float32Array.length * 2, true);
  writeString(view, 8, 'WAVE');
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeString(view, 36, 'data');
  view.setUint32(40, float32Array.length * 2, true);
  
  for (let i = 0; i < float32Array.length; i++) {
    const s = Math.max(-1, Math.min(1, float32Array[i]));
    view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }
  
  return new Blob([buffer], { type: 'audio/wav' });
}

// 使用
const wavBlob = float32ToWav(audio);
const audioUrl = URL.createObjectURL(wavBlob);
new Audio(audioUrl).play();
```

### 计算时长

```javascript
const duration = audio.length / 16000; // 秒
```

## 集成到项目

### 文件放置

将所有文件放到项目的静态资源目录，例如：
```
public/
  └── vad/
      ├── ort.min.js
      ├── ort-wasm-simd.wasm
      ├── vad.bundle.min.js
      ├── vad.worklet.bundle.min.js
      └── silero_vad.onnx
```

### 路径配置

```javascript
// 配置 WASM 路径
ort.env.wasm.wasmPaths = '/vad/';

// 配置 worklet 和模型路径
const myvad = await vad.MicVAD.new({
  workletURL: '/vad/vad.worklet.bundle.min.js',
  modelURL: '/vad/silero_vad.onnx',
  // ...
});
```

## 注意事项

1. **HTTPS 要求**：麦克风 API 需要 HTTPS 或 localhost 环境
2. **文件完整性**：确保所有文件完整下载，特别是 WASM 文件（~10MB）
3. **首次加载**：模型和 WASM 加载需要时间，建议显示加载状态
4. **浏览器兼容**：需要支持 SIMD 的现代浏览器（Chrome 75+, Firefox 89+, Safari 14.1+, Edge 79+）
5. **内存释放**：长期不用时调用 `pause()` 释放资源

## 常见问题

### Q: 模型加载失败 "Unsupported model IR version"

A: 模型和 ONNX Runtime 版本不匹配。确保使用本文档指定的版本组合。

### Q: 找不到 WASM 文件

A: 检查 `ort.env.wasm.wasmPaths` 配置是否正确指向 WASM 文件所在目录。

### Q: 找不到 worklet 文件

A: 检查 `workletURL` 配置，路径相对于当前页面 URL。

### Q: 检测过于灵敏/不灵敏

A: 调整 `positiveSpeechThreshold`（提高更严格）和 `negativeSpeechThreshold` 参数。

## 参考链接

- [ricky0123/vad-web GitHub](https://github.com/ricky0123/vad-web)
- [ONNX Runtime Web](https://onnxruntime.ai/docs/build/web.html)
- [Silero VAD](https://github.com/snakers4/silero-vad)
