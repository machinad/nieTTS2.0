"""OpenXR 覆盖层测试 UI。

包含射线交汇坐标显示、交互测试按钮、准星绘制。
用于验证 OpenXR 射线交互、坐标映射、事件处理等功能。
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen
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

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class OpenXRTestWidget(QWidget):
    """OpenXR 覆盖层测试 UI。

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

    def __init__(self, manager=None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._manager = manager
        self._click_count = 0

        # 准星状态
        self._crosshair_x = 0.0
        self._crosshair_y = 0.0
        self._ray_active = False

        self._setup_ui()
        self._apply_styles()

    # ── UI 构建 ──

    def _setup_ui(self) -> None:
        """构建测试 UI。"""
        self.setFixedSize(800, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        # 标题栏
        main_layout.addWidget(self._create_title_bar())
        main_layout.addWidget(self._create_separator())

        # 射线调试信息
        main_layout.addWidget(self._create_ray_debug_panel())

        # 交互测试按钮
        main_layout.addWidget(self._create_button_panel())

        # 滑块测试
        main_layout.addWidget(self._create_slider_panel())

        main_layout.addStretch()

        # 底部状态栏
        main_layout.addWidget(self._create_footer())

    def _create_title_bar(self) -> QFrame:
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("nieTTS 2.0 — OpenXR Overlay Test")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(title)

        layout.addStretch()

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(36, 36)
        btn_close.setObjectName("btn_close")
        btn_close.clicked.connect(self.close_requested.emit)
        layout.addWidget(btn_close)

        return frame

    def _create_separator(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: #404040;")
        return line

    def _create_ray_debug_panel(self) -> QFrame:
        """射线调试信息面板。"""
        frame = QFrame()
        frame.setObjectName("ray_panel")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        title = QLabel("射线调试信息")
        title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(title)

        # 第一行：状态 + 触发
        row1 = QHBoxLayout()
        self._ray_status_label = QLabel("状态: 未命中 ✗")
        self._ray_status_label.setFont(QFont("Microsoft YaHei", 10))
        self._ray_status_label.setStyleSheet("color: #ff7070;")
        row1.addWidget(self._ray_status_label)

        row1.addStretch()

        self._trigger_label = QLabel("触发: 释放")
        self._trigger_label.setFont(QFont("Consolas", 10))
        self._trigger_label.setStyleSheet("color: #a0a0a0;")
        row1.addWidget(self._trigger_label)
        layout.addLayout(row1)

        # 第二行：UV + 距离
        row2 = QHBoxLayout()
        self._uv_label = QLabel("UV: (-, -)")
        self._uv_label.setFont(QFont("Consolas", 10))
        self._uv_label.setStyleSheet("color: #70c0ff;")
        row2.addWidget(self._uv_label)

        row2.addStretch()

        self._distance_label = QLabel("距离: -")
        self._distance_label.setFont(QFont("Consolas", 10))
        self._distance_label.setStyleSheet("color: #70c0ff;")
        row2.addWidget(self._distance_label)
        layout.addLayout(row2)

        # 第三行：像素坐标
        row3 = QHBoxLayout()
        self._pixel_label = QLabel("像素: (-, -)")
        self._pixel_label.setFont(QFont("Consolas", 10))
        self._pixel_label.setStyleSheet("color: #70ff70;")
        row3.addWidget(self._pixel_label)

        row3.addStretch()

        # 帧计数
        self._frame_label = QLabel("帧: 0")
        self._frame_label.setFont(QFont("Consolas", 9))
        self._frame_label.setStyleSheet("color: #606060;")
        row3.addWidget(self._frame_label)
        layout.addLayout(row3)

        return frame

    def _create_button_panel(self) -> QFrame:
        """交互测试按钮面板。"""
        frame = QFrame()
        frame.setObjectName("button_panel")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        title = QLabel("交互测试")
        title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(title)

        # 第一行按钮
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        btn_tts = QPushButton("测试 TTS")
        btn_tts.setObjectName("btn_tts")
        btn_tts.setFixedHeight(40)
        btn_tts.clicked.connect(self._on_tts_click)
        row1.addWidget(btn_tts)

        btn_count = QPushButton("计数 +1")
        btn_count.setObjectName("btn_count")
        btn_count.setFixedHeight(40)
        btn_count.clicked.connect(self._on_count_click)
        row1.addWidget(btn_count)

        layout.addLayout(row1)

        # 第二行按钮
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        btn_settings = QPushButton("设置")
        btn_settings.setObjectName("btn_settings")
        btn_settings.setFixedHeight(40)
        btn_settings.clicked.connect(self.settings_requested.emit)
        row2.addWidget(btn_settings)

        btn_reset = QPushButton("重置计数")
        btn_reset.setObjectName("btn_reset")
        btn_reset.setFixedHeight(40)
        btn_reset.clicked.connect(self._on_reset_click)
        row2.addWidget(btn_reset)

        layout.addLayout(row2)

        # 点击计数
        click_row = QHBoxLayout()
        click_label = QLabel("点击次数:")
        click_label.setStyleSheet("color: #a0a0a0;")
        click_row.addWidget(click_label)

        self._click_count_label = QLabel("0")
        self._click_count_label.setFont(QFont("Consolas", 10))
        self._click_count_label.setStyleSheet("color: #70ff70;")
        click_row.addWidget(self._click_count_label)
        click_row.addStretch()

        layout.addLayout(click_row)

        return frame

    def _create_slider_panel(self) -> QFrame:
        """滑块测试面板。"""
        frame = QFrame()
        frame.setObjectName("slider_panel")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        title = QLabel("滑块测试")
        title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(title)

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
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 4, 0, 0)

        text = QLabel("OpenXR 射线交互测试界面 — 感应式手柄射线")
        text.setFont(QFont("Microsoft YaHei", 9))
        text.setStyleSheet("color: #606060;")
        layout.addWidget(text)

        layout.addStretch()

        version = QLabel("v2.0.0")
        version.setStyleSheet("color: #505050;")
        layout.addWidget(version)

        return frame

    def _apply_styles(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2e;
                color: #e0e0e0;
            }
            QFrame#ray_panel, QFrame#button_panel, QFrame#slider_panel {
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

    # ── 准星绘制 ──

    def paintEvent(self, event) -> None:  # noqa: N802
        """绘制准星（红色十字 + 圆圈）。"""
        super().paintEvent(event)

        if not self._ray_active:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        x = self._crosshair_x
        y = self._crosshair_y

        # 半透明背景圆
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 50, 50, 40)))
        painter.drawEllipse(QPointF(x, y), 20, 20)

        # 红色十字
        pen = QPen(QColor(255, 50, 50), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(x - 15, y, x + 15, y)
        painter.drawLine(x, y - 15, x, y + 15)

        # 圆圈
        painter.drawEllipse(QPointF(x, y), 10, 10)

        # 中心点
        painter.setBrush(QBrush(QColor(255, 50, 50)))
        painter.drawEllipse(QPointF(x, y), 2, 2)

        painter.end()

    # ── 公共接口（由 manager 调用）──

    def update_ray_status(self, hit: bool, u: float, v: float, distance: float) -> None:
        """更新射线状态显示。由 manager 每帧调用。"""
        self._ray_active = hit
        if hit:
            self._ray_status_label.setText("状态: 命中 ✓")
            self._ray_status_label.setStyleSheet("color: #70ff70;")
            self._uv_label.setText(f"UV: ({u:.3f}, {v:.3f})")
            self._distance_label.setText(f"距离: {distance:.2f}m")
        else:
            self._ray_status_label.setText("状态: 未命中 ✗")
            self._ray_status_label.setStyleSheet("color: #ff7070;")
            self._uv_label.setText("UV: (-, -)")
            self._distance_label.setText("距离: -")
            self._pixel_label.setText("像素: (-, -)")

    def update_crosshair_coord(self, x: float, y: float) -> None:
        """更新准星位置和像素坐标。由 manager 每帧调用。"""
        self._crosshair_x = x
        self._crosshair_y = y
        self._pixel_label.setText(f"像素: ({x:.0f}, {y:.0f})")
        self.update()

    def update_trigger_status(self, pressed: bool) -> None:
        """更新触发器状态。由 manager 每帧调用。"""
        if pressed:
            self._trigger_label.setText("触发: 按下")
            self._trigger_label.setStyleSheet("color: #ff7070;")
        else:
            self._trigger_label.setText("触发: 释放")
            self._trigger_label.setStyleSheet("color: #a0a0a0;")

    def increment_frame_count(self, count: int) -> None:
        """更新帧计数。"""
        self._frame_label.setText(f"帧: {count}")

    def mark_dirty(self) -> None:
        """通知 manager 需要重渲染。"""
        if self._manager is not None:
            self._manager.mark_dirty()

    # ── 槽函数 ──

    def _on_tts_click(self) -> None:
        self.tts_requested.emit("这是一段 OpenXR 覆盖层测试语音")
        self._update_status("TTS 请求已发送")
        self.mark_dirty()

    def _on_count_click(self) -> None:
        self._click_count += 1
        self._click_count_label.setText(str(self._click_count))
        self._update_status(f"点击计数: {self._click_count}")
        self.mark_dirty()

    def _on_reset_click(self) -> None:
        self._click_count = 0
        self._click_count_label.setText("0")
        self._update_status("计数已重置")
        self.mark_dirty()

    def _on_slider_change(self, value: int) -> None:
        self._slider_value.setText(str(value))
        self._progress.setValue(value)
        self._spin.blockSignals(True)
        self._spin.setValue(value)
        self._spin.blockSignals(False)
        self.slider_changed.emit(value)
        self.mark_dirty()

    def _on_spin_change(self, value: int) -> None:
        self._slider.blockSignals(True)
        self._slider.setValue(value)
        self._slider.blockSignals(False)
        self._progress.setValue(value)
        self._slider_value.setText(str(value))
        self.mark_dirty()

    def _update_status(self, text: str) -> None:
        """更新状态文本（可用于扩展）。"""
        logger.debug("状态: %s", text)
