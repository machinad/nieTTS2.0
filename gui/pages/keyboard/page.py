"""键盘页面：协调者（预览栏 + 候选栏 + 方案栏 + 布局切换）"""

import logging
from PySide6.QtCore import Qt, Signal, QSize, QTimer
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QSizePolicy, QStackedWidget,
)

from gui.pages.keyboard.base import BaseKeyboardLayout, KEY_W, KEY_H, FN_RATIO
from gui.pages.keyboard.qwerty import QwertyLayout
from gui.pages.keyboard.symbol import SymbolLayout
from gui.pages.keyboard.numpad import NumberPadLayout
from gui.pages.keyboard.ninekey import NineKeyLayout
from gui.pages.keyboard.shuangpin_maps import SHUANGPIN_HINT_MAPS

logger = logging.getLogger(__name__)

_CN_PUNCT = {",": "，", ".": "。", "?": "？", "!": "！", ";": "；", ":": "："}

# ── 中/英模式图标 ──

def _build_mode_icons() -> tuple[QIcon, QIcon]:
    """用 QPainter 绘制中/英层叠图标，返回 (cn_icon, en_icon)"""
    w, h = 32, 24
    icons = []
    for is_en in (False, True):
        pm = QPixmap(w, h)
        pm.fill(Qt.GlobalColor.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        p.setPen(QColor("white"))
        if is_en:
            p.setOpacity(0.5)
            p.setFont(QFont("Microsoft YaHei", 8, QFont.Weight.Bold))
            p.drawText(0, 4, 18, h, Qt.AlignmentFlag.AlignCenter, "中")
            p.setOpacity(1.0)
            p.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            p.drawText(6, 0, 26, h, Qt.AlignmentFlag.AlignCenter, "EN")
        else:
            p.setOpacity(0.5)
            p.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            p.drawText(14, 4, 18, h, Qt.AlignmentFlag.AlignCenter, "en")
            p.setOpacity(1.0)
            p.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
            p.drawText(0, 0, 26, h, Qt.AlignmentFlag.AlignCenter, "中")
        p.end()
        icons.append(QIcon(pm))
    return icons  # [cn_icon, en_icon]


# ── QSS 样式 ──

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
    font-size: {mode_fs}px; color: #ffffff;
}}
QPushButton#mode:hover {{ background: #c4507a; }}
QPushButton#mode:pressed {{ background: #b8507a; border-color: #a8406a; }}

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

/* ── 符号键盘 ── */
QPushButton#sym {{
    background: #ffffff; border: 1px solid #c8c7c4; border-radius: 5px;
    font-size: 18px; color: #1a1a1a;
    min-height: 96px;
}}
QPushButton#sym:hover {{ background: #eae9e6; }}
QPushButton#sym:pressed {{ background: #d8d7d4; border-color: #b0afac; }}
QFrame#sym_catbar {{
    background: #f8f7f5; border: 1px solid #e0dfdc;
    border-radius: 5px;
}}
QPushButton#sym_cat {{
    background: transparent; border: 1px solid transparent;
    border-radius: 3px; padding: 2px 6px;
    font-size: 13px; color: #6a6a68;
    min-height: 28px; max-height: 28px;
}}
QPushButton#sym_cat:hover {{ background: #eae9e6; }}
QPushButton#sym_cat[active="true"] {{
    background: #9a6ad6; color: #ffffff; border-color: #8a5ac6;
}}
"""

# 基准字号（scale=1.0 时）
_FONT_K = 14
_FONT_FN = 14
_FONT_MODE = 16
_FONT_P = 18
_FONT_SP = 15
_FONT_ENT = 18


def _build_qss(scale: float = 1.0) -> str:
    s = lambda base: max(10, round(base * scale))
    return _QSS.format(
        k_fs=s(_FONT_K), fn_fs=s(_FONT_FN), mode_fs=s(_FONT_MODE),
        p_fs=s(_FONT_P), sp_fs=s(_FONT_SP), ent_fs=s(_FONT_ENT),
    )


# ══════════════════════════════════════════════════════════════

class KeyboardPage(QWidget):
    """虚拟键盘输入页面（协调者）"""

    request_send = Signal(str, dict)

    def __init__(self, bridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self.setStyleSheet(_build_qss())

        # ── 共用输入状态 ──
        self._committed = ""
        self._preedit = ""
        self._raw_input = ""
        self._candidates: list[str] = []
        self._page_no = 0
        self._is_last = False
        self._ascii = False
        self._upper = False
        self._cn_punct = True
        self._icon_cn, self._icon_en = _build_mode_icons()
        self._last_scale: float = 0.0  # 缓存上次缩放值，避免重复 setStyleSheet

        # ── 退格长按 ──
        self._bs_held = False
        self._bs_timer = QTimer(self)
        self._bs_timer.setInterval(100)
        self._bs_timer.timeout.connect(self._backspace)

        # ── 布局管理 ──
        self._stack = QStackedWidget()
        self._layouts: dict[str, BaseKeyboardLayout] = {}
        self._current_layout: BaseKeyboardLayout | None = None
        self._layout_stack: list[str] = []  # 布局导航栈，用于"返回"按钮

        self._build_ui()

        # 注册布局
        self._register("qwerty", QwertyLayout())
        self._register("symbol", SymbolLayout())
        self._register("numpad", NumberPadLayout())
        self._register("ninekey", NineKeyLayout())

        # 默认显示 26 键
        self._switch_to("qwerty")

        # 初次加载时更新双拼提示
        try:
            initial = self.bridge.rime_current_schema()
            hint_map = SHUANGPIN_HINT_MAPS.get(initial)
            if hint_map is not None:
                self._layouts["qwerty"].on_schema_changed(hint_map)
        except Exception:
            pass

    # ── 构建 ──

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 8, 16, 8)
        root.setSpacing(6)

        root.addWidget(self._mk_preview())
        root.addWidget(self._mk_candbar())
        root.addWidget(self._mk_schema_bar())
        root.addWidget(self._stack, stretch=1)

    def _register(self, name: str, layout: BaseKeyboardLayout):
        self._layouts[name] = layout
        self._stack.addWidget(layout)
        layout.key_input.connect(self._on_key)
        layout.backspace.connect(self._on_backspace)
        layout.enter.connect(self._on_enter)
        layout.space.connect(self._on_space)
        layout.punct.connect(self._on_punct)
        layout.command.connect(self._on_command)

    # ── 信号处理 ──

    def _on_command(self, cmd: str):
        if cmd.startswith("show:"):
            self._switch_to(cmd[5:])
        elif cmd == "back":
            target = self._layout_stack.pop() if self._layout_stack else "qwerty"
            self._switch_to(target, track_previous=False)
        elif cmd == "toggle_mode":
            self._toggle_mode()
        elif cmd == "shift":
            self._shift_action()
        elif cmd == "enter":
            self._enter()
        elif cmd == "send":
            self._on_send()
        elif cmd == "bs_start":
            self._bs_start()
        elif cmd == "bs_stop":
            self._bs_stop()
        elif cmd == "retype":
            self._clear_rime()
            self._preedit = ""
            self._candidates = []
            self._refresh_preview()
            self._refresh_cands()

    def _on_key(self, ch: str):
        """26 键字母/上划字符输入"""
        if self._ascii:
            self._committed += ch.upper() if self._upper else ch
            self._refresh_preview()
        else:
            self._raw_input += ch
            self._set_input(self._raw_input)

    def _on_backspace(self):
        self._backspace()

    def _on_enter(self):
        self._enter()

    def _on_space(self):
        self._space()

    def _on_punct(self, ch: str):
        if not self._ascii and self._raw_input:
            # 有拼音：嵌入 RIME
            self._raw_input += ch
            self._set_input(self._raw_input)
        elif self._cn_punct and not self._ascii:
            # 无拼音中文模式：中文标点直接上屏
            self._committed += _CN_PUNCT.get(ch, ch)
            self._refresh_preview()
        else:
            # 英文模式或无中文标点：直接上屏
            self._committed += ch
            self._refresh_preview()

    # ── 布局切换 ──

    def _sync_mode_to_layout(self, layout: BaseKeyboardLayout | None = None):
        """同步中英模式状态到指定布局（默认当前布局）"""
        layout = layout or self._current_layout
        if not layout:
            return
        layout.set_mode_icon(self._icon_en if self._ascii else self._icon_cn)
        layout.set_shift_text("⇧" if self._ascii else "分词")
        layout.refresh_labels(not self._ascii or self._upper)

    def _switch_to(self, name: str, track_previous: bool = True):
        layout = self._layouts.get(name)
        if not layout:
            return
        # 记录导航历史：show:XXX 时将当前布局压栈，"返回"时不压栈
        if track_previous and self._current_layout is not None:
            for key, val in self._layouts.items():
                if val is self._current_layout and key != name:
                    self._layout_stack.append(key)
                    break
        self._stack.setCurrentWidget(layout)
        self._current_layout = layout
        self._sync_mode_to_layout(layout)
        QTimer.singleShot(0, self._recalc_current)

    # ── 缩放 ──

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 防抖：动画期间多次 resize 只算最后一次
        if hasattr(self, '_resize_timer'):
            self._resize_timer.stop()
        else:
            self._resize_timer = QTimer(self)
            self._resize_timer.setSingleShot(True)
            self._resize_timer.timeout.connect(self._recalc_current)
        self._resize_timer.start(30)

    def showEvent(self, event):
        super().showEvent(event)
        self._refresh_labels()
        QTimer.singleShot(0, self._recalc_current)

    def _recalc_current(self):
        layout = self._current_layout
        if not layout:
            return
        geo = layout.geometry()
        bw, bh = layout.base_size()
        if bw <= 0 or bh <= 0:
            return
        scale = min(geo.width() / bw, geo.height() / bh)
        scale = max(0.5, scale)
        layout.apply_scale(scale)
        # 仅在缩放值变化时重建 QSS，避免 resize 期间反复触发全量样式重算
        rounded = round(scale, 2)
        if rounded != self._last_scale:
            self._last_scale = rounded
            self.setStyleSheet(_build_qss(scale))

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

    _NINE_KEY_HINTS = ("t9", "nine", "九键", "九宫")

    @classmethod
    def _is_nine_key_schema(cls, schema_id: str, name: str) -> bool:
        """检测是否为九键方案"""
        text = (schema_id + " " + name).lower()
        return any(h in text for h in cls._NINE_KEY_HINTS)

    def _switch_schema(self, schema_id: str):
        try:
            logger.debug("switch_schema(%s) clearing state", schema_id)
            ok = self.bridge.rime_switch_schema(schema_id)
            if ok:
                # 持久化方案选择
                self.bridge.set_rime_schema(schema_id)
                for sid, b in self._schema_btns.items():
                    active = sid == schema_id
                    b.setProperty("active", active)
                    b.style().unpolish(b)
                    b.style().polish(b)
                # 根据方案类型切换键盘布局（方案切换清空导航栈，不压栈）
                self._layout_stack.clear()
                name = self._schema_btns[schema_id].text() if schema_id in self._schema_btns else ""
                if self._is_nine_key_schema(schema_id, name):
                    self._switch_to("ninekey", track_previous=False)
                    logger.debug("九键方案 → 切换到 ninekey 布局")
                elif self._current_layout is self._layouts.get("ninekey"):
                    # 从九键切回非九键方案时，回到 26 键
                    self._switch_to("qwerty", track_previous=False)
                else:
                    # 从符号/数字键盘等非主布局切换方案时，回到 26 键
                    self._switch_to("qwerty", track_previous=False)
                # 更新双拼提示
                hint_map = SHUANGPIN_HINT_MAPS.get(schema_id)
                qwerty = self._layouts.get("qwerty")
                if qwerty:
                    qwerty.on_schema_changed(hint_map)
                self._preedit = ""
                self._raw_input = ""
                self._candidates = []
                self._stop_bs_timer()
                self._refresh_preview()
                self._refresh_cands()
        except Exception as e:
            logger.error("切换方案失败: %s", e)

    # ── UI 刷新 ──

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
        logger.debug("refresh_cands: destroying %d old, creating %d new",
                     len(self._cand_btns), len(self._candidates))
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
        upper = not self._ascii or self._upper
        for layout in self._layouts.values():
            layout.refresh_labels(upper)

    # ── RIME 操作 ──

    def _set_input(self, text: str):
        try:
            r = self.bridge.rime_set_input(text)
            self._preedit = r.get("preedit", "")
            self._candidates = r.get("candidates", [])
            self._page_no = r.get("page_no", 0)
            self._is_last = r.get("is_last_page", False)
            if r.get("committed"):
                self._committed += r["committed"]
            logger.debug("set_input(%r) → preedit=%r, cands=%s, committed=%r",
                         text, self._preedit, self._candidates, r.get("committed"))
            self._refresh_preview()
            self._refresh_cands()
        except Exception as e:
            logger.error("rime_set_input 失败: %s", e)

    def _pick(self, idx: int):
        try:
            r = self.bridge.rime_select(idx)
            self._preedit = r.get("preedit", "")
            self._candidates = r.get("candidates", [])
            self._page_no = r.get("page_no", 0)
            self._is_last = r.get("is_last_page", False)
            if r.get("committed"):
                self._committed += r["committed"]
                self._raw_input = ""
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
            self._sync_mode_to_layout()
            if self._ascii:
                self._preedit = ""
                self._raw_input = ""
                self._candidates = []
                self._stop_bs_timer()
                self._refresh_cands()
            self._refresh_labels()
            self._refresh_preview()
        except Exception as e:
            logger.error("toggle_mode 失败: %s", e)

    # ── 按键动作 ──

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
        if hasattr(self, '_bs_delay') and self._bs_delay.isActive():
            self._bs_delay.stop()
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
        elif self._preedit:
            # 拼音区有内容但无候选（如含数字）→ 上屏拼音区文本
            self._committed += self._preedit
            self._clear_rime()
            self._preedit = ""
            self._candidates = []
            self._refresh_preview()
            self._refresh_cands()
        else:
            self._committed += " "
            self._refresh_preview()

    def _shift_action(self):
        if self._ascii:
            self._upper = not self._upper
            self._refresh_labels()
        elif self._raw_input:
            self._raw_input += "'"
            self._set_input(self._raw_input)

    def _stop_bs_timer(self):
        """停止退格长按 timer，防止其在后台持续删除新输入"""
        self._bs_held = False
        if self._bs_timer.isActive():
            self._bs_timer.stop()
        if hasattr(self, '_bs_delay') and self._bs_delay.isActive():
            self._bs_delay.stop()

    def _clear_rime(self):
        self._raw_input = ""
        self._stop_bs_timer()
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
