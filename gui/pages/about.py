from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
)

from version import VERSION

_SVG_LOGO = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 3v18"/>
  <path d="M8 7v10"/>
  <path d="M4 10v4"/>
  <path d="M16 5v14"/>
  <path d="M20 8v8"/>
</svg>'''


def _card(title: str) -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setProperty("class", "card")
    card.setObjectName("card")
    lay = QVBoxLayout(card)
    lay.setContentsMargins(20, 16, 20, 20)
    lay.setSpacing(14)
    header = QHBoxLayout()
    ttl = QLabel(title)
    ttl.setStyleSheet("font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent;")
    header.addWidget(ttl)
    header.addStretch()
    lay.addLayout(header)
    return card, lay


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("关于")
        title.setObjectName("page_title")
        root.addWidget(title)

        hero = QFrame()
        hero.setStyleSheet(
            "QFrame { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            "stop:0 #ffffff, stop:1 #f0eeeb);"
            "border: 1px solid rgba(0,0,0,0.04); border-radius: 20px; }"
        )
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(40, 36, 40, 36)
        hero_layout.setSpacing(12)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(64, 64)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        p = QPainter(pixmap)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        QSvgRenderer(QByteArray(_SVG_LOGO)).render(p)
        p.end()
        icon_lbl.setPixmap(pixmap)
        icon_lbl.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            "stop:0 #d6608a, stop:1 #9a6ad6);"
            "border-radius: 16px;"
        )
        hero_layout.addWidget(icon_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        name_lbl = QLabel("nieTTS 2.0")
        name_lbl.setStyleSheet(
            "font-size: 24px; font-weight: 700; color: #1a1a1a; letter-spacing: -0.02em;"
        )
        hero_layout.addWidget(name_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        ver_lbl = QLabel(VERSION)
        ver_lbl.setStyleSheet(
            "font-family: 'Consolas', monospace; font-size: 13px; color: #d6608a; font-weight: 500;"
        )
        hero_layout.addWidget(ver_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        desc_lbl = QLabel("一体化 TTS + STT + 翻译工具")
        desc_lbl.setStyleSheet("font-size: 14px; color: #6b6a68;")
        hero_layout.addWidget(desc_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        root.addWidget(hero)

        stack_card, stack_l = _card("技术栈")
        for label, value in [
            ("GUI", "PySide6 + qasync"),
            ("前端", "Vue 3 + Element Plus + Vite"),
            ("后端", "Python Quart + Hypercorn"),
            ("通信", "WebSocket 实时通信"),
        ]:
            row = QHBoxLayout()
            row.setSpacing(16)
            lbl = QLabel(label)
            lbl.setFixedWidth(48)
            lbl.setStyleSheet(
                "font-size: 12px; font-weight: 600; color: #9b9a98;"
            )
            row.addWidget(lbl)
            val = QLabel(value)
            val.setStyleSheet("font-size: 14px; color: #1a1a1a;")
            row.addWidget(val)
            stack_l.addLayout(row)
        root.addWidget(stack_card)

        root.addStretch()
