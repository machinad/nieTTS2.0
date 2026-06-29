"""26 键 QWERTY 键盘布局"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy,
)

from .base import (
    BaseKeyboardLayout, SwipeKey, KEY_W, KEY_H,
    FN_RATIO, SPACE_RATIO, BASE_SPACING,
)

# 长按上滑输入映射
_SWIPE_MAP = {
    "q": "1", "w": "2", "e": "3", "r": "4", "t": "5",
    "y": "6", "u": "7", "i": "8", "o": "9", "p": "0",
    "a": "~", "s": "!", "d": "@", "f": "#", "g": "%",
    "h": "“", "j": "”", "k": "*", "l": "?",
    "z": "(", "x": ")", "c": "-", "v": "_", "b": ":",
    "n": ";", "m": "/",
}

# 基准键盘总宽 / 总高
_BASE_KB_WIDTH = 10 * KEY_W + 9 * BASE_SPACING   # 507
_BASE_KB_HEIGHT = 4 * KEY_H + 3 * BASE_SPACING   # 177


class QwertyLayout(BaseKeyboardLayout):
    """26 键 QWERTY 键盘：支持上滑输入、双拼提示。"""

    def __init__(self, hint_map: dict[str, str] | None = None,
                 parent=None):
        self._hint_map = hint_map
        self._letter_btns: dict[str, QPushButton] = {}
        self._hint_labels: dict[str, QLabel] = {}
        self._shift_btn: QPushButton | None = None
        self._mode_btn: QPushButton | None = None
        super().__init__(parent)

    def base_size(self) -> tuple[int, int]:
        return (_BASE_KB_WIDTH, _BASE_KB_HEIGHT)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(10, 6, 10, 6)
        outer.setSpacing(BASE_SPACING)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        outer.addWidget(self._mk_row("qwertyuiop"),
                        alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addWidget(self._mk_row("asdfghjkl"),
                        alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addWidget(self._mk_row_zxcv(),
                        alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addWidget(self._mk_row_bottom(),
                        alignment=Qt.AlignmentFlag.AlignHCenter)

    # ── 行构建 ──

    def _mk_row(self, keys: str) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(BASE_SPACING)
        for ch in keys:
            h.addWidget(self._mk_key(ch))
        return w

    def _mk_row_zxcv(self) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(BASE_SPACING)

        self._shift_btn = self._mk_fn("分词")
        self._shift_btn.clicked.connect(lambda: self.command.emit("shift"))
        h.addWidget(self._shift_btn)

        for ch in "zxcvbnm":
            h.addWidget(self._mk_key(ch))

        bs = self._mk_fn("⌫")
        bs.pressed.connect(lambda: self.command.emit("bs_start"))
        bs.released.connect(lambda: self.command.emit("bs_stop"))
        h.addWidget(bs)
        return w

    def _mk_row_bottom(self) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(BASE_SPACING)

        # 符号
        sym = self._mk_fn("符号")
        sym.clicked.connect(lambda: self.command.emit("show:symbol"))
        h.addWidget(sym)

        # 123
        num = self._mk_fn("123")
        num.clicked.connect(lambda: self.command.emit("show:numpad"))
        h.addWidget(num)

        # 逗号
        comma = QPushButton(",")
        comma.setObjectName("p")
        comma.setFixedSize(int(KEY_W * 0.5), KEY_H)
        comma.setCursor(Qt.CursorShape.PointingHandCursor)
        comma.setProperty("base_font_size", 30)
        comma.clicked.connect(lambda: self.punct.emit(","))
        self._scaleable_buttons.append((comma, 0.5))
        h.addWidget(comma)

        # 空格
        sp = QPushButton("空格")
        sp.setObjectName("sp")
        sp.setFixedSize(int(KEY_W * SPACE_RATIO), KEY_H)
        sp.setCursor(Qt.CursorShape.PointingHandCursor)
        sp.setProperty("base_font_size", 26)
        sp.clicked.connect(lambda: self.space.emit())
        self._scaleable_buttons.append((sp, SPACE_RATIO))
        h.addWidget(sp)

        # 句号
        period = QPushButton(".")
        period.setObjectName("p")
        period.setFixedSize(int(KEY_W * 0.5), KEY_H)
        period.setCursor(Qt.CursorShape.PointingHandCursor)
        period.setProperty("base_font_size", 30)
        period.clicked.connect(lambda: self.punct.emit("."))
        self._scaleable_buttons.append((period, 0.5))
        h.addWidget(period)

        # 中英切换
        self._mode_btn = QPushButton()
        self._mode_btn.setObjectName("mode")
        self._mode_btn.setFixedSize(KEY_W, KEY_H)
        self._mode_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._mode_btn.setProperty("base_font_size", 28)
        self._mode_btn.clicked.connect(lambda: self.command.emit("toggle_mode"))
        self._scaleable_buttons.append((self._mode_btn, 1.0))
        h.addWidget(self._mode_btn)

        # 回车
        ent = QPushButton("↵")
        ent.setObjectName("ent")
        ent.setFixedSize(int(KEY_W * FN_RATIO), KEY_H)
        ent.setCursor(Qt.CursorShape.PointingHandCursor)
        ent.setProperty("base_font_size", 30)
        ent.clicked.connect(lambda: self.command.emit("enter"))
        self._scaleable_buttons.append((ent, FN_RATIO))
        h.addWidget(ent)
        return w

    def _mk_key(self, ch: str) -> QPushButton:
        swipe_ch = _SWIPE_MAP.get(ch)
        b = SwipeKey(ch, swipe_ch)
        b.setObjectName("k")
        b.setFixedSize(KEY_W, KEY_H)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setProperty("base_font_size", 30)
        b.clicked.connect(lambda _, c=ch: self.key_input.emit(c))
        if swipe_ch:
            b.swipe_up.connect(lambda c=swipe_ch: self.key_input.emit(c))
            b._tip.setProperty("base_font_size", 13)
        if ch.isalpha():
            self._letter_btns[ch] = b
            # 双拼提示
            if self._hint_map and ch in self._hint_map:
                hint = self._hint_map[ch]
                tip = QLabel(hint, b)
                tip.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
                tip.setStyleSheet("font-size: 9px; color: #9b9a98; background: transparent; border: none;")
                tip.setGeometry(0, b.height() - 14, b.width(), 12)
                self._hint_labels[ch] = tip
        self._scaleable_buttons.append((b, 1.0))
        return b

    def _mk_fn(self, text: str) -> QPushButton:
        b = self._make_key(text, "fn", 28, FN_RATIO)
        b.setFixedSize(int(KEY_W * FN_RATIO), KEY_H)
        return b

    # ── 接口覆写 ──

    def refresh_labels(self, upper: bool):
        """中文模式始终大写，英文模式由 upper 控制。"""
        for ch, b in self._letter_btns.items():
            b.setText(ch.upper() if upper else ch)

    def set_mode_icon(self, icon):
        """设置中英切换按钮图标。"""
        if self._mode_btn:
            from PySide6.QtCore import QSize
            self._mode_btn.setIcon(icon)
            self._mode_btn.setIconSize(QSize(32, 24))

    def set_shift_text(self, text: str):
        """设置 Shift 按钮文本。"""
        if self._shift_btn:
            self._shift_btn.setText(text)

    def on_schema_changed(self, hint_map: dict[str, str] | None):
        """更新双拼提示。支持在构造后动态设置／更新提示标签。"""
        self._hint_map = hint_map
        if hint_map is None:
            # 全拼方案：隐藏所有提示
            for ch, lbl in self._hint_labels.items():
                lbl.hide()
            return
        for ch, hint in hint_map.items():
            if ch in self._hint_labels:
                # 已有标签 → 更新文本并显示
                self._hint_labels[ch].setText(hint)
                self._hint_labels[ch].show()
            elif ch in self._letter_btns:
                # 无标签但字母键存在 → 动态创建
                btn = self._letter_btns[ch]
                tip = QLabel(hint, btn)
                tip.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
                tip.setStyleSheet("font-size: 9px; color: #9b9a98; background: transparent; border: none;")
                tip.setGeometry(0, btn.height() - 14, btn.width(), 12)
                tip.show()
                self._hint_labels[ch] = tip
        # 隐藏不再有提示的旧标签
        for ch, lbl in self._hint_labels.items():
            if ch not in hint_map:
                lbl.hide()

    def apply_scale(self, scale: float):
        """26 键缩放：按钮尺寸 + SwipeKey 提示 + 双拼提示"""
        super().apply_scale(scale)
        # 更新双拼提示位置
        tip_h = max(10, round(12 * scale))
        for ch, lbl in self._hint_labels.items():
            btn = self._letter_btns.get(ch)
            if btn:
                lbl.setGeometry(0, btn.height() - tip_h, btn.width(), tip_h - 2)
                lbl.setStyleSheet(f"font-size: {max(7, round(9 * scale))}px; "
                                  "color: #9b9a98; background: transparent; border: none;")
