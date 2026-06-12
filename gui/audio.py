import asyncio
import logging
import time
import numpy as np
from PySide6.QtCore import QObject, Signal
from PySide6.QtMultimedia import QAudioSource, QAudioFormat, QMediaDevices

logger = logging.getLogger(__name__)


class GuiAudioInput(QObject):
    level_changed = Signal(float, list)

    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self._audio_source: QAudioSource | None = None
        self._io_device = None
        self._vad = None
        self._recording = False
        self._device_name = ""
        self._last_level_time = 0  # 上次发送 level 的时间戳
        self._fft_frame_size = 2000  # FFT 帧大小
        self._sample_buffer = np.zeros(0, dtype=np.float32)  # 样本缓冲区

    def start_recording(self, device_name: str = ""):
        if self._recording:
            return

        from engines.stt.vad.silero_vad import SileroVAD
        vad_cfg = self.bridge.config.config.get("vad", {})
        self._vad = SileroVAD(
            model_path=vad_cfg.get("model_path", "models/silero_vad.onnx"),
            sample_rate=vad_cfg.get("sample_rate", 16000),
            threshold=vad_cfg.get("threshold", 0.5),
            min_silence_duration=vad_cfg.get("min_silence_duration", 0.25),
            min_speech_duration=vad_cfg.get("min_speech_duration", 0.25),
            max_speech_duration=vad_cfg.get("max_speech_duration", 15.0),
            window_size=vad_cfg.get("window_size", 512),
        )
        try:
            self._vad.preload()
            logger.info("VAD 模型预加载完成")
        except Exception as e:
            logger.error("VAD 模型加载失败: %s", e)
            self._vad = None

        fmt = QAudioFormat()
        fmt.setSampleRate(16000)
        fmt.setChannelCount(1)
        fmt.setSampleFormat(QAudioFormat.SampleFormat.Int16)

        target_device = None
        devices = QMediaDevices.audioInputs()
        if device_name:
            for d in devices:
                if d.description() == device_name:
                    target_device = d
                    break
        if target_device is None and devices:
            target_device = devices[0]

        if target_device is None:
            logger.error("未找到音频输入设备")
            return

        self._audio_source = QAudioSource(target_device, fmt)
        self._audio_source.setBufferSize(32000)  # 1秒缓冲区（16kHz * 2字节）
        self._io_device = self._audio_source.start()
        if self._io_device:
            self._io_device.readyRead.connect(self._on_audio_data)
        self._recording = True
        self._device_name = device_name
        logger.info("GUI 录音开始: %s", target_device.description())

    def stop_recording(self):
        if not self._recording:
            return
        self._recording = False
        self._sample_buffer = np.zeros(0, dtype=np.float32)  # 清空样本缓冲区

        if self._audio_source:
            self._audio_source.stop()
            self._audio_source = None
            self._io_device = None

        if self._vad is not None:
            self._vad.flush()
            self._process_segments()
            self._vad = None

        logger.info("GUI 录音停止")

    def _on_audio_data(self):
        if not self._io_device or not self._recording:
            return
        from PySide6.QtCore import QByteArray
        data: QByteArray = self._io_device.readAll()
        if data.isEmpty():
            return

        raw = bytes(data)
        samples_int16 = np.frombuffer(raw, dtype=np.int16)
        samples_f32 = samples_int16.astype(np.float32) / 32768.0

        # 将新数据添加到缓冲区
        self._sample_buffer = np.concatenate([self._sample_buffer, samples_f32])

        # 当缓冲区达到2000个样本时进行FFT分析
        while len(self._sample_buffer) >= self._fft_frame_size:
            # 取出2000个样本
            frame = self._sample_buffer[:self._fft_frame_size]
            self._sample_buffer = self._sample_buffer[self._fft_frame_size:]

            # 限制 level 信号发送频率到 16fps（约62.5ms）
            current_time = time.time() * 1000  # 转换为毫秒
            if current_time - self._last_level_time >= 62.5:  # 62.5ms = 16fps
                self._last_level_time = current_time
                
                rms = float(np.sqrt(np.mean(frame**2)))
                
                # RMS 太小则跳过 FFT，直接输出全零
                silence_threshold = 0.005
                if rms < silence_threshold:
                    self.level_changed.emit(0.0, [0.0] * 30)
                    continue
                
                # FFT 分析
                fft_data = np.abs(np.fft.rfft(frame))
                fft_data = fft_data[:len(fft_data)//2]  # 只取前半部分（有效频率）
                if np.max(fft_data) > 0:
                    fft_data = fft_data / np.max(fft_data)  # 归一化到 0-1
                
                # 采样范围：第9-39个bin（72Hz-316Hz）
                start_bin = 9
                end_bin = 39
                fft_data_trimmed = fft_data[start_bin:end_bin]  # 30个bin
                
                # 只基于关心的bin进行归一化
                if np.max(fft_data_trimmed) > 0:
                    fft_data_trimmed = fft_data_trimmed / np.max(fft_data_trimmed)
                
                # 放大系数
                amplify_factor = 1.5
                freq_levels = [min(1.0, float(x) * amplify_factor) for x in fft_data_trimmed]
                
                self.level_changed.emit(min(1.0, rms * 20.0), freq_levels)

        if self._vad is None:
            return
        self._vad.accept_waveform(samples_f32)
        self._process_segments()

    def _process_segments(self):
        if self._vad is None:
            return
        cfg = self.bridge.config.config
        while not self._vad.empty():
            seg = self._vad.front
            asyncio.ensure_future(self.bridge.pipeline.submit(
                audio_samples=seg.samples,
                sample_rate=seg.sample_rate,
                translate=cfg.get("isTranslate"),
                play_audio=cfg.get("isPlayAudio"),
                play_translation=cfg.get("isPlayTranslation"),
                osc_enabled=cfg.get("osc_enabled"),
                source_lang=cfg.get("source_lang"),
                target_lang=cfg.get("target_lang"),
            ))
            self._vad.pop()
