"""九键键盘布局（T9 拼音输入）——完全对齐 numpad 规范"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .base import BaseKeyboardLayout

# T9 字母映射
_T9_MAP = {
    "2": "ABC",
    "3": "DEF",
    "4": "GHI",
    "5": "JKL",
    "6": "MNO",
    "7": "PQRS",
    "8": "TUV",
    "9": "WXYZ",
}

# 基准尺寸（与 numpad 一致）
_NK_COLS = 5
_NK_ROWS = 4
_NK_CELL_W = 48
_NK_CELL_H = 48
_NK_SP = 4


class NineKeyLayout(BaseKeyboardLayout):
    """九键 T9 拼音键盘布局"""

    def __init__(self, parent=None):
        self._sym_scroll: QScrollArea | None = None
        self._mode_btn: QPushButton | None = None
        super().__init__(parent)

    def base_size(self) -> tuple[int, int]:
        sym_w = round(_NK_CELL_W * 1.1)
        w = sym_w + (_NK_COLS - 1) * _NK_CELL_W + (_NK_COLS - 1) * _NK_SP + 16
        h = _NK_ROWS * _NK_CELL_H + (_NK_ROWS - 1) * _NK_SP + 16
        return (w, h)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 6, 8, 6)
        outer.setSpacing(_NK_SP)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(_NK_SP)
        grid.setColumnStretch(0, 0)
        for c in range(1, 5):
            grid.setColumnStretch(c, 1)

        # ── 符号容器（col=0, row=0, 跨3行） ──
        self._sym_scroll = self._build_sym_container()
        grid.addWidget(self._sym_scroll, 0, 0, 3, 1)

        # Row 0: [sym] [标] [2 ABC] [3 DEF] [退格]
        grid.addWidget(self._make_t9_btn("1", "标"), 0, 1)
        grid.addWidget(self._make_t9_btn("2"), 0, 2)
        grid.addWidget(self._make_t9_btn("3"), 0, 3)
        grid.addWidget(self._make_fn_btn("⌫", "bs"), 0, 4)

        # Row 1: [sym] [4 GHI] [5 JKL] [6 MNO] [重输]
        grid.addWidget(self._make_t9_btn("4"), 1, 1)
        grid.addWidget(self._make_t9_btn("5"), 1, 2)
        grid.addWidget(self._make_t9_btn("6"), 1, 3)
        grid.addWidget(self._make_cmd_btn("重输", "retype"), 1, 4)

        # Row 2: [sym] [7 PQRS] [8 TUV] [9 WXYZ] [0]
        grid.addWidget(self._make_t9_btn("7"), 2, 1)
        grid.addWidget(self._make_t9_btn("8"), 2, 2)
        grid.addWidget(self._make_t9_btn("9"), 2, 3)
        grid.addWidget(self._make_punct_btn("0"), 2, 4)

        # Row 3: [符] [123] [空格] [中] [回车]
        sym_btn = self._make_cmd_btn("符", "show:symbol")
        sym_btn.setFixedWidth(int(_NK_CELL_W * 1.1))
        grid.addWidget(sym_btn, 3, 0)
        grid.addWidget(self._make_cmd_btn("123", "show:numpad"), 3, 1)
        grid.addWidget(self._make_space_btn(), 3, 2)
        self._mode_btn = self._make_cmd_btn("中", "toggle_mode")
        grid.addWidget(self._mode_btn, 3, 3)
        grid.addWidget(self._make_cmd_btn("回车", "enter"), 3, 4)

        outer.addLayout(grid)

    # ── 符号容器 ──

    def _build_sym_container(self) -> QScrollArea:
        symbols = "% / # + - * : _ = < > ( ) [ ] { } ~ ^ & |".split()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(int(_NK_CELL_W * 1.1))
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        inner = QWidget()
        vbox = QVBoxLayout(inner)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(_NK_SP)

        for ch in symbols:
            btn = QPushButton(ch)
            btn.setObjectName("p")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("base_font_size", 20)
            btn.clicked.connect(lambda _, c=ch: self.punct.emit(c))
            vbox.addWidget(btn)

        scroll.setWidget(inner)
        return scroll

    # ── 按钮工厂 ──

    def _make_punct_btn(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("p")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", 26)
        btn.clicked.connect(lambda _, v=text: self.punct.emit(v))
        self._scaleable_buttons.append((btn, 1.0))
        return btn

    def _make_t9_btn(self, digit: str, label: str | None = None) -> QWidget:
        """T9 键：大标签 + 小字母，容器整体可缩放。digit 传给 RIME，label 为显示文本"""
        letters = _T9_MAP.get(digit, "")
        display = label if label is not None else digit

        container = QWidget()
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        container.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        container.setCursor(Qt.CursorShape.PointingHandCursor)

        lay = QVBoxLayout(container)
        lay.setContentsMargins(2, 2, 2, 2)
        lay.setSpacing(0)

        digit_lbl = QLabel(display)
        digit_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        digit_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        lay.addWidget(digit_lbl, 1)

        if letters:
            letter_lbl = QLabel(letters)
            letter_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            letter_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            lay.addWidget(letter_lbl)
        else:
            letter_lbl = None

        container._digit_lbl = digit_lbl
        container._letter_lbl = letter_lbl
        container._digit = digit
        container._hover = False
        container._pressed = False

        def _update_ss():
            bg = "#d8d7d4" if container._pressed else ("#eae9e6" if container._hover else "#ffffff")
            border = "#b0afac" if container._pressed else ("#c8c7c4" if container._hover else "#c8c7c4")
            container.setStyleSheet(f"background: {bg}; border: 1px solid {border}; border-radius: 5px;")

        container._update_ss = _update_ss
        _update_ss()

        def _enter(e):
            container._hover = True
            _update_ss()

        def _leave(e):
            container._hover = False
            _update_ss()

        def _press(e):
            container._pressed = True
            _update_ss()
            self.key_input.emit(digit)

        def _release(e):
            container._pressed = False
            _update_ss()

        container.enterEvent = _enter
        container.leaveEvent = _leave
        container.mousePressEvent = _press
        container.mouseReleaseEvent = _release

        self._scaleable_buttons.append((container, 1.0))
        return container

    def _make_fn_btn(self, text: str, cmd: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("fn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", 24)
        if cmd == "bs":
            btn.pressed.connect(lambda: self.command.emit("bs_start"))
            btn.released.connect(lambda: self.command.emit("bs_stop"))
        else:
            btn.clicked.connect(lambda _, v=cmd: self.command.emit(v))
        self._scaleable_buttons.append((btn, 1.0))
        return btn

    def _make_cmd_btn(self, text: str, cmd: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("p" if cmd not in ("enter",) else "ent")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", 24)
        btn.clicked.connect(lambda _, v=cmd: self.command.emit(v))
        self._scaleable_buttons.append((btn, 1.0))
        return btn

    def _make_space_btn(self) -> QPushButton:
        btn = QPushButton("空格")
        btn.setObjectName("sp")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", 22)
        btn.clicked.connect(lambda: self.space.emit())
        self._scaleable_buttons.append((btn, 1.0))
        return btn

    # ── 接口 ──

    def set_mode_icon(self, icon):
        if self._mode_btn:
            self._mode_btn.setIcon(icon)
            self._mode_btn.setText("")

    def apply_scale(self, scale: float):
        cell_w = max(32, round(_NK_CELL_W * scale))
        cell_h = max(28, round(_NK_CELL_H * scale))
        sym_w = max(28, round(_NK_CELL_W * 1.1 * scale))
        sp = max(2, round(_NK_SP * scale))

        # 更新符号容器宽度
        if self._sym_scroll:
            self._sym_scroll.setFixedWidth(sym_w)

        # 遍历所有可交互 widget（排除符号容器内）
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == "p" and btn.parent() and btn.parent().parent() == self._sym_scroll:
                continue
            if btn.text() == "符":
                btn.setFixedSize(sym_w, cell_h)
            else:
                btn.setFixedSize(cell_w, cell_h)

        # T9 容器缩放
        for item in self.findChildren(QWidget):
            if hasattr(item, "_digit_lbl"):
                item.setFixedSize(cell_w, cell_h)
                # 字号跟随缩放
                digit_fs = max(12, round(22 * scale))
                letter_fs = max(7, round(10 * scale))
                item._digit_lbl.setStyleSheet(
                    f"font-size: {digit_fs}px; font-weight: 600; color: #1a1a1a; background: transparent; border: none;"
                )
                if item._letter_lbl:
                    item._letter_lbl.setStyleSheet(
                        f"font-size: {letter_fs}px; color: #888; background: transparent; border: none;"
                    )

        # 更新间距
        grid = self.layout().itemAt(0).layout()
        if grid:
            grid.setSpacing(sp)
