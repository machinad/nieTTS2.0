import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter
from PySide6.QtWidgets import QWidget


class WaveformWidget(QWidget):
    BAR_COUNT = 30
    MAX_BAR_HEIGHT = 56

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)
        self.setMaximumHeight(80)
        self._levels = [0.0] * self.BAR_COUNT
        self._target_levels = [0.0] * self.BAR_COUNT
        self._recording = False
        self._tick = 0

        self._accent = QColor("#d6608a")
        self._accent_dim = QColor("#d6608a")
        self._accent_dim.setAlpha(50)

        self._grad_brush = QBrush(self._build_gradient())

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.setInterval(33)  # 30fps

    def _build_gradient(self):
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0, self._accent)
        grad.setColorAt(1, self._accent_dim)
        return grad

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._grad_brush = QBrush(self._build_gradient())

    def set_recording(self, recording: bool):
        self._recording = recording
        if recording:
            self._timer.start()
        else:
            self._timer.stop()
            self._levels = [0.0] * self.BAR_COUNT
            self._target_levels = [0.0] * self.BAR_COUNT
            self.update()

    def update_level(self, level: float, freq_levels: list = None):
        if freq_levels and len(freq_levels) >= self.BAR_COUNT:
            for i in range(self.BAR_COUNT):
                self._target_levels[i] = freq_levels[i]
        else:
            step = self._tick % self.BAR_COUNT
            for i in range(self.BAR_COUNT):
                dist = abs(i - step)
                wave = math.sin((self._tick * 0.15) + i * 0.3) * 0.3
                self._target_levels[i] = max(
                    self._target_levels[i] * 0.7,
                    level * max(0, 1.0 - dist * 0.04) + wave * level * 0.3,
                )

    def _animate(self):
        self._tick += 1
        for i in range(self.BAR_COUNT):
            if self._target_levels[i] > self._levels[i]:
                self._levels[i] += (self._target_levels[i] - self._levels[i]) * 0.3
            else:
                self._levels[i] *= 0.95
        if any(lv > 0.01 for lv in self._levels):
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        w = self.width()
        h = self.height()
        bar_w = max(3, int(w / self.BAR_COUNT * 0.7))
        gap = (w - self.BAR_COUNT * bar_w) / max(1, self.BAR_COUNT - 1)
        y_base = h - 4

        painter.setBrush(self._grad_brush)
        painter.setPen(Qt.PenStyle.NoPen)

        for i in range(self.BAR_COUNT):
            bar_h = max(2, int(self._levels[i] * self.MAX_BAR_HEIGHT))
            x = int(i * (bar_w + gap))
            painter.drawRect(x, y_base - bar_h, bar_w, bar_h)

        painter.end()
