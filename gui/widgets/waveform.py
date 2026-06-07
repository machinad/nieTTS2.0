import math
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QLinearGradient
from PySide6.QtWidgets import QWidget


class WaveformWidget(QWidget):
    BAR_COUNT = 48
    MAX_BAR_HEIGHT = 56

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)
        self.setMaximumHeight(80)
        self._levels = [0.0] * self.BAR_COUNT
        self._recording = False
        self._tick = 0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.setInterval(33)

    def set_recording(self, recording: bool):
        self._recording = recording
        if recording:
            self._timer.start()
        else:
            self._timer.stop()
            self._levels = [0.0] * self.BAR_COUNT
            self.update()

    def update_level(self, level: float):
        step = self._tick % self.BAR_COUNT
        for i in range(self.BAR_COUNT):
            dist = abs(i - step)
            wave = math.sin((self._tick * 0.15) + i * 0.3) * 0.3
            self._levels[i] = max(
                self._levels[i] * 0.85,
                level * max(0, 1.0 - dist * 0.04) + wave * level * 0.3,
            )

    def _animate(self):
        self._tick += 1
        for i in range(self.BAR_COUNT):
            self._levels[i] *= 0.92
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        bar_w = max(3, int(w / self.BAR_COUNT * 0.7))
        gap = (w - self.BAR_COUNT * bar_w) / max(1, self.BAR_COUNT - 1)
        y_base = h - 4

        accent = QColor("#d6608a")
        accent_dim = QColor("#d6608a")
        accent_dim.setAlpha(50)

        for i in range(self.BAR_COUNT):
            bar_h = max(2, int(self._levels[i] * self.MAX_BAR_HEIGHT))
            x = int(i * (bar_w + gap))
            y = y_base - bar_h

            grad = QLinearGradient(x, y, x, y_base)
            grad.setColorAt(0, accent)
            grad.setColorAt(1, accent_dim)
            painter.setBrush(grad)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, bar_w, bar_h, 2, 2)

        painter.end()
