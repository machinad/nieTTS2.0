"""键盘布局基类和通用组件"""

import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton

logger = logging.getLogger(__name__)

# ── 键盘基准尺寸（scale=1.0 时的像素值） ──
KEY_W = 48
KEY_H = 42
FN_RATIO = 1.38  # Shift/⌫/↵ 宽度比
SPACE_RATIO = 4.2  # 空格宽度比
BASE_SPACING = 3  # 基准间距


class SwipeKey(QPushButton):
    """支持上滑输入的按键：短按触发 clicked，上滑触发 swipe_up 信号。"""

    swipe_up = Signal(str)

    def __init__(self, text: str, swipe_char: str | None = None, parent=None):
        super().__init__(text, parent)
        self._swipe_char = swipe_char
        self._press_pos = None
        self._swiped = False
        self._swipe_threshold = 20

        if swipe_char:
            self._tip = QLabel(swipe_char, self)
            self._tip.setStyleSheet("font-size: 13px; color: #9b9a98; background: transparent; border: none;")
            self._tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._tip.setGeometry(0, 2, self.width(), 16)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "_tip"):
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


class BaseKeyboardLayout(QFrame):
    """所有键盘布局的基类。

    子类需实现：
    - _build_ui(): 构建布局 UI
    - base_size(): 返回基准 (width, height)

    子类可选覆写：
    - apply_scale(scale): 自定义缩放逻辑
    - refresh_labels(upper): 刷新大小写
    - on_schema_changed(hint_map): 方案切换回调
    """

    # ── 输出信号（→ KeyboardPage）──
    key_input = Signal(str)  # 字母/数字/符号输入
    backspace = Signal()  # 退格
    enter = Signal()  # 回车
    space = Signal()  # 空格
    punct = Signal(str)  # 标点
    command = Signal(str)  # 特殊命令

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("kb_container")
        self._scaleable_buttons: list[tuple[QPushButton, float]] = []
        self._build_ui()

    def _build_ui(self):
        """构建布局 UI，由 __init__ 调用。子类必须实现。"""
        raise NotImplementedError

    def base_size(self) -> tuple[int, int]:
        """返回基准 (width, height)，用于计算缩放比例。子类必须实现。"""
        raise NotImplementedError

    def set_mode_icon(self, icon):
        """设置中英切换按钮图标（由 KeyboardPage 调用）。子类可覆写。"""
        pass

    def set_shift_text(self, text: str):
        """设置 Shift 按钮文本（由 KeyboardPage 调用）。子类可覆写。"""
        pass

    def apply_scale(self, scale: float):
        """根据缩放因子调整按钮尺寸。子类可覆写。"""
        key_w = max(32, round(KEY_W * scale))
        key_h = max(28, round(KEY_H * scale))
        tip_fs = max(8, round(8 * scale))
        tip_h = max(10, round(16 * scale))
        for btn, ratio in self._scaleable_buttons:
            btn.setFixedSize(max(32, round(key_w * ratio)), key_h)
            if isinstance(btn, SwipeKey) and hasattr(btn, "_tip"):
                btn._tip.setStyleSheet(f"font-size: {tip_fs}px; color: #9b9a98; background: transparent; border: none;")
                btn._tip.setGeometry(0, round(2 * scale), btn.width(), tip_h)

    def refresh_labels(self, upper: bool):
        """刷新字母大小写（仅 26 键需要）。"""
        pass

    def on_schema_changed(self, hint_map: dict[str, str] | None):
        """方案切换时更新（如双拼提示）。"""
        pass

    # ── 工具方法 ──

    def _make_key(self, text: str, obj_name: str, base_fs: int, ratio: float = 1.0) -> QPushButton:
        """创建标准按钮并注册到缩放列表。"""
        btn = QPushButton(text)
        btn.setObjectName(obj_name)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", base_fs)
        self._scaleable_buttons.append((btn, ratio))
        return btn

    def _make_swipe_key(self, ch: str, swipe_char: str | None, base_fs: int) -> SwipeKey:
        """创建 SwipeKey 并注册到缩放列表。"""
        btn = SwipeKey(ch, swipe_char)
        btn.setObjectName("k")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("base_font_size", base_fs)
        self._scaleable_buttons.append((btn, 1.0))
        return btn
