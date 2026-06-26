import logging
from PySide6.QtCore import Qt, Signal, QSize, QByteArray, QTimer
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QSizePolicy,
)

logger = logging.getLogger(__name__)


_CN_PUNCT = {",": "，", ".": "。", "?": "？", "!": "！", ";": "；", ":": "："}

# 长按上滑输入映射
_SWIPE_MAP = {
    "q": "1", "w": "2", "e": "3", "r": "4", "t": "5",
    "y": "6", "u": "7", "i": "8", "o": "9", "p": "0",
    "a": "~", "s": "!", "d": "@", "f": "#", "g": "%",
    "h": "“", "j": "”", "k": "*", "l": "?",
    "z": "(", "x": ")", "c": "-", "v": "_", "b": ":",
    "n": ";", "m": "/",
}

# 键盘基准尺寸（scale=1.0 时的像素值，实际由 resizeEvent 等比缩放）
_KEY_W = 48
_KEY_H = 42
_KEY_RATIO = _KEY_W / _KEY_H  # 宽高比 8:7
_FN_RATIO = 1.38    # Shift/⌫/↵ 宽度比
_SPACE_RATIO = 4.2  # 空格宽度比
_BASE_SPACING = 3   # 基准间距

# 基准键盘总宽（qwertyuiop: 10键 + 9间距，间距按 _KEY_W 等比）
_BASE_KB_WIDTH = 10 * _KEY_W + 9 * _BASE_SPACING   # 507
# 基准键盘总高（4行 × 键高 + 3行间距）
_BASE_KB_HEIGHT = 4 * _KEY_H + 3 * _BASE_SPACING   # 177


def _icon(svg: bytes, sz: int = 16) -> QIcon:
    r = QSvgRenderer(QByteArray(svg))
    pm = QPixmap(sz, sz)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    r.render(p)
    p.end()
    return QIcon(pm)


class SwipeKey(QPushButton):
    """支持上滑输入的按键：短按触发 clicked，上滑触发 swipe_up 信号。"""

    swipe_up = Signal(str)  # 滑动时发出特殊字符

    def __init__(self, text: str, swipe_char: str | None = None, parent=None):
        super().__init__(text, parent)
        self._swipe_char = swipe_char
        self._press_pos = None
        self._swiped = False
        self._swipe_threshold = 20  # 上滑最小像素

        # 在按键上方显示小号特殊字符
        if swipe_char:
            self._tip = QLabel(swipe_char, self)
            self._tip.setStyleSheet(
                "font-size: 13px; color: #9b9a98; background: transparent; border: none;")
            self._tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._tip.setGeometry(0, 2, self.width(), 16)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, '_tip'):
            self._tip.setGeometry(0, 2, self.width(), 16)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._press_pos = event.position().toPoint()
            self._swiped = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._press_pos and not self._swiped:
            dy = self._press_pos.y() - event.position().toPoint().y()
            if dy > self._swipe_threshold and self._swipe_char:
                self._swiped = True
                self.swipe_up.emit(self._swipe_char)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._swiped:
            # 滑动已触发，阻止 clicked 信号
            self._press_pos = None
            self._swiped = False
            return
        self._press_pos = None
        super().mouseReleaseEvent(event)

    def touchEvent(self, event):
        points = event.points()
        if not points:
            return False
        pt = points[0]
        pos = pt.position().toPoint()
        if pt.state() == Qt.TouchPointState.TouchPointPressed:
            self._press_pos = pos
            self._swiped = False
        elif pt.state() == Qt.TouchPointState.TouchPointMoved:
            if self._press_pos and not self._swiped:
                dy = self._press_pos.y() - pos.y()
                if dy > self._swipe_threshold and self._swipe_char:
                    self._swiped = True
                    self.swipe_up.emit(self._swipe_char)
        elif pt.state() == Qt.TouchPointState.TouchPointReleased:
            if self._swiped:
                self._press_pos = None
                self._swiped = False
                return True
            self._press_pos = None
        return False


_QSS = """
/* ── 预览行 ── */
QLineEdit#preview {{
    background: #fafaf8; border: 1px solid #d8d7d4;
    border-radius: 5px; padding: 4px 8px;
    font-size: 20px; color: #1a1a1a;
    min-height: 28px; max-height: 28px;
}}
QLineEdit#preview:focus {{ border-color: #9a6ad6; }}
QLabel#count {{ font-family: 'Consolas', monospace; font-size: 22px; color: #9b9a98; }}
/* ── 候选栏 ── */
QFrame#candbar {{
    background: #ffffff; border: 1px solid #e0dfdc;
    border-radius: 5px;
}}
QLabel#preedit {{ color: #d6608a; font-size: 26px; font-weight: 600; padding-left: 4px; }}
QPushButton#pg {{
    background: transparent; border: none; color: #9b9a98; font-size: 26px;
    min-width: 24px; max-width: 24px; min-height: 44px; max-height: 44px;
}}
QPushButton#pg:hover {{ color: #d6608a; }}
QPushButton#pg:disabled {{ color: #d0cfcc; }}
QLabel#pginfo {{ font-size: 22px; color: #9b9a98; min-width: 16px; max-width: 16px; }}
QPushButton#cand {{
    background: #ffffff; border: 1px solid #e8e7e4;
    border-radius: 3px; padding: 0 8px;
    font-size: 20px; color: #1a1a1a;
    min-height: 48px; max-height: 48px;
}}
QPushButton#cand:hover {{ background: #f5f0ff; border-color: #9a6ad6; }}

/* ── 键盘容器 ── */
QFrame#kb_container {{
    background: #f0efec;
    border: 1px solid #e0dfdc;
    border-radius: 10px;
}}

/* ── 字母键 ── */
QPushButton#k {{
    background: #ffffff; border: 1px solid #c8c7c4; border-radius: 5px;
    font-size: {k_fs}px; font-weight: 500; color: #1a1a1a;
}}
QPushButton#k:hover {{ background: #eae9e6; }}
QPushButton#k:pressed {{ background: #d8d7d4; border-color: #b0afac; }}

/* ── 功能键 ⌫ ── */
QPushButton#fn {{
    background: #c8c7c4; border: 1px solid #b8b7b4; border-radius: 5px;
    font-size: {fn_fs}px; font-weight: 600; color: #ffffff;
}}
QPushButton#fn:hover {{ background: #b8b7b4; }}
QPushButton#fn:pressed {{ background: #a8a7a4; }}

/* ── 中英 ── */
QPushButton#mode {{
    background: #d6608a; border: 1px solid #c4507a; border-radius: 5px;
    font-size: {mode_fs}px; font-weight: 700; color: #ffffff;
}}
QPushButton#mode:hover {{ background: #c4507a; }}

/* ── 标点 ── */
QPushButton#p {{
    background: #e8e7e4; border: 1px solid #d0cfcc; border-radius: 5px;
    font-size: {p_fs}px; color: #4a4a48;
}}
QPushButton#p:hover {{ background: #dddcda; }}
QPushButton#p:pressed {{ background: #d0cfcc; }}

/* ── 空格 ── */
QPushButton#sp {{
    background: #ffffff; border: 1px solid #c8c7c4; border-radius: 5px;
    font-size: {sp_fs}px; color: #9b9a98;
}}
QPushButton#sp:hover {{ background: #eae9e6; }}
QPushButton#sp:pressed {{ background: #d8d7d4; }}

/* ── 回车 ── */
QPushButton#ent {{
    background: #9a6ad6; border: 1px solid #8a5ac6; border-radius: 5px;
    font-size: {ent_fs}px; font-weight: 700; color: #ffffff;
}}
QPushButton#ent:hover {{ background: #8a5ac6; }}
QPushButton#ent:pressed {{ background: #7a5ab6; }}

/* ── 方案选择栏 ── */
QFrame#schema_bar {{
    background: #f8f7f5; border: 1px solid #e0dfdc;
    border-radius: 5px;
}}
QPushButton#schema {{
    background: transparent; border: 1px solid transparent;
    border-radius: 3px; padding: 2px 8px;
    font-size: 13px; color: #6a6a68;
}}
QPushButton#schema:hover {{ background: #eae9e6; }}
QPushButton#schema[active="true"] {{
    background: #9a6ad6; color: #ffffff; border-color: #8a5ac6;
}}
"""

# 基准字号（scale=1.0 时）
_FONT_K = 18      # 字母键
_FONT_FN = 16     # 功能键
_FONT_MODE = 16   # 中英
_FONT_P = 18      # 标点
_FONT_SP = 15     # 空格
_FONT_ENT = 18    # 回车
_FONT_TIP = 10    # 滑动提示字符


def _build_qss(scale: float = 1.0) -> str:
    """根据缩放因子生成完整 QSS"""
    s = lambda base: max(10, round(base * scale))
    return _QSS.format(
        k_fs=s(_FONT_K), fn_fs=s(_FONT_FN), mode_fs=s(_FONT_MODE),
        p_fs=s(_FONT_P), sp_fs=s(_FONT_SP), ent_fs=s(_FONT_ENT),
    )


class KeyboardPage(QWidget):
    """虚拟键盘输入页面"""

    request_send = Signal(str, dict)

    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self.setStyleSheet(_build_qss())

        self._committed = ""
        self._preedit = ""
        self._raw_input = ""  # 用户输入的原始拼音（不带 RIME 分段空格）
        self._candidates: list[str] = []
        self._page_no = 0
        self._is_last = False
        self._ascii = False
        self._upper = False
        self._cn_punct = True
        self._letter_btns: dict[str, QPushButton] = {}
        self._all_key_btns: list[tuple[QPushButton, float]] = []  # (btn, width_ratio)
        self._kb_frame: QFrame | None = None
        self._kb_outer_layout: QVBoxLayout | None = None
        self._bs_held = False
        self._bs_timer = QTimer(self)
        self._bs_timer.setInterval(100)
        self._bs_timer.timeout.connect(self._backspace)

        self._build_ui()

    # ── 构建 ────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 8, 16, 8)
        root.setSpacing(6)

        # 预览行
        root.addWidget(self._mk_preview())
        # 候选栏
        root.addWidget(self._mk_candbar())
        # 方案选择栏
        root.addWidget(self._mk_schema_bar())
        # 键盘（占满剩余空间）
        kb = self._mk_keyboard()
        kb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        root.addWidget(kb, stretch=1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._recalc_key_sizes()

    def showEvent(self, event):
        super().showEvent(event)
        # 首次显示时延迟一帧再算，确保布局已完成
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._recalc_key_sizes)

    def _recalc_key_sizes(self):
        """根据页面可用空间等比缩放键盘（宽高和字体都等比）"""
        if not self._kb_frame or not self._kb_outer_layout:
            return

        geo = self._kb_frame.geometry()
        pad = self._kb_outer_layout.contentsMargins()
        avail_w = geo.width() - pad.left() - pad.right()
        avail_h = geo.height() - pad.top() - pad.bottom()
        if avail_w <= 0 or avail_h <= 0:
            return

        scale_w = avail_w / _BASE_KB_WIDTH
        scale_h = avail_h / _BASE_KB_HEIGHT
        scale = min(scale_w, scale_h)
        scale = max(0.5, scale)

        key_w = max(32, round(_KEY_W * scale))
        key_h = max(28, round(_KEY_H * scale))
        sp = max(2, round(_BASE_SPACING * scale))

        for btn, ratio in self._all_key_btns:
            btn.setFixedSize(max(32, round(key_w * ratio)), key_h)

        # 动态重建 QSS（含缩放后的字号）
        self.setStyleSheet(_build_qss(scale))

        # 等比缩放 SwipeKey 的提示标签
        tip_fs = max(8, round(_FONT_TIP * scale))
        tip_h = max(10, round(16 * scale))
        for btn, _ in self._all_key_btns:
            if isinstance(btn, SwipeKey) and hasattr(btn, '_tip'):
                btn._tip.setStyleSheet(
                    f"font-size: {tip_fs}px; color: #9b9a98; background: transparent; border: none;")
                btn._tip.setGeometry(0, round(2 * scale), btn.width(), tip_h)

        for row in self._kb_frame.findChildren(QWidget):
            lay = row.layout()
            if lay and isinstance(lay, (QHBoxLayout, QVBoxLayout)):
                lay.setSpacing(sp)

        self._kb_outer_layout.setSpacing(sp)

    # ── 预览行 ──

    def _mk_preview(self) -> QWidget:
        w = QWidget()
        w.setMaximumHeight(42)
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(6)

        self._preview = QLineEdit()
        self._preview.setObjectName("preview")
        self._preview.setPlaceholderText("点击键盘输入文字...")
        self._preview.setReadOnly(True)
        h.addWidget(self._preview, 1)

        self._count = QLabel("0")
        self._count.setObjectName("count")
        h.addWidget(self._count)
        return w

    # ── 候选栏 ──

    def _mk_candbar(self) -> QFrame:
        f = QFrame()
        f.setObjectName("candbar")
        v = QVBoxLayout(f)
        v.setContentsMargins(6, 4, 16, 4)
        v.setSpacing(3)

        # 第一行：候选词 + 翻页（翻页在右侧）
        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(4)

        self._cand_box = QHBoxLayout()
        self._cand_box.setContentsMargins(0, 0, 0, 0)
        self._cand_box.setSpacing(3)
        self._cand_btns: list[QPushButton] = []
        row1.addLayout(self._cand_box, 1)

        self._prev_btn = QPushButton("◀")
        self._prev_btn.setObjectName("pg")
        self._prev_btn.clicked.connect(lambda: self._page(True))
        row1.addWidget(self._prev_btn)

        self._pg_info = QLabel("")
        self._pg_info.setObjectName("pginfo")
        row1.addWidget(self._pg_info)

        self._next_btn = QPushButton("▶")
        self._next_btn.setObjectName("pg")
        self._next_btn.clicked.connect(lambda: self._page(False))
        row1.addWidget(self._next_btn)
        v.addLayout(row1)

        # 第二行：拼音
        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(0)
        self._preedit_lbl = QLabel("")
        self._preedit_lbl.setObjectName("preedit")
        self._preedit_lbl.hide()
        row2.addWidget(self._preedit_lbl)
        row2.addStretch(1)
        v.addLayout(row2)

        return f

    # ── 方案选择栏 ──

    def _mk_schema_bar(self) -> QFrame:
        f = QFrame()
        f.setObjectName("schema_bar")
        h = QHBoxLayout(f)
        h.setContentsMargins(4, 2, 4, 2)
        h.setSpacing(4)

        self._schema_btns: dict[str, QPushButton] = {}
        try:
            schemas = self.bridge.rime_schema_list()
            current = self.bridge.rime_current_schema()
        except Exception:
            schemas, current = [], None

        for s in schemas:
            sid = s.get("schema_id", "")
            name = s.get("name", sid)
            b = QPushButton(name)
            b.setObjectName("schema")
            b.setProperty("schema_id", sid)
            if sid == current:
                b.setProperty("active", True)
                b.style().unpolish(b)
                b.style().polish(b)
            b.clicked.connect(lambda _, s=sid: self._switch_schema(s))
            h.addWidget(b)
            self._schema_btns[sid] = b

        h.addStretch(1)
        return f

    def _switch_schema(self, schema_id: str):
        try:
            ok = self.bridge.rime_switch_schema(schema_id)
            if ok:
                # 更新按钮高亮状态
                for sid, b in self._schema_btns.items():
                    active = sid == schema_id
                    b.setProperty("active", active)
                    b.style().unpolish(b)
                    b.style().polish(b)
                # 清空当前输入状态
                self._preedit = ""
                self._raw_input = ""
                self._candidates = []
                self._refresh_preview()
                self._refresh_cands()
        except Exception as e:
            logger.error("切换方案失败: %s", e)

    # ── 键盘 ──

    def _mk_keyboard(self) -> QFrame:
        """整个键盘：4 行各自居中，外包一个固定宽度容器"""
        frame = QFrame()
        frame.setObjectName("kb_container")
        self._kb_frame = frame

        outer = QVBoxLayout(frame)
        outer.setContentsMargins(10, 6, 10, 6)
        outer.setSpacing(_BASE_SPACING)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._kb_outer_layout = outer

        # Row 0: QWERTYUIOP
        outer.addWidget(self._mk_row("qwertyuiop"), alignment=Qt.AlignmentFlag.AlignHCenter)
        # Row 1: ASDFGHJKL
        outer.addWidget(self._mk_row("asdfghjkl"), alignment=Qt.AlignmentFlag.AlignHCenter)
        # Row 2: ⇧ ZXCVBNM ⌫
        outer.addWidget(self._mk_row_zxcv(), alignment=Qt.AlignmentFlag.AlignHCenter)
        # Row 3: 中/英 ， 空格 。 ↵
        outer.addWidget(self._mk_row_bottom(), alignment=Qt.AlignmentFlag.AlignHCenter)

        return frame

    def _mk_row(self, keys: str) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(_BASE_SPACING)
        for ch in keys:
            h.addWidget(self._mk_key(ch))
        return w

    def _mk_row_zxcv(self) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(_BASE_SPACING)

        self._shift_btn = self._mk_fn("分词")
        self._shift_btn.clicked.connect(self._shift_action)
        h.addWidget(self._shift_btn)

        for ch in "zxcvbnm":
            h.addWidget(self._mk_key(ch))

        self._bs_btn = self._mk_fn("⌫")
        self._bs_btn.pressed.connect(self._bs_start)
        self._bs_btn.released.connect(self._bs_stop)
        h.addWidget(self._bs_btn)
        return w

    def _mk_row_bottom(self) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(_BASE_SPACING)

        # 符号
        sym = QPushButton("符号")
        sym.setObjectName("fn")
        sym.setFixedSize(_KEY_W, _KEY_H)
        sym.setCursor(Qt.CursorShape.PointingHandCursor)
        sym.setProperty("base_font_size", 28)
        self._all_key_btns.append((sym, 1.0))
        h.addWidget(sym)

        # 123
        num = QPushButton("123")
        num.setObjectName("fn")
        num.setFixedSize(_KEY_W, _KEY_H)
        num.setCursor(Qt.CursorShape.PointingHandCursor)
        num.setProperty("base_font_size", 28)
        self._all_key_btns.append((num, 1.0))
        h.addWidget(num)

        # 逗号
        comma = QPushButton(",")
        comma.setObjectName("p")
        comma.setFixedSize(int(_KEY_W * 0.5), _KEY_H)
        comma.setCursor(Qt.CursorShape.PointingHandCursor)
        comma.setProperty("base_font_size", 30)
        comma.clicked.connect(lambda: self._punct(","))
        self._all_key_btns.append((comma, 0.5))
        h.addWidget(comma)

        # 空格
        sp = QPushButton("空格")
        sp.setObjectName("sp")
        sp.setFixedSize(int(_KEY_W * _SPACE_RATIO), _KEY_H)
        sp.setCursor(Qt.CursorShape.PointingHandCursor)
        sp.setProperty("base_font_size", 26)
        sp.clicked.connect(self._space)
        self._all_key_btns.append((sp, _SPACE_RATIO))
        h.addWidget(sp)

        # 句号
        period = QPushButton(".")
        period.setObjectName("p")
        period.setFixedSize(int(_KEY_W * 0.5), _KEY_H)
        period.setCursor(Qt.CursorShape.PointingHandCursor)
        period.setProperty("base_font_size", 30)
        period.clicked.connect(lambda: self._punct("."))
        self._all_key_btns.append((period, 0.5))
        h.addWidget(period)

        # 中英切换
        self._mode_btn = QPushButton("中英")
        self._mode_btn.setObjectName("mode")
        self._mode_btn.setFixedSize(_KEY_W, _KEY_H)
        self._mode_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._mode_btn.setProperty("base_font_size", 28)
        self._mode_btn.clicked.connect(self._toggle_mode)
        self._all_key_btns.append((self._mode_btn, 1.0))
        h.addWidget(self._mode_btn)

        # 回车
        ent = QPushButton("↵")
        ent.setObjectName("ent")
        ent.setFixedSize(int(_KEY_W * _FN_RATIO), _KEY_H)
        ent.setCursor(Qt.CursorShape.PointingHandCursor)
        ent.setProperty("base_font_size", 30)
        ent.clicked.connect(self._enter)
        self._all_key_btns.append((ent, _FN_RATIO))
        h.addWidget(ent)
        return w

    def _mk_key(self, ch: str) -> QPushButton:
        swipe_ch = _SWIPE_MAP.get(ch)
        b = SwipeKey(ch, swipe_ch)
        b.setObjectName("k")
        b.setFixedSize(_KEY_W, _KEY_H)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setProperty("base_font_size", 30)
        b.clicked.connect(lambda _, c=ch: self._key(c))
        if swipe_ch:
            b.swipe_up.connect(self._on_swipe)
            b._tip.setProperty("base_font_size", 13)
        if ch.isalpha():
            self._letter_btns[ch] = b
        self._all_key_btns.append((b, 1.0))
        return b

    def _mk_fn(self, text: str) -> QPushButton:
        b = QPushButton(text)
        b.setObjectName("fn")
        b.setFixedSize(int(_KEY_W * _FN_RATIO), _KEY_H)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setProperty("base_font_size", 28)
        self._all_key_btns.append((b, _FN_RATIO))
        return b

    # ── UI 刷新 ────────────────────────────────────────────────

    def _refresh_preview(self):
        t = self._committed[:5000]
        self._committed = t
        self._preview.setText(t)
        self._count.setText(str(len(t)))
        if self._preedit:
            self._preedit_lbl.setText(self._preedit)
            self._preedit_lbl.show()
        else:
            self._preedit_lbl.hide()

    def _refresh_cands(self):
        for b in self._cand_btns:
            b.deleteLater()
        self._cand_btns.clear()
        for i, c in enumerate(self._candidates):
            b = QPushButton(f"{i+1}.{c}")
            b.setObjectName("cand")
            b.clicked.connect(lambda _, idx=i: self._pick(idx))
            self._cand_box.addWidget(b)
            self._cand_btns.append(b)
        self._prev_btn.setEnabled(self._page_no > 0)
        self._next_btn.setEnabled(not self._is_last)
        self._pg_info.setText(str(self._page_no + 1) if self._candidates else "")

    def _refresh_labels(self):
        for ch, b in self._letter_btns.items():
            b.setText(ch.upper() if self._upper else ch)

    # ── 按键逻辑 ────────────────────────────────────────────────

    def _key(self, ch: str):
        if self._ascii:
            self._committed += ch.upper() if self._upper else ch
            self._refresh_preview()
        else:
            self._raw_input += ch
            self._set_input(self._raw_input)

    def _rime_key(self, code: int, mask: int = 0):
        try:
            r = self.bridge.rime_key(code, mask)
            self._preedit = r.get("preedit", "")
            self._candidates = r.get("candidates", [])
            self._page_no = r.get("page_no", 0)
            self._is_last = r.get("is_last_page", False)
            if r.get("committed"):
                self._committed += r["committed"]
            self._refresh_preview()
            self._refresh_cands()
        except Exception as e:
            logger.error("rime_key 失败: %s", e)

    def _set_input(self, text: str):
        try:
            r = self.bridge.rime_set_input(text)
            self._preedit = r.get("preedit", "")
            self._candidates = r.get("candidates", [])
            self._page_no = r.get("page_no", 0)
            self._is_last = r.get("is_last_page", False)
            if r.get("committed"):
                self._committed += r["committed"]
            self._refresh_preview()
            self._refresh_cands()
        except Exception as e:
            logger.error("rime_set_input 失败: %s", e)

    def _on_swipe(self, ch: str):
        if self._raw_input:
            self._raw_input += ch
            self._set_input(self._raw_input)
        else:
            self._committed += ch
            self._refresh_preview()

    def _backspace(self):
        if self._raw_input:
            self._raw_input = self._raw_input[:-1]
            if self._raw_input:
                self._set_input(self._raw_input)
            else:
                self._clear_rime()
                self._preedit = ""
                self._candidates = []
                self._refresh_preview()
                self._refresh_cands()
        elif self._committed:
            self._committed = self._committed[:-1]
            self._refresh_preview()

    def _bs_start(self):
        self._backspace()
        self._bs_held = True
        self._bs_delay = QTimer(self)
        self._bs_delay.setSingleShot(True)
        self._bs_delay.setInterval(400)
        self._bs_delay.timeout.connect(self._bs_repeat_start)
        self._bs_delay.start()

    def _bs_repeat_start(self):
        if self._bs_held:
            self._bs_timer.start()

    def _bs_stop(self):
        self._bs_held = False
        if hasattr(self, '_bs_delay') and self._bs_delay.isActive():
            self._bs_delay.stop()
        if hasattr(self, '_bs_timer') and self._bs_timer.isActive():
            self._bs_timer.stop()

    def _enter(self):
        if self._raw_input:
            self._committed += self._raw_input
            self._clear_rime()
            self._preedit = ""
            self._candidates = []
            self._refresh_preview()
            self._refresh_cands()
        elif self._committed.strip():
            self._on_send()

    def _space(self):
        if self._candidates:
            self._pick(0)
        else:
            self._committed += " "
            self._refresh_preview()

    def _pick(self, idx: int):
        try:
            r = self.bridge.rime_select(idx)
            self._preedit = r.get("preedit", "")
            self._candidates = r.get("candidates", [])
            self._page_no = r.get("page_no", 0)
            self._is_last = r.get("is_last_page", False)
            if r.get("committed"):
                self._committed += r["committed"]
                self._raw_input = ""  # 已上屏，清空原始输入
            self._refresh_preview()
            self._refresh_cands()
        except Exception as e:
            logger.error("rime_select 失败: %s", e)

    def _page(self, back: bool):
        try:
            r = self.bridge.rime_page(back)
            self._candidates = r.get("candidates", [])
            self._page_no = r.get("page_no", 0)
            self._is_last = r.get("is_last_page", False)
            self._refresh_cands()
        except Exception as e:
            logger.error("rime_page 失败: %s", e)

    def _toggle_mode(self):
        try:
            r = self.bridge.rime_toggle_mode()
            self._ascii = r.get("is_ascii_mode", False)
            self._mode_btn.setText("中英" if self._ascii else "中英")
            self._shift_btn.setText("⇧" if self._ascii else "分词")
            if self._ascii:
                self._preedit = ""
                self._raw_input = ""
                self._candidates = []
                self._refresh_cands()
            self._refresh_preview()
        except Exception as e:
            logger.error("toggle_mode 失败: %s", e)

    def _shift_action(self):
        if self._ascii:
            self._toggle_case()
        else:
            # 中文模式：插入隔音符，仅在有拼音时有效
            if self._raw_input:
                self._raw_input += "'"
                self._set_input(self._raw_input)

    def _toggle_case(self):
        self._upper = not self._upper
        self._refresh_labels()

    def _punct(self, ch: str):
        if not self._ascii and self._raw_input:
            # 中文模式有拼音：用 set_input 将标点嵌入拼音
            self._raw_input += ch
            self._set_input(self._raw_input)
        elif self._cn_punct and not self._ascii:
            self._committed += _CN_PUNCT.get(ch, ch)
            self._refresh_preview()
        else:
            self._committed += ch
            self._refresh_preview()

    def _clear_rime(self):
        self._raw_input = ""
        try:
            self.bridge.rime_clear()
        except Exception:
            pass

    def _on_send(self):
        t = self._committed.strip()
        if not t:
            return
        opts = self.bridge.build_submit_opts()
        self._committed = ""
        self._preedit = ""
        self._raw_input = ""
        self._candidates = []
        self._clear_rime()
        self._refresh_preview()
        self._refresh_cands()
        self.request_send.emit(t, opts)
