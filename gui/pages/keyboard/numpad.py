"""九宫格数字键盘布局"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy,
    QGridLayout, QScrollArea,
)

from .base import BaseKeyboardLayout, KEY_W, KEY_H, FN_RATIO, SPACE_RATIO

# 符号容器中的符号列表
_NP_SYMBOLS = [
    "%", "/", "#", "+", "-", "*", ":", "_",
    "(", ")", "$", "&", "~", "^", "|", "\\",
    "<", ">", "{", "}", "[", "]", "¥", "€",
]

# 基准尺寸
_NP_COLS = 5       # 总列数
_NP_ROWS = 4       # 总行数
_NP_CELL_W = 48    # 单元格基准宽
_NP_CELL_H = 48    # 单元格基准高
_NP_SP = 4         # 间距


class NumberPadLayout(BaseKeyboardLayout):
    """九宫格数字键盘：左侧符号容器 + 右侧数字/功能键"""

    def __init__(self, parent=None):
        self._sym_scroll: QScrollArea | None = None
        super().__init__(parent)

    def base_size(self) -> tuple[int, int]:
        w = _NP_COLS * _NP_CELL_W + (_NP_COLS - 1) * _NP_SP + 16
        h = _NP_ROWS * _NP_CELL_H + (_NP_ROWS - 1) * _NP_SP + 16
        return (w, h)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 6, 8, 6)
        outer.setSpacing(_NP_SP)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(_NP_SP)
        grid.setColumnStretch(0, 0)   # 符号列不拉伸
        for c in range(1, 5):
            grid.setColumnStretch(c, 1)  # 数字列拉伸

        # ── 符号容器（col=0, row=0, 跨3行） ──
        sym_container = self._build_sym_container()
        grid.addWidget(sym_container, 0, 0, 3, 1)

        # ── 数字和功能键 ──
        # Row 0: [1] [2] [3] [退格]
        grid.addWidget(self._make_punct_btn("1"), 0, 1)
        grid.addWidget(self._make_punct_btn("2"), 0, 2)
        grid.addWidget(self._make_punct_btn("3"), 0, 3)
        grid.addWidget(self._make_cmd_btn("⌫", "bs"), 0, 4)

        # Row 1: [4] [5] [6] [.]
        grid.addWidget(self._make_punct_btn("4"), 1, 1)
        grid.addWidget(self._make_punct_btn("5"), 1, 2)
        grid.addWidget(self._make_punct_btn("6"), 1, 3)
        grid.addWidget(self._make_punct_btn("."), 1, 4)

        # Row 2: [7] [8] [9] [@]
        grid.addWidget(self._make_punct_btn("7"), 2, 1)
        grid.addWidget(self._make_punct_btn("8"), 2, 2)
        grid.addWidget(self._make_punct_btn("9"), 2, 3)
        grid.addWidget(self._make_punct_btn("@"), 2, 4)

        # Row 3: [符] [返回] [0] [空格] [回车]
        sym_btn = self._make_cmd_btn("符", "show:symbol")
        sym_btn.setFixedWidth(int(_NP_CELL_W * 1.1))
        grid.addWidget(sym_btn, 3, 0)
        grid.addWidget(self._make_cmd_btn("返回", "back"), 3, 1)
        grid.addWidget(self._make_punct_btn("0"), 3, 2)
        grid.addWidget(self._make_space_btn(), 3, 3)
        grid.addWidget(self._make_cmd_btn("↵", "enter"), 3, 4)

        outer.addLayout(grid)

    def _build_sym_container(self) -> QScrollArea:
        """左侧可滚动符号列"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(int(_NP_CELL_W * 1.1))  # 比数字键略宽
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        inner = QWidget()
        vbox = QVBoxLayout(inner)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(_NP_SP)

        for ch in _NP_SYMBOLS:
            btn = QPushButton(ch)
            btn.setObjectName("p")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("base_font_size", 20)
            btn.clicked.connect(lambda _, c=ch: self.punct.emit(c))
            vbox.addWidget(btn)

        scroll.setWidget(inner)
        self._sym_scroll = scroll
        return scroll

    def _make_punct_btn(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("p")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", 26)
        btn.clicked.connect(lambda _, v=text: self.punct.emit(v))
        self._scaleable_buttons.append((btn, 1.0))
        return btn

    def _make_cmd_btn(self, text: str, cmd: str) -> QPushButton:
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

    def _make_space_btn(self) -> QPushButton:
        btn = QPushButton("空格")
        btn.setObjectName("sp")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", 22)
        btn.clicked.connect(lambda: self.space.emit())
        self._scaleable_buttons.append((btn, 1.0))
        return btn

    def apply_scale(self, scale: float):
        """数字键盘缩放"""
        cell_w = max(32, round(_NP_CELL_W * scale))
        cell_h = max(28, round(_NP_CELL_H * scale))
        sym_w = max(28, round(_NP_CELL_W * 1.1 * scale))
        sp = max(2, round(_NP_SP * scale))

        # 更新符号容器宽度
        if self._sym_scroll:
            self._sym_scroll.setFixedWidth(sym_w)

        # 遍历 grid 中所有按钮（排除符号容器内的按钮）
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == "p" and btn.parent() and btn.parent().parent() == self._sym_scroll:
                continue  # 跳过符号容器内的按钮
            if btn.text() == "符":
                btn.setFixedSize(sym_w, cell_h)
            else:
                btn.setFixedSize(cell_w, cell_h)

        # 更新间距
        grid = self.layout().itemAt(0).layout()
        if grid:
            grid.setSpacing(sp)
