import logging
import asyncio
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
)

from gui.widgets.sidebar import Sidebar
from gui.widgets.header import Header
from gui.pages.home import HomePage
from gui.pages.settings import SettingsPage
from gui.pages.logs import LogsPage
from gui.pages.about import AboutPage
from gui.audio import GuiAudioInput
from gui.log_handler import QtLogHandler

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, bridge, log_handler: QtLogHandler, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self.log_handler = log_handler
        self.setWindowTitle("nieTTS 2.0")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

        self._audio = GuiAudioInput(bridge)
        self._audio.level_changed.connect(self._on_audio_level)

        self._setup_ui()
        self._connect_signals()
        self.bridge.stt_result_ready.connect(self._on_stt_result)

        loop = asyncio.get_event_loop()
        loop.call_soon(self._init_async)

    def closeEvent(self, event):
        self._audio.stop_recording()
        loop = asyncio.get_event_loop()
        loop.call_soon(loop.stop)
        event.accept()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._sidebar = Sidebar()
        main_layout.addWidget(self._sidebar)

        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(0)

        self._header = Header(self.bridge)
        right.addWidget(self._header)

        self._stack = QStackedWidget()
        self._stack.setStyleSheet("QStackedWidget { background: #f5f3f0; }")

        self._home_page = HomePage(self.bridge)
        self._settings_page = SettingsPage(self.bridge)
        self._logs_page = LogsPage()
        self._about_page = AboutPage()

        self._stack.addWidget(self._home_page)
        self._stack.addWidget(self._settings_page)
        self._stack.addWidget(self._logs_page)
        self._stack.addWidget(self._about_page)

        right.addWidget(self._stack)
        main_layout.addLayout(right)

    def _connect_signals(self):
        self._sidebar.page_changed.connect(self._stack.setCurrentIndex)

        self.log_handler.log_received.connect(self._on_log)

        self._home_page.request_send.connect(self._on_send_tts)
        self._home_page.recording_started.connect(self._start_recording)
        self._home_page.recording_stopped.connect(self._stop_recording)

    def _init_async(self):
        asyncio.create_task(self._load_config_and_status())

    async def _load_config_and_status(self):
        try:
            self._settings_page.refresh_models_status()
        except Exception as e:
            logger.error("加载模型状态失败: %s", e)

    def _on_log(self, level: str, message: str):
        self._home_page.append_log(level, message)
        self._logs_page.append_log(level, message)

    def _on_send_tts(self, text: str, opts: dict):
        async def _do():
            try:
                req_id = await self.bridge.submit_tts(text, **opts)
                logger.info("请求已提交: %s", req_id)
            except Exception as e:
                logger.error("发送失败: %s", e)
        asyncio.create_task(_do())

    def _start_recording(self):
        cfg = self.bridge.get_config()
        device_name = cfg.get("gui_input_device", "")
        self._audio.start_recording(device_name)

    def _stop_recording(self):
        self._audio.stop_recording()

    def _on_stt_result(self, text: str):
        logger.info("STT 识别结果: %s", text)

    def _on_audio_level(self, level: float, freq_levels: list):
        self._home_page.update_waveform(level, freq_levels)
