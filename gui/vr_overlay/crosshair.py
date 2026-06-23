"""准星叠加层：显示 VR 射线与覆盖层的交互坐标。

准星以透明 QWidget 实现，覆盖在测试 UI 上方。
通过 WA_TransparentForMouseEvents 属性确保鼠标事件穿透到下层 Widget。
"""

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QWidget


class VRCrosshairOverlay(QWidget):
    """VR 射线交互准星叠加层。

    显示一个红色十字准星和当前坐标值。
    透明覆盖在测试 UI 上方，不拦截鼠标事件。

    用法：
        crosshair = VRCrosshairOverlay(parent_widget)
        crosshair.update_position(100.0, 200.0)  # 更新位置
    """

    # 准星样式常量
    _CIRCLE_RADIUS = 12
    _CROSS_LENGTH = 18
    _PEN_WIDTH = 2
    _COLOR_CROSS = QColor(255, 60, 60, 220)      # 红色准星
    _COLOR_CIRCLE = QColor(255, 60, 60, 180)      # 圆圈
    _COLOR_TEXT = QColor(255, 255, 255, 200)       # 白色文字
    _COLOR_BG = QColor(0, 0, 0, 120)              # 文字背景

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._pos = QPointF(0, 0)
        self._visible = False

        # 关键属性：鼠标事件穿透 + 透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # 不获取焦点
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def update_position(self, x: float, y: float):
        """更新准星位置（Widget 像素坐标）。

        Args:
            x: 水平坐标（像素）
            y: 垂直坐标（像素）
        """
        self._pos = QPointF(x, y)
        self._visible = True
        self.update()

    def hide_crosshair(self):
        """隐藏准星。"""
        self._visible = False
        self.update()

    def paintEvent(self, event):
        """绘制准星。"""
        if not self._visible:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        x = self._pos.x()
        y = self._pos.y()

        # 绘制圆圈
        painter.setPen(QPen(self._COLOR_CIRCLE, self._PEN_WIDTH))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(self._pos, self._CIRCLE_RADIUS, self._CIRCLE_RADIUS)

        # 绘制十字线
        painter.setPen(QPen(self._COLOR_CROSS, self._PEN_WIDTH))
        # 水平线
        painter.drawLine(
            QPointF(x - self._CROSS_LENGTH, y),
            QPointF(x + self._CROSS_LENGTH, y),
        )
        # 垂直线
        painter.drawLine(
            QPointF(x, y - self._CROSS_LENGTH),
            QPointF(x, y + self._CROSS_LENGTH),
        )

        # 绘制坐标文本背景
        text = f"({x:.0f}, {y:.0f})"
        font = QFont("Consolas", 10)
        painter.setFont(font)
        text_rect = painter.boundingRect(0, 0, 200, 30, Qt.AlignmentFlag.AlignLeft, text)

        text_x = int(x) + 22
        text_y = int(y) - 12

        # 确保文本不超出边界
        if text_x + text_rect.width() > self.width():
            text_x = int(x) - 22 - text_rect.width()
        if text_y < 0:
            text_y = int(y) + 22

        bg_rect = text_rect.adjusted(-4, -2, 4, 2)
        bg_rect.moveTopLeft(QPointF(text_x, text_y).toPoint())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._COLOR_BG)
        painter.drawRoundedRect(bg_rect, 4, 4)

        # 绘制坐标文本
        painter.setPen(self._COLOR_TEXT)
        painter.drawText(bg_rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.end()
