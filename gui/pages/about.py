from PySide6.QtCore import QByteArray, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from version import VERSION

_SVG_LOGO = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 3v18"/>
  <path d="M8 7v10"/>
  <path d="M4 10v4"/>
  <path d="M16 5v14"/>
  <path d="M20 8v8"/>
</svg>"""

_SVG_LINK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
  <polyline points="15 3 21 3 21 9"/>
  <line x1="10" y1="14" x2="21" y2="3"/>
</svg>"""

_SVG_GITHUB = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"/>
</svg>"""

_SVG_MAIL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
  <polyline points="22,6 12,13 2,6"/>
</svg>"""

_SVG_INFO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="16" x2="12" y2="12"/>
  <line x1="12" y1="8" x2="12.01" y2="8"/>
</svg>"""

_SVG_CODE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="16 18 22 12 16 6"/>
  <polyline points="8 6 2 12 8 18"/>
</svg>"""

_SVG_HEART = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
</svg>"""


def _card(title: str, icon: str = "") -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setProperty("class", "card")
    card.setObjectName("card")
    lay = QVBoxLayout(card)
    lay.setContentsMargins(20, 16, 20, 20)
    lay.setSpacing(14)
    header = QHBoxLayout()
    if icon:
        icon_lbl = QLabel()
        icon_lbl.setFixedSize(18, 18)
        icon_lbl.setStyleSheet("background: transparent;")
        svg_bytes = icon.encode("utf-8")
        pixmap = QPixmap(18, 18)
        pixmap.fill(Qt.GlobalColor.transparent)
        p = QPainter(pixmap)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        QSvgRenderer(QByteArray(svg_bytes)).render(p)
        p.end()
        icon_lbl.setPixmap(pixmap)
        header.addWidget(icon_lbl)
    ttl = QLabel(title)
    ttl.setStyleSheet("font-size: 15px; font-weight: 600; color: #1a1a1a; background: transparent;")
    header.addWidget(ttl)
    header.addStretch()
    lay.addLayout(header)
    return card, lay


def _link_button(text: str, url: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(
        "QPushButton { font-size: 13px; color: #d6608a; background: rgba(214, 96, 138, 0.08);"
        "border: 1px solid rgba(214, 96, 138, 0.2); border-radius: 6px;"
        "padding: 6px 14px; text-align: left; }"
        "QPushButton:hover { background: rgba(214, 96, 138, 0.15); }"
    )
    btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
    return btn


def _info_row(parent_lay: QVBoxLayout, label: str, value: str, is_link: bool = False, url: str = ""):
    row = QHBoxLayout()
    row.setSpacing(16)
    lbl = QLabel(label)
    lbl.setFixedWidth(64)
    lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #9b9a98;")
    row.addWidget(lbl)
    if is_link and url:
        val = QLabel(f'<a href="{url}" style="color: #d6608a; text-decoration: none;">{value}</a>')
        val.setOpenExternalLinks(True)
        val.setStyleSheet("font-size: 14px; color: #1a1a1a;")
    else:
        val = QLabel(value)
        val.setStyleSheet("font-size: 14px; color: #1a1a1a;")
    row.addWidget(val)
    parent_lay.addLayout(row)


def _section_label(parent_lay: QVBoxLayout, text: str):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        "font-size: 12px; font-weight: 600; color: #9b9a98;"
        "text-transform: uppercase; letter-spacing: 0.05em;"
        "margin-top: 8px; background: transparent;"
    )
    parent_lay.addWidget(lbl)


def _dep_row(parent_lay: QVBoxLayout, name: str, license_: str, url: str):
    row = QHBoxLayout()
    row.setSpacing(12)
    name_lbl = QLabel(f'<a href="{url}" style="color: #d6608a; text-decoration: none;">{name}</a>')
    name_lbl.setOpenExternalLinks(True)
    name_lbl.setFixedWidth(140)
    name_lbl.setStyleSheet("font-size: 13px; font-weight: 500;")
    row.addWidget(name_lbl)
    lic_lbl = QLabel(license_)
    lic_lbl.setStyleSheet("font-size: 12px; color: #9b9a98;")
    row.addWidget(lic_lbl)
    row.addStretch()
    parent_lay.addLayout(row)


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        root = QVBoxLayout(container)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("关于")
        title.setObjectName("page_title")
        root.addWidget(title)

        hero = QFrame()
        hero.setStyleSheet("QFrame { background: #ffffff;border: 1px solid rgba(0,0,0,0.04); border-radius: 20px; }")
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
        icon_lbl.setStyleSheet("background: #d6608a;border-radius: 16px;")
        hero_layout.addWidget(icon_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        name_lbl = QLabel("nieTTS 2.0")
        name_lbl.setStyleSheet("font-size: 24px; font-weight: 700; color: #1a1a1a; letter-spacing: -0.02em;")
        hero_layout.addWidget(name_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        ver_lbl = QLabel(VERSION)
        ver_lbl.setStyleSheet("font-family: 'Consolas', monospace; font-size: 13px; color: #d6608a; font-weight: 500;")
        hero_layout.addWidget(ver_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        desc_lbl = QLabel("一体化 TTS + STT + 翻译工具")
        desc_lbl.setStyleSheet("font-size: 14px; color: #6b6a68;")
        hero_layout.addWidget(desc_lbl, 0, Qt.AlignmentFlag.AlignCenter)

        root.addWidget(hero)

        intro_card, intro_l = _card("软件简介", _SVG_INFO)
        intro_text = QLabel(
            "nieTTS 2.0 是一款专为 VR 社交平台（如 VRChat）设计的桌面应用，"
            "集成了语音合成（TTS）、语音识别（STT）和翻译功能。"
            "支持多种在线和离线引擎，提供 PySide6 桌面 GUI 和 Vue 3 Web 界面，"
            "可通过 OSC 协议与 VRChat 无缝集成。"
        )
        intro_text.setWordWrap(True)
        intro_text.setStyleSheet("font-size: 14px; color: #1a1a1a; line-height: 1.6;")
        intro_l.addWidget(intro_text)
        root.addWidget(intro_card)

        author_card, author_l = _card("作者信息", _SVG_GITHUB)
        _info_row(author_l, "作者", "machina")
        _info_row(author_l, "GitHub", "@machinad", True, "https://github.com/machinad")
        _info_row(author_l, "邮箱", "l1531829828@163.com", True, "mailto:l1531829828@163.com")
        root.addWidget(author_card)

        links_card, links_l = _card("项目链接", _SVG_LINK)
        links_btn_row = QHBoxLayout()
        links_btn_row.setSpacing(12)
        links_btn_row.addWidget(_link_button("GitHub 仓库", "https://github.com/machinad/nieTTS2.0"))
        links_btn_row.addWidget(_link_button("问题反馈", "https://github.com/machinad/nieTTS2.0/issues"))
        links_btn_row.addStretch()
        links_l.addLayout(links_btn_row)
        root.addWidget(links_card)

        license_card, license_l = _card("许可证", _SVG_INFO)
        lic_text = QLabel(
            '本项目基于 <a href="http://www.apache.org/licenses/LICENSE-2.0" '
            'style="color: #d6608a; text-decoration: none;">Apache License 2.0</a> 开源。'
        )
        lic_text.setOpenExternalLinks(True)
        lic_text.setStyleSheet("font-size: 14px; color: #1a1a1a;")
        license_l.addWidget(lic_text)
        root.addWidget(license_card)

        stack_card, stack_l = _card("技术栈", _SVG_CODE)
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
            lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #9b9a98;")
            row.addWidget(lbl)
            val = QLabel(value)
            val.setStyleSheet("font-size: 14px; color: #1a1a1a;")
            row.addWidget(val)
            stack_l.addLayout(row)
        root.addWidget(stack_card)

        deps_card, deps_l = _card("开源致谢", _SVG_HEART)

        _section_label(deps_l, "核心运行时")
        for name, lic, url in [
            ("sherpa-onnx", "Apache-2.0", "https://github.com/k2-fsa/sherpa-onnx"),
            ("edge-tts", "MIT", "https://github.com/rany2/edge-tts"),
            ("dashscope", "Apache-2.0", "https://github.com/dashscope/dashscope-sdk-python"),
            ("openai", "Apache-2.0", "https://github.com/openai/openai-python"),
            ("numpy", "BSD-3-Clause", "https://github.com/numpy/numpy"),
            ("miniaudio", "Unlicense", "https://github.com/mackron/miniaudio"),
            ("python-osc", "MIT", "https://github.com/attwad/python-osc"),
            ("httpx", "BSD-3-Clause", "https://github.com/encode/httpx"),
        ]:
            _dep_row(deps_l, name, lic, url)

        _section_label(deps_l, "Web 服务")
        for name, lic, url in [
            ("quart", "MIT", "https://github.com/pallets/quart"),
            ("quart-cors", "MIT", "https://github.com/pallets/quart-cors"),
            ("cryptography", "Apache-2.0/BSD-3-Clause", "https://github.com/pyca/cryptography"),
        ]:
            _dep_row(deps_l, name, lic, url)

        _section_label(deps_l, "GUI")
        for name, lic, url in [
            ("PySide6", "LGPL-3.0", "https://wiki.qt.io/Qt_for_Python"),
            ("qasync", "BSD-2-Clause", "https://github.com/gmarull/qasync"),
        ]:
            _dep_row(deps_l, name, lic, url)

        _section_label(deps_l, "前端")
        for name, lic, url in [
            ("Vue 3", "MIT", "https://github.com/vuejs/core"),
            ("Vue Router 4", "MIT", "https://github.com/vuejs/router"),
            ("Element Plus", "MIT", "https://github.com/element-plus/element-plus"),
            ("Vite", "MIT", "https://github.com/vitejs/vite"),
        ]:
            _dep_row(deps_l, name, lic, url)

        _section_label(deps_l, "模型下载")
        for name, lic, url in [
            ("huggingface-hub", "Apache-2.0", "https://github.com/huggingface/huggingface_hub"),
            ("modelscope", "Apache-2.0", "https://github.com/modelscope/modelscope"),
        ]:
            _dep_row(deps_l, name, lic, url)

        root.addWidget(deps_card)

        root.addStretch()

        scroll.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
