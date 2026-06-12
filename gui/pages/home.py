import html
import logging
from PySide6.QtCore import Qt, Signal, QSize, QByteArray, QEvent
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit,
    QComboBox, QPushButton, QFrame,
)
from gui.widgets.waveform import WaveformWidget

logger = logging.getLogger(__name__)

LANGUAGES = [
    "中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语", "俄语",
    "葡萄牙语", "意大利语", "阿拉伯语", "印尼语", "泰语", "越南语", "粤语",
]

_SVG_PENCIL = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6b6a68" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M17 3a2.85 2.85 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
  <path d="m15 5 4 4"/>
</svg>'''

_SVG_SEND = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m22 2-7 20-4-9-9-4Z"/>
  <path d="M22 2 11 13"/>
</svg>'''

_SVG_MIC = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
  <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
  <line x1="12" x2="12" y1="19" y2="22"/>
</svg>'''

_SVG_STOP = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="14" height="14" x="5" y="5" rx="2"/>
</svg>'''

_SVG_ARROW_RIGHT = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9b9a98" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M5 12h14"/>
  <path d="m12 5 7 7-7 7"/>
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


def _make_icon(svg_data: bytes, size: int = 16) -> QIcon:
    renderer = QSvgRenderer(QByteArray(svg_data))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


class HomePage(QWidget):
    request_send = Signal(str, dict)
    log_message = Signal(str, str)
    recording_started = Signal()
    recording_stopped = Signal()

    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self._recording = False
        self._setup_ui()
        self._load_config()
        self.bridge.config_changed.connect(self._refresh_from_config)

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        scroll = QWidget()
        scroll_layout = QVBoxLayout(scroll)
        scroll_layout.setContentsMargins(24, 24, 24, 24)
        scroll_layout.setSpacing(16)

        title_row = QHBoxLayout()
        title = QLabel("主页")
        title.setObjectName("page_title")
        title_row.addWidget(title)
        title_row.addStretch()
        scroll_layout.addLayout(title_row)

        # ---- Editor card ----
        editor_card = QFrame()
        editor_card.setObjectName("card")
        editor_card.setProperty("class", "card")
        editor_layout = QVBoxLayout(editor_card)
        editor_layout.setContentsMargins(20, 16, 20, 20)
        editor_layout.setSpacing(8)

        editor_header = QHBoxLayout()
        editor_label = QLabel("文本输入")
        editor_label.setStyleSheet("font-size: 13px; color: #6b6a68; font-weight: 500; background: transparent;")
        editor_header.addWidget(editor_label)
        editor_header.addStretch()
        self._char_count = QLabel("0 / 5000")
        self._char_count.setStyleSheet(
            "font-family: 'JetBrains Mono', 'Consolas', monospace; font-size: 12px; color: #9b9a98; background: transparent;"
        )
        editor_header.addWidget(self._char_count)
        editor_layout.addLayout(editor_header)

        self._text_edit = QPlainTextEdit()
        self._text_edit.setPlaceholderText("输入要合成的文本...\n\nEnter 发送 · shift+Enter 换行")
        self._text_edit.setMaximumHeight(200)
        self._text_edit.textChanged.connect(self._on_text_changed)
        self._text_edit.installEventFilter(self)
        editor_layout.addWidget(self._text_edit)

        scroll_layout.addWidget(editor_card)

        # ---- Language card ----
        lang_card = QFrame()
        lang_card.setProperty("class", "card")
        lang_card.setObjectName("card")
        lang_layout = QHBoxLayout(lang_card)
        lang_layout.setContentsMargins(20, 16, 20, 16)
        lang_layout.setSpacing(16)

        src_col = QVBoxLayout()
        src_col.setSpacing(6)
        src_label = QLabel("源语言")
        src_label.setProperty("class", "field_label")
        src_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #9b9a98; background: transparent;")
        src_col.addWidget(src_label)
        self._src_combo = QComboBox()
        self._src_combo.addItems(LANGUAGES)
        src_col.addWidget(self._src_combo)
        lang_layout.addLayout(src_col, stretch=1)

        arrow = QLabel()
        arrow_pixmap = QPixmap(24, 24)
        arrow_pixmap.fill(Qt.GlobalColor.transparent)
        p = QPainter(arrow_pixmap)
        QSvgRenderer(QByteArray(_SVG_ARROW_RIGHT)).render(p)
        p.end()
        arrow.setPixmap(arrow_pixmap)
        arrow.setFixedSize(24, 24)
        arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow.setStyleSheet("background: transparent;")
        lang_layout.addWidget(arrow, alignment=Qt.AlignmentFlag.AlignVCenter)

        tgt_col = QVBoxLayout()
        tgt_col.setSpacing(6)
        tgt_label = QLabel("目标语言")
        tgt_label.setProperty("class", "field_label")
        tgt_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #9b9a98; background: transparent;")
        tgt_col.addWidget(tgt_label)
        self._tgt_combo = QComboBox()
        self._tgt_combo.addItems(LANGUAGES)
        tgt_col.addWidget(self._tgt_combo)
        lang_layout.addLayout(tgt_col, stretch=1)

        scroll_layout.addWidget(lang_card)

        # ---- Engine badge ----
        engine_btn = QPushButton()
        engine_btn.setObjectName("secondary_btn")
        engine_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        engine_btn.setFixedHeight(42)
        engine_btn.setIconSize(QSize(16, 16))
        self._engine_label = engine_btn
        self._update_engine_badge()
        scroll_layout.addWidget(engine_btn)

        # ---- Action buttons ----
        actions_row = QHBoxLayout()
        actions_row.setSpacing(12)

        send_btn = QPushButton("发送合成")
        send_btn.setObjectName("primary_btn")
        send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        send_btn.setFixedHeight(48)
        send_btn.setIconSize(QSize(18, 18))
        send_btn.setIcon(_make_icon(_SVG_SEND, 18))
        send_btn.clicked.connect(self._on_send)
        actions_row.addWidget(send_btn)

        self._mic_btn = QPushButton("语音输入")
        self._mic_btn.setObjectName("secondary_btn")
        self._mic_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._mic_btn.setFixedHeight(48)
        self._mic_btn.setIconSize(QSize(18, 18))
        self._mic_btn.setIcon(_make_icon(_SVG_MIC, 18))
        self._mic_btn.clicked.connect(self._toggle_recording)
        actions_row.addWidget(self._mic_btn)

        scroll_layout.addWidget(QWidget())
        scroll_layout.addLayout(actions_row)

        self._waveform = WaveformWidget()
        self._waveform.hide()
        scroll_layout.addWidget(self._waveform)

        self._log_box = QPlainTextEdit()
        self._log_box.setObjectName("log_terminal")
        self._log_box.setReadOnly(True)
        self._log_box.setMaximumHeight(120)
        self._log_box.setPlaceholderText("日志输出...")
        scroll_layout.addWidget(self._log_box)

        scroll_layout.addStretch()
        root.addWidget(scroll)

    def _load_config(self):
        self._refresh_from_config()
        self._src_combo.currentTextChanged.connect(
            lambda v: self.bridge.update_config({"source_lang": v})
        )
        self._tgt_combo.currentTextChanged.connect(
            lambda v: self.bridge.update_config({"target_lang": v})
        )

    def _refresh_from_config(self):
        cfg = self.bridge.get_config()
        src = cfg.get("source_lang")
        tgt = cfg.get("target_lang")
        self._src_combo.blockSignals(True)
        idx_src = self._src_combo.findText(src)
        if idx_src >= 0:
            self._src_combo.setCurrentIndex(idx_src)
        self._src_combo.blockSignals(False)
        self._tgt_combo.blockSignals(True)
        idx_tgt = self._tgt_combo.findText(tgt)
        if idx_tgt >= 0:
            self._tgt_combo.setCurrentIndex(idx_tgt)
        self._tgt_combo.blockSignals(False)
        self._update_engine_badge()

    def _update_engine_badge(self):
        cfg = self.bridge.get_config()
        engine = cfg.get("tts_provider", {}).get("provider", "edge_tts")
        providers = cfg.get("tts_provider", {}).get("providers", [])
        voice = ""
        for p in providers:
            if p.get("name") == engine:
                voice = p.get("voice", "")
                break
        text = f"引擎: {engine}"
        if voice:
            text += f"  /  {voice}"
        self._engine_label.setText(text)
        self._engine_label.setIcon(_make_icon(_SVG_GEAR, 16))

    def eventFilter(self, obj, event):
        if obj is self._text_edit and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier) and \
                   not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                    self._on_send()
                    return True
        return super().eventFilter(obj, event)

    def _on_text_changed(self):
        text = self._text_edit.toPlainText()
        if len(text) > 5000:
            self._text_edit.setPlainText(text[:5000])
            text = text[:5000]
        self._char_count.setText(f"{len(text)} / 5000")

    def _on_send(self):
        text = self._text_edit.toPlainText().strip()
        if not text:
            return
        cfg = self.bridge.get_config()
        providers = cfg.get("tts_provider", {}).get("providers", [])
        engine = cfg.get("tts_provider", {}).get("provider", "edge_tts")
        voice = ""
        for p in providers:
            if p.get("name") == engine:
                voice = p.get("voice", "")
                break
        opts = {
            "tts_provider": engine,
            "voice": voice,
            "translate": cfg.get("isTranslate"),
            "play_audio": cfg.get("isPlayAudio"),
            "play_translation": cfg.get("isPlayTranslation"),
            "osc_enabled": cfg.get("osc_enabled"),
            "source_lang": self._src_combo.currentText(),
            "target_lang": self._tgt_combo.currentText(),
        }
        self._text_edit.clear()
        self.request_send.emit(text, opts)

    def _toggle_recording(self):
        if self._recording:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self):
        self._recording = True
        self._mic_btn.setText("停止录音")
        self._mic_btn.setObjectName("danger_btn")
        self._mic_btn.setIcon(_make_icon(_SVG_STOP, 18))
        self._mic_btn.style().unpolish(self._mic_btn)
        self._mic_btn.style().polish(self._mic_btn)
        self._waveform.show()
        self._waveform.set_recording(True)
        self.recording_started.emit()

    def _stop_recording(self):
        self._recording = False
        self._mic_btn.setText("语音输入")
        self._mic_btn.setObjectName("secondary_btn")
        self._mic_btn.setIcon(_make_icon(_SVG_MIC, 18))
        self._mic_btn.style().unpolish(self._mic_btn)
        self._mic_btn.style().polish(self._mic_btn)
        self._waveform.set_recording(False)
        self._waveform.hide()
        self.recording_stopped.emit()

    def update_waveform(self, level: float, freq_levels: list = None):
        if self._recording:
            self._waveform.update_level(level, freq_levels)

    def append_log(self, level: str, message: str):
        color_map = {"info": "#6b6a68", "warn": "#c48520", "error": "#d04840"}
        color = color_map.get(level, "#6b6a68")
        self._log_box.appendHtml(
            f'<span style="color:{color};font-family:JetBrains Mono,Consolas,monospace;font-size:12px;">{html.escape(message)}</span>'
        )
        sb = self._log_box.verticalScrollBar()
        sb.setValue(sb.maximum())

