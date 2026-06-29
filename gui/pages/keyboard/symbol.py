"""符号键盘布局"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .base import FN_RATIO, KEY_H, KEY_W, BaseKeyboardLayout

# 符号键盘分类数据
SYM_CATS = {
    "中文": [
        "，",
        "。",
        "？",
        "！",
        "：",
        "；",
        "、",
        "“",
        "”",
        "（",
        "）",
        "【",
        "】",
        "《",
        "》",
        "—",
        "…",
        "～",
        "·",
        "「",
        "」",
        "『",
        "』",
        "〈",
        "〉",
        "〔",
        "〕",
        "‖",
        "｜",
    ],
    "英文": [
        ",",
        ".",
        "?",
        "!",
        ":",
        ";",
        "'",
        '"',
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "@",
        "#",
        "$",
        "%",
        "&",
        "*",
        "+",
        "=",
        "/",
        "\\",
        "|",
        "_",
        "~",
        "^",
        "<",
        ">",
    ],
    "网络": [
        "www.",
        "http://",
        "https://",
        "@",
        ".com",
        ".cn",
        ".net",
        ".org",
        "/",
        "//",
        "://",
        "?",
        "&",
        "#",
        "=",
        "mailto:",
        "ftp://",
    ],
    "数字": [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "＋",
        "－",
        "×",
        "÷",
        "＝",
        "≠",
        "≈",
        "∞",
        "π",
        "∑",
        "∏",
        "√",
        "∫",
        "∂",
        "∈",
        "∉",
        "⊂",
        "⊃",
        "∪",
        "∩",
    ],
    "角标": [
        "⁰",
        "¹",
        "²",
        "³",
        "⁴",
        "⁵",
        "⁶",
        "⁷",
        "⁸",
        "⁹",
        "₀",
        "₁",
        "₂",
        "₃",
        "₄",
        "₅",
        "₆",
        "₇",
        "₈",
        "₉",
        "ⁿ",
        "ⁱ",
        "⁺",
        "⁻",
        "⁼",
        "⁽",
        "⁾",
        "ₑ",
    ],
    "序号": [
        "①",
        "②",
        "③",
        "④",
        "⑤",
        "⑥",
        "⑦",
        "⑧",
        "⑨",
        "⑩",
        "⑪",
        "⑫",
        "⑬",
        "⑭",
        "⑮",
        "⑯",
        "⑰",
        "⑱",
        "⑲",
        "⑳",
        "Ⅰ",
        "Ⅱ",
        "Ⅲ",
        "Ⅳ",
        "Ⅴ",
        "Ⅵ",
        "Ⅶ",
        "Ⅷ",
        "Ⅸ",
        "Ⅹ",
    ],
    "音标": [
        "ɑ",
        "ɔ",
        "ɜ",
        "ɪ",
        "ʊ",
        "ə",
        "æ",
        "ʌ",
        "ɒ",
        "ɛ",
        "ʒ",
        "ʃ",
        "θ",
        "ð",
        "ŋ",
        "ɡ",
        "tʃ",
        "dʒ",
        "ˈ",
        "ˌ",
        "ː",
        "ˑ",
        "˘",
    ],
    "平假": [
        "あ",
        "い",
        "う",
        "え",
        "お",
        "か",
        "き",
        "く",
        "け",
        "こ",
        "さ",
        "し",
        "す",
        "せ",
        "そ",
        "た",
        "ち",
        "つ",
        "て",
        "と",
        "な",
        "に",
        "ぬ",
        "ね",
        "の",
        "は",
        "ひ",
        "ふ",
        "へ",
        "ほ",
        "ま",
        "み",
        "む",
        "め",
        "も",
        "や",
        "ゆ",
        "よ",
        "ら",
        "り",
        "る",
        "れ",
        "ろ",
        "わ",
        "を",
        "ん",
    ],
    "片假": [
        "ア",
        "イ",
        "ウ",
        "エ",
        "オ",
        "カ",
        "キ",
        "ク",
        "ケ",
        "コ",
        "サ",
        "シ",
        "ス",
        "セ",
        "ソ",
        "タ",
        "チ",
        "ツ",
        "テ",
        "ト",
        "ナ",
        "ニ",
        "ヌ",
        "ネ",
        "ノ",
        "ハ",
        "ヒ",
        "フ",
        "ヘ",
        "ホ",
        "マ",
        "ミ",
        "ム",
        "メ",
        "モ",
        "ヤ",
        "ユ",
        "ヨ",
        "ラ",
        "リ",
        "ル",
        "レ",
        "ロ",
        "ワ",
        "ヲ",
        "ン",
    ],
    "箭头": [
        "←",
        "→",
        "↑",
        "↓",
        "↔",
        "↕",
        "⇐",
        "⇒",
        "⇑",
        "⇓",
        "⇔",
        "⇕",
        "↺",
        "↻",
        "⟳",
        "⟲",
        "⬆",
        "⬇",
        "⬅",
        "➡",
        "▲",
        "▼",
        "◀",
        "▶",
        "△",
        "▽",
        "▷",
        "◁",
        "▵",
        "▿",
    ],
    "颜文字": [
        "(⌒▽⌒)",
        "(´・ω・`)",
        "(；´д`)",
        "orz",
        "Σ(°△°|||)",
        "(￣▽￣)",
        "(*^▽^*)",
        "(｡>﹏<｡)",
        "qwq",
        "QAQ",
        "TAT",
        "owo",
        "uwu",
        "XD",
        ":D",
        ":P",
        "^_^",
        "T_T",
        ">_<",
        "=_=",
    ],
}

# 符号网格常量
_SYM_COLS = 4
_SYM_VISIBLE_ROWS = 5
_SYM_CELL_W = 48
_SYM_CELL_H = 96
_SYM_GRID_SP = 4


class SymbolLayout(BaseKeyboardLayout):
    """符号键盘：4×5 可滚动符号矩阵 + 单行分类栏（含退格、返回）"""

    def __init__(self, parent=None):
        self._active_cat = "中文"
        self._cat_btns: dict[str, QPushButton] = {}
        self._grid: QGridLayout | None = None
        self._grid_widget: QWidget | None = None
        self._scroll: QScrollArea | None = None
        super().__init__(parent)

    def base_size(self) -> tuple[int, int]:
        w = _SYM_COLS * _SYM_CELL_W + (_SYM_COLS - 1) * _SYM_GRID_SP + 16
        h = _SYM_VISIBLE_ROWS * _SYM_CELL_H + (_SYM_VISIBLE_ROWS - 1) * _SYM_GRID_SP + 36 + 16
        return (w, h)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 6, 8, 6)
        outer.setSpacing(4)

        # ── 可滚动符号区域（固定 5 行高度） ──
        grid_h = _SYM_VISIBLE_ROWS * _SYM_CELL_H + (_SYM_VISIBLE_ROWS - 1) * _SYM_GRID_SP
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFixedHeight(grid_h)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._grid_widget = QWidget()
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setContentsMargins(4, 4, 4, 4)
        self._grid.setSpacing(_SYM_GRID_SP)
        self._scroll.setWidget(self._grid_widget)
        outer.addWidget(self._scroll)

        # ── 单行分类栏 ──
        catbar = QFrame()
        catbar.setObjectName("sym_catbar")
        cat_row = QHBoxLayout(catbar)
        cat_row.setContentsMargins(4, 2, 4, 2)
        cat_row.setSpacing(3)

        for cat in SYM_CATS:
            b = QPushButton(cat)
            b.setObjectName("sym_cat")
            b.setProperty("active", cat == self._active_cat)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, c=cat: self._load_cat(c))
            cat_row.addWidget(b)
            self._cat_btns[cat] = b

        cat_row.addStretch(1)

        # 退格
        bs = QPushButton("⌫")
        bs.setObjectName("fn")
        bs.setFixedSize(int(KEY_W * 0.8), KEY_H)
        bs.setCursor(Qt.CursorShape.PointingHandCursor)
        bs.clicked.connect(lambda: self.backspace.emit())
        cat_row.addWidget(bs)

        # 返回
        back = QPushButton("返回")
        back.setObjectName("fn")
        back.setFixedSize(int(KEY_W * FN_RATIO), KEY_H)
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(lambda: self.command.emit("back"))
        cat_row.addWidget(back)

        outer.addWidget(catbar)

        # 加载默认分类
        self._load_cat(self._active_cat)

    def _load_cat(self, cat: str):
        """切换符号分类"""
        if cat not in SYM_CATS:
            return
        self._active_cat = cat

        # 更新高亮
        for name, btn in self._cat_btns.items():
            btn.setProperty("active", name == cat)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # 清空 grid
        grid = self._grid
        while grid.count():
            item = grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        # 填充符号按钮
        cols = _SYM_COLS
        for c in range(cols):
            grid.setColumnStretch(c, 1)
        chars = SYM_CATS[cat]
        for i, ch in enumerate(chars):
            btn = QPushButton(ch)
            btn.setObjectName("sym")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, c=ch: self.key_input.emit(c))
            grid.addWidget(btn, i // cols, i % cols)

        # 设置 grid 最小高度，确保超出可视区域时可滚动
        rows = (len(chars) + cols - 1) // cols
        min_h = (_SYM_CELL_H + _SYM_GRID_SP) * rows
        self._grid_widget.setMinimumHeight(min_h)

    def apply_scale(self, scale: float):
        """符号键盘的缩放：只更新 scroll 高度"""
        grid_h = _SYM_VISIBLE_ROWS * _SYM_CELL_H + (_SYM_VISIBLE_ROWS - 1) * _SYM_GRID_SP
        self._scroll.setFixedHeight(grid_h)
