"""VR 覆盖层测试 UI。

包含用于测试交互的按钮、状态显示、准星区域等。
用于验证 VR 射线交互、坐标映射、事件处理等功能。
"""

import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class VROverlayTestWidget(QWidget):
    """VR 覆盖层测试 UI。

    信号：
        tts_requested(str): TTS 测试请求
        settings_requested(): 设置请求
        close_requested(): 关闭请求
        slider_changed(int): 滑块值变化
    """

    tts_requested = Signal(str)
    settings_requested = Signal()
    close_requested = Signal()
    slider_changed = Signal(int)

    def __init__(self, manager=None, parent: QWidget | None = None):
        super().__init__(parent)
        self._manager = manager
        self._click_count = 0
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """构建测试 UI。"""
        self.setFixedSize(800, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        # ── 标题栏 ──
        title_bar = self._create_title_bar()
        main_layout.addWidget(title_bar)

        # ── 分隔线 ──
        main_layout.addWidget(self._create_separator())

        # ── 状态区域 ──
        status_area = self._create_status_area()
        main_layout.addWidget(status_area)

        # ── 测试按钮区域 ──
        button_area = self._create_button_area()
        main_layout.addWidget(button_area)

        # ── 滑块测试区域 ──
        slider_area = self._create_slider_area()
        main_layout.addWidget(slider_area)

        # ── 底部状态栏 ──
        main_layout.addStretch()
        footer = self._create_footer()
        main_layout.addWidget(footer)

    def _create_title_bar(self) -> QFrame:
        """创建标题栏。"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        # 标题
        title = QLabel("nieTTS 2.0 VR Overlay Test")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(title)

        layout.addStretch()

        # 关闭按钮
        self._btn_close = QPushButton("✕")
        self._btn_close.setFixedSize(36, 36)
        self._btn_close.setObjectName("btn_close")
        self._btn_close.clicked.connect(self.close_requested.emit)
        layout.addWidget(self._btn_close)

        return frame

    def _create_separator(self) -> QFrame:
        """创建分隔线。"""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: #404040;")
        return line

    def _create_status_area(self) -> QFrame:
        """创建状态显示区域。"""
        frame = QFrame()
        frame.setObjectName("status_frame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        # 状态标题
        status_title = QLabel("状态信息")
        status_title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        status_title.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(status_title)

        # 状态文本
        self._status_label = QLabel("就绪 - 等待 VR 交互...")
        self._status_label.setFont(QFont("Microsoft YaHei", 10))
        self._status_label.setStyleSheet("color: #c0c0c0;")
        layout.addWidget(self._status_label)

        # 坐标显示
        coord_layout = QHBoxLayout()
        coord_label = QLabel("准星坐标:")
        coord_label.setStyleSheet("color: #a0a0a0;")
        coord_layout.addWidget(coord_label)

        self._coord_label = QLabel("(0, 0)")
        self._coord_label.setFont(QFont("Consolas", 10))
        self._coord_label.setStyleSheet("color: #70c0ff;")
        coord_layout.addWidget(self._coord_label)
        coord_layout.addStretch()

        layout.addLayout(coord_layout)

        # 点击计数
        click_layout = QHBoxLayout()
        click_label = QLabel("点击次数:")
        click_label.setStyleSheet("color: #a0a0a0;")
        click_layout.addWidget(click_label)

        self._click_count_label = QLabel("0")
        self._click_count_label.setFont(QFont("Consolas", 10))
        self._click_count_label.setStyleSheet("color: #70ff70;")
        click_layout.addWidget(self._click_count_label)
        click_layout.addStretch()

        layout.addLayout(click_layout)

        return frame

    def _create_button_area(self) -> QFrame:
        """创建测试按钮区域。"""
        frame = QFrame()
        frame.setObjectName("button_frame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        # 按钮标题
        btn_title = QLabel("交互测试")
        btn_title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        btn_title.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(btn_title)

        # 第一行按钮
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        self._btn_tts = QPushButton("测试 TTS")
        self._btn_tts.setObjectName("btn_tts")
        self._btn_tts.setFixedHeight(40)
        self._btn_tts.clicked.connect(self._on_tts_click)
        row1.addWidget(self._btn_tts)

        self._btn_count = QPushButton("点击计数 +1")
        self._btn_count.setObjectName("btn_count")
        self._btn_count.setFixedHeight(40)
        self._btn_count.clicked.connect(self._on_count_click)
        row1.addWidget(self._btn_count)

        layout.addLayout(row1)

        # 第二行按钮
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        self._btn_settings = QPushButton("设置")
        self._btn_settings.setObjectName("btn_settings")
        self._btn_settings.setFixedHeight(40)
        self._btn_settings.clicked.connect(self.settings_requested.emit)
        row2.addWidget(self._btn_settings)

        self._btn_reset = QPushButton("重置计数")
        self._btn_reset.setObjectName("btn_reset")
        self._btn_reset.setFixedHeight(40)
        self._btn_reset.clicked.connect(self._on_reset_click)
        row2.addWidget(self._btn_reset)

        layout.addLayout(row2)

        return frame

    def _create_slider_area(self) -> QFrame:
        """创建滑块测试区域。"""
        frame = QFrame()
        frame.setObjectName("slider_frame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        # 滑块标题
        slider_title = QLabel("滑块测试")
        slider_title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        slider_title.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(slider_title)

        # 水平滑块
        slider_layout = QHBoxLayout()
        slider_label = QLabel("音量:")
        slider_label.setStyleSheet("color: #c0c0c0;")
        slider_layout.addWidget(slider_label)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(0, 100)
        self._slider.setValue(50)
        self._slider.valueChanged.connect(self._on_slider_change)
        slider_layout.addWidget(self._slider)

        self._slider_value = QLabel("50")
        self._slider_value.setFixedWidth(30)
        self._slider_value.setStyleSheet("color: #70c0ff;")
        slider_layout.addWidget(self._slider_value)

        layout.addLayout(slider_layout)

        # 进度条
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(50)
        self._progress.setFixedHeight(12)
        layout.addWidget(self._progress)

        # 数值输入框
        spin_layout = QHBoxLayout()
        spin_label = QLabel("数值:")
        spin_label.setStyleSheet("color: #c0c0c0;")
        spin_layout.addWidget(spin_label)

        self._spin = QSpinBox()
        self._spin.setRange(0, 100)
        self._spin.setValue(50)
        self._spin.valueChanged.connect(self._on_spin_change)
        spin_layout.addWidget(self._spin)
        spin_layout.addStretch()

        layout.addLayout(spin_layout)

        return frame

    def _create_footer(self) -> QFrame:
        """创建底部状态栏。"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 4, 0, 0)

        footer_text = QLabel("VR 覆盖层测试界面 - 使用控制器射线交互")
        footer_text.setFont(QFont("Microsoft YaHei", 9))
        footer_text.setStyleSheet("color: #606060;")
        layout.addWidget(footer_text)

        layout.addStretch()

        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #505050;")
        layout.addWidget(version)

        return frame

    def _apply_styles(self):
        """应用样式表。"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2e;
                color: #e0e0e0;
            }
            QFrame#status_frame, QFrame#button_frame, QFrame#slider_frame {
                background-color: #333336;
                border: 1px solid #404040;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #3c3c40;
                border: 1px solid #505050;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                color: #e0e0e0;
            }
            QPushButton:hover {
                background-color: #4a4a50;
                border-color: #606060;
            }
            QPushButton:pressed {
                background-color: #2a2a2e;
                border-color: #70c0ff;
            }
            QPushButton#btn_close {
                background-color: #c42b1c;
                border: none;
                font-size: 16px;
                color: white;
            }
            QPushButton#btn_close:hover {
                background-color: #e04030;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #404040;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                margin: -5px 0;
                background: #70c0ff;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #70c0ff;
                border-radius: 3px;
            }
            QProgressBar {
                border: 1px solid #404040;
                border-radius: 4px;
                background: #333336;
            }
            QProgressBar::chunk {
                background: #70c0ff;
                border-radius: 3px;
            }
            QSpinBox {
                background-color: #3c3c40;
                border: 1px solid #505050;
                border-radius: 4px;
                padding: 4px 8px;
                color: #e0e0e0;
            }
        """)

    # ── 槽函数 ──

    def _on_tts_click(self):
        """TTS 测试按钮点击。"""
        self.tts_requested.emit("这是一段 VR 覆盖层测试语音")
        self.update_status("TTS 请求已发送")
        if self._manager:
            self._manager.mark_dirty()

    def _on_count_click(self):
        """计数按钮点击。"""
        self._click_count += 1
        self._click_count_label.setText(str(self._click_count))
        self.update_status(f"点击计数: {self._click_count}")
        if self._manager:
            self._manager.mark_dirty()

    def _on_reset_click(self):
        """重置计数。"""
        self._click_count = 0
        self._click_count_label.setText("0")
        self.update_status("计数已重置")
        if self._manager:
            self._manager.mark_dirty()

    def _on_slider_change(self, value: int):
        """滑块值变化。"""
        self._slider_value.setText(str(value))
        self._progress.setValue(value)
        self._spin.blockSignals(True)
        self._spin.setValue(value)
        self._spin.blockSignals(False)
        self.slider_changed.emit(value)
        if self._manager:
            self._manager.mark_dirty()

    def _on_spin_change(self, value: int):
        """数值输入框变化。"""
        self._slider.blockSignals(True)
        self._slider.setValue(value)
        self._slider.blockSignals(False)
        self._progress.setValue(value)
        self._slider_value.setText(str(value))
        if self._manager:
            self._manager.mark_dirty()

    # ── 公共接口 ──

    def update_status(self, text: str):
        """更新状态文本。"""
        self._status_label.setText(text)
        if self._manager:
            self._manager.mark_dirty()

    def update_crosshair_coord(self, x: float, y: float):
        """更新准星坐标显示。"""
        self._coord_label.setText(f"({x:.0f}, {y:.0f})")
        if self._manager:
            self._manager.mark_dirty()
