from PySide6.QtCore import Qt, Signal, QSize, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
)

# SVG icon paths (stroke-based, 24x24 viewBox, matching Element Plus style)
_SVG_HOUSE = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M15 21V13a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/>
  <path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 0-1 1H4a1 1 0 0 0-1-1Z"/>
</svg>'''

_SVG_GEAR = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="3"/>
  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33
    1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06
    a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09
    A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9
    4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l
    .06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0
    4h-.09a1.65 1.65 0 0 0-1.51 1Z"/>
</svg>'''

_SVG_DOCUMENT = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/>
  <path d="M14 2v6h6"/>
  <path d="M16 13H8"/>
  <path d="M16 17H8"/>
  <path d="M10 9H8"/>
</svg>'''

_SVG_INFO = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <path d="M12 16v-4"/>
  <path d="M12 8h.01"/>
</svg>'''

_SVG_LOGO = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 3v18"/>
  <path d="M8 7v10"/>
  <path d="M4 10v4"/>
  <path d="M16 5v14"/>
  <path d="M20 8v8"/>
</svg>'''

_SVG_CHEVRON_LEFT = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m15 6-6 6 6 6"/>
</svg>'''

_SVG_CHEVRON_RIGHT = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m9 6 6 6-6 6"/>
</svg>'''


def _svg_icon(svg_data: bytes, color: str = "#6b6a68", size: int = 20) -> QIcon:
    """Render SVG bytes to a QIcon with the given color."""
    svg = svg_data.replace(b"currentColor", color.encode())
    renderer = QSvgRenderer(QByteArray(svg))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


class _NavButton(QPushButton):
    def __init__(self, svg_data: bytes, label: str, parent=None):
        super().__init__(parent)
        self._svg_data = svg_data
        self._label_text = label
        self._active = False
        self._collapsed = False
        self.setObjectName("nav_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(44)
        self.setIconSize(QSize(20, 20))
        self._update_appearance()

    def set_active(self, active: bool):
        self._active = active
        self.setProperty("active", str(active).lower())
        self.style().unpolish(self)
        self.style().polish(self)
        self._update_appearance()

    def set_collapsed(self, collapsed: bool):
        self._collapsed = collapsed
        self._update_appearance()

    def _update_appearance(self):
        color = "#d6608a" if self._active else "#6b6a68"
        icon = _svg_icon(self._svg_data, color)
        self.setIcon(icon)
        if self._collapsed:
            self.setText("")
        else:
            self.setText(f"  {self._label_text}")


class Sidebar(QFrame):
    page_changed = Signal(int)
    collapse_changed = Signal(bool)

    NAV_ITEMS = [
        (_SVG_HOUSE, "主页"),
        (_SVG_GEAR, "设置"),
        (_SVG_DOCUMENT, "日志"),
        (_SVG_INFO, "关于"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self._collapsed = False
        self._current = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(4)

        logo_row = QHBoxLayout()
        logo_row.setSpacing(10)
        logo_icon = QLabel()
        logo_pixmap = QPixmap(32, 32)
        logo_pixmap.fill(Qt.GlobalColor.transparent)
        p = QPainter(logo_pixmap)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        renderer = QSvgRenderer(QByteArray(_SVG_LOGO))
        renderer.render(p)
        p.end()
        logo_icon.setPixmap(logo_pixmap)
        logo_icon.setFixedSize(32, 32)
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_icon.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            "stop:0 #d6608a, stop:1 #9a6ad6);"
            "border-radius: 8px;"
        )
        logo_row.addWidget(logo_icon)
        self._logo_label = QLabel("nieTTS")
        self._logo_label.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #1a1a1a; background: transparent;"
        )
        logo_row.addWidget(self._logo_label)
        logo_row.addStretch()
        layout.addLayout(logo_row)

        layout.addSpacing(20)

        self._nav_buttons: list[_NavButton] = []
        for svg_data, label in self.NAV_ITEMS:
            btn = _NavButton(svg_data, label, self)
            btn.clicked.connect(lambda checked, b=btn, i=len(self._nav_buttons): self._on_nav(i))
            layout.addWidget(btn)
            self._nav_buttons.append(btn)

        layout.addStretch()

        self._collapse_btn = QPushButton(self)
        self._collapse_btn.setObjectName("secondary_btn")
        self._collapse_btn.setFixedSize(36, 36)
        self._collapse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._collapse_btn.setIconSize(QSize(16, 16))
        self._collapse_btn.setIcon(_svg_icon(_SVG_CHEVRON_LEFT, "#6b6a68"))
        self._collapse_btn.clicked.connect(self._toggle_collapse)
        collapse_row = QHBoxLayout()
        collapse_row.addStretch()
        collapse_row.addWidget(self._collapse_btn)
        collapse_row.addStretch()
        layout.addLayout(collapse_row)

        layout.addSpacing(8)
        self._set_active(0)

    def _on_nav(self, index: int):
        self._set_active(index)
        self.page_changed.emit(index)

    def _set_active(self, index: int):
        self._current = index
        for i, btn in enumerate(self._nav_buttons):
            btn.set_active(i == index)

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self.setFixedWidth(64)
            self._logo_label.hide()
            self._collapse_btn.setIcon(_svg_icon(_SVG_CHEVRON_RIGHT, "#6b6a68"))
        else:
            self.setFixedWidth(220)
            self._logo_label.show()
            self._collapse_btn.setIcon(_svg_icon(_SVG_CHEVRON_LEFT, "#6b6a68"))
        for btn in self._nav_buttons:
            btn.set_collapsed(self._collapsed)
        self.collapse_changed.emit(self._collapsed)
