import asyncio
import logging
import numpy as np
from PySide6.QtCore import QObject, Signal
from PySide6.QtMultimedia import QAudioSource, QAudioFormat, QMediaDevices

logger = logging.getLogger(__name__)


class GuiAudioInput(QObject):
    stt_result_ready = Signal(str)
    level_changed = Signal(float)

    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self._audio_source: QAudioSource | None = None
        self._io_device = None
        self._vad = None
        self._recording = False
        self._device_name = ""
        self._stt_tasks: set[asyncio.Task] = set()

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

        rms = float(np.sqrt(np.mean(samples_f32**2))) if len(samples_f32) > 0 else 0.0
        self.level_changed.emit(min(1.0, rms * 10.0))

        if self._vad is None:
            return
        self._vad.accept_waveform(samples_f32)
        self._process_segments()

    def _process_segments(self):
        if self._vad is None:
            return
        while not self._vad.empty():
            seg = self._vad.front
            task = asyncio.create_task(self._run_stt(seg.samples, seg.sample_rate))
            self._stt_tasks.add(task)
            task.add_done_callback(self._stt_tasks.discard)
            self._vad.pop()

    async def _run_stt(self, samples, sample_rate: int):
        try:
            result = await self.bridge.transcribe_audio(samples, sample_rate)
            if result.is_success and result.text:
                self.stt_result_ready.emit(result.text)
                await self.bridge.submit_stt_text(result.text)
        except Exception as e:
            logger.error("GUI STT 处理异常: %s", e)
