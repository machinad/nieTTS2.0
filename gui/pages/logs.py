import html
import logging
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)

COLOR_MAP = {"debug": "#8080ff", "info": "#6b6a68", "warn": "#c48520", "error": "#d04840"}
ICON_MAP = {"debug": "\u2699", "info": "\u25cf", "warn": "\u26a0", "error": "\u2715"}


class LogsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._filter = "all"
        self._counts = {"all": 0, "debug": 0, "info": 0, "warn": 0, "error": 0}
        self._entries: list[tuple[str, str]] = []
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("日志")
        title.setObjectName("page_title")
        root.addWidget(title)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self._filter_buttons = {}
        for level in ("all", "debug", "info", "warn", "error"):
            btn = QPushButton()
            btn.setObjectName("filter_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self._update_filter_btn_text(btn, level)
            btn.clicked.connect(lambda checked, lv=level: self._set_filter(lv))
            toolbar.addWidget(btn)
            self._filter_buttons[level] = btn

        toolbar.addStretch()

        clear_btn = QPushButton("  清空")
        clear_btn.setObjectName("secondary_btn")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setFixedHeight(40)
        clear_btn.setMinimumWidth(80)
        clear_btn.clicked.connect(self._clear_logs)
        toolbar.addWidget(clear_btn)

        root.addLayout(toolbar)

        self._terminal = QTextBrowser()
        self._terminal.setObjectName("log_terminal")
        self._terminal.setOpenExternalLinks(False)
        root.addWidget(self._terminal)

        self._update_active_filter()

    def append_log(self, level: str, message: str):
        self._entries.append((level, message))
        if len(self._entries) > 500:
            self._entries = self._entries[-500:]

        self._counts["all"] += 1
        if level in self._counts:
            self._counts[level] += 1

        for btn_level, btn in self._filter_buttons.items():
            self._update_filter_btn_text(btn, btn_level)

        if self._filter != "all" and self._filter != level:
            return

        self._append_html(level, message)

    def _append_html(self, level: str, message: str):
        color = COLOR_MAP.get(level, "#6b6a68")
        icon = ICON_MAP.get(level, "\u25cf")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._terminal.append(
            f'<div style="color:{color};font-family:JetBrains Mono,Consolas,monospace;'
            f'font-size:13px;line-height:1.6;">'
            f'<span style="color:#9b9a98;">{timestamp}</span> '
            f'<span style="font-size:10px;">{icon}</span> {html.escape(message)}</div>'
        )
        sb = self._terminal.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _set_filter(self, level: str):
        self._filter = level
        self._update_active_filter()
        self._rebuild_terminal()

    def _update_active_filter(self):
        for level, btn in self._filter_buttons.items():
            btn.setProperty("active", str(level == self._filter).lower())
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _update_filter_btn_text(self, btn: QPushButton, level: str):
        label_map = {"all": "全部", "debug": "debug", "info": "info", "warn": "warn", "error": "error"}
        count = self._counts.get(level, 0)
        btn.setText(f"  {label_map[level]}  {count}")

    def _clear_logs(self):
        self._counts = {"all": 0, "debug": 0, "info": 0, "warn": 0, "error": 0}
        self._entries.clear()
        self._terminal.clear()
        for btn_level, btn in self._filter_buttons.items():
            self._update_filter_btn_text(btn, btn_level)

    def _rebuild_terminal(self):
        self._terminal.clear()
        for level, message in self._entries:
            if self._filter == "all" or self._filter == level:
                self._append_html(level, message)
