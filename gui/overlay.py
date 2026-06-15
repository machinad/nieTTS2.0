import logging
from PySide6.QtCore import Qt, Signal, QEvent, QTimer
from PySide6.QtGui import QColor, QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame,
    QApplication, QGraphicsDropShadowEffect,
)

logger = logging.getLogger(__name__)

_OVERLAY_WIDTH = 460
_TOP_MARGIN = 60


class OverlayInput(QWidget):
    """Semi-transparent overlay input for quick TTS text submission."""

    submit_text = Signal(str, dict)

    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self._bridge = bridge
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._setup_ui()
        self.hide()

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self._card = QFrame()
        self._card.setObjectName("overlay_card")
        self._card.setFixedWidth(_OVERLAY_WIDTH)

        shadow = QGraphicsDropShadowEffect(self._card)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self._card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(16, 12, 16, 12)
        card_layout.setSpacing(0)

        self._input = QLineEdit()
        self._input.setObjectName("overlay_input")
        self._input.setPlaceholderText("输入要合成的文本...  Enter 发送  |  Esc 关闭")
        self._input.setFixedHeight(40)
        self._input.installEventFilter(self)
        card_layout.addWidget(self._input)

        outer.addWidget(self._card, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._apply_styles()

    def _apply_styles(self):
        self._card.setStyleSheet(
            "QFrame#overlay_card {"
            "  background-color: rgba(255, 255, 255, 0.85);"
            "  border: 1px solid rgba(255, 255, 255, 0.4);"
            "  border-radius: 14px;"
            "}"
        )
        self._input.setStyleSheet(
            "QLineEdit#overlay_input {"
            "  border: none;"
            "  background: transparent;"
            "  font-size: 15px;"
            "  padding: 0 4px;"
            "  color: #1a1a1a;"
            "  selection-background-color: rgba(214, 96, 138, 0.2);"
            "}"
        )

    def show_overlay(self):
        """Show overlay: clear text, focus, position at top-center of current screen."""
        self._input.clear()
        self._reposition()
        self.show()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        QTimer.singleShot(0, self._input.setFocus)

    def _reposition(self):
        """Position overlay at top-center of the screen under the cursor."""
        screen = QApplication.screenAt(QCursor.pos()) or QApplication.primaryScreen()
        geo = screen.geometry()
        total_w = _OVERLAY_WIDTH + 32
        total_h = self._card.sizeHint().height() + 24
        x = geo.x() + (geo.width() - total_w) // 2
        y = geo.y() + _TOP_MARGIN
        self.setGeometry(x, y, total_w, total_h)

    def eventFilter(self, obj, event):
        if obj is self._input and event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self._on_submit()
                return True
            if key == Qt.Key.Key_Escape:
                self._defer_hide()
                return True
        return super().eventFilter(obj, event)

    def focusOutEvent(self, event):
        """Hide overlay when focus is lost (clicking outside)."""
        QTimer.singleShot(50, self._check_focus_on_blur)
        super().focusOutEvent(event)

    def _check_focus_on_blur(self):
        if self.isVisible() and not self.isActiveWindow():
            self.hide()

    def _on_submit(self):
        text = self._input.text().strip()
        if not text:
            self._defer_hide()
            return
        opts = self._build_opts()
        self._defer_hide()
        self.submit_text.emit(text, opts)
        logger.info("覆盖层提交: %s", text[:40])

    def _defer_hide(self):
        """Hide after the current event is fully consumed by Qt."""
        QTimer.singleShot(0, self.hide)

    def _build_opts(self) -> dict:
        return self._bridge.build_submit_opts()
