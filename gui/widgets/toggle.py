from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class ToggleSwitch(QWidget):
    toggled = Signal(bool)

    _TRACK_W = 44
    _TRACK_H = 24
    _THUMB_D = 18
    _PAD = 3  # thumb inset from track edge
    _ANIM_MS = 150

    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self._xPos = self._thumb_x(checked)
        self.setFixedSize(self._TRACK_W, self._TRACK_H)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._anim = QPropertyAnimation(self, b"xPos", self)
        self._anim.setDuration(self._ANIM_MS)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    # --- Property for animation ---
    def _get_xPos(self) -> float:
        return self._xPos

    def _set_xPos(self, v: float):
        self._xPos = v
        self.update()

    xPos = Property(float, fget=_get_xPos, fset=_set_xPos)

    # --- Geometry helpers ---
    def _thumb_x(self, checked: bool) -> float:
        """X position of thumb left edge."""
        if checked:
            return self._TRACK_W - self._THUMB_D - self._PAD
        return self._PAD

    # --- Public API ---
    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool):
        if self._checked == checked:
            return
        self._checked = checked
        target = self._thumb_x(checked)
        self._anim.stop()
        self._anim.setStartValue(self._xPos)
        self._anim.setEndValue(target)
        self._anim.start()
        self.toggled.emit(checked)

    def sizeHint(self):
        return QSize(self._TRACK_W, self._TRACK_H)

    # --- Events ---
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            target = self._thumb_x(self._checked)
            self._anim.stop()
            self._anim.setStartValue(self._xPos)
            self._anim.setEndValue(target)
            self._anim.start()
            self.toggled.emit(self._checked)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Track
        track_rect = self.rect()
        track_radius = self._TRACK_H / 2
        if self._checked:
            track_color = QColor("#d6608a")
        else:
            track_color = QColor("#e0ddd9")
        p.setBrush(track_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(track_rect, track_radius, track_radius)

        # Thumb
        thumb_y = (self._TRACK_H - self._THUMB_D) / 2
        thumb_rect_x = self._xPos
        thumb_rect = QRectF(thumb_rect_x, thumb_y, self._THUMB_D, self._THUMB_D)

        # Shadow (subtle)
        shadow = QColor(0, 0, 0, 30)
        p.setBrush(shadow)
        p.drawEllipse(thumb_rect.adjusted(0.5, 1, 0.5, 1))

        # Thumb circle
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(thumb_rect)

        p.end()
