from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QPushButton

from gui.widgets.utils import svg_icon

_SVG_COPY = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
  <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
</svg>"""

_SVG_CHECK = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#3da85c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="20 6 9 17 4 12"/>
</svg>"""


class Header(QFrame):
    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self.setObjectName("header")
        self.setFixedHeight(56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(12)

        self._title = QLabel("nieTTS 2.0")
        self._title.setObjectName("header_title")
        layout.addWidget(self._title)

        separator = QLabel("|")
        separator.setStyleSheet("color: #c5c4c2; font-size: 14px; background: transparent;")
        layout.addWidget(separator)

        self._url_label = QLabel()
        self._url_label.setStyleSheet(
            "font-family: 'JetBrains Mono', 'Consolas', monospace; "
            "font-size: 12px; color: #d6608a; background: transparent;"
        )
        layout.addWidget(self._url_label)

        self._copy_btn = QPushButton()
        self._copy_btn.setObjectName("secondary_btn")
        self._copy_btn.setFixedSize(28, 28)
        self._copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._copy_btn.setIconSize(QSize(14, 14))
        self._copy_btn.setIcon(svg_icon(_SVG_COPY, "#6b6a68"))
        self._copy_btn.clicked.connect(self._copy_to_clipboard)
        layout.addWidget(self._copy_btn)

        layout.addStretch()

    def update_web_url(self):
        ip = self.bridge.ip_address
        port = self.bridge.web_port
        self._url_label.setText(f"web面板地址(可跨设备访问): https://{ip}:{port}")

    def _copy_to_clipboard(self):
        url = self._url_label.text().split(": ", 1)[-1] if ": " in self._url_label.text() else self._url_label.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(url)
        self._copy_btn.setIcon(svg_icon(_SVG_CHECK, "#3da85c"))
        QTimer.singleShot(1500, lambda: self._copy_btn.setIcon(svg_icon(_SVG_COPY, "#6b6a68")))
