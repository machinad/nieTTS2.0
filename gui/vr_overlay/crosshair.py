"""准星叠加层（双手独立）：显示 VR 射线与覆盖层的交互坐标。

准星以透明 QWidget 实现，覆盖在测试 UI 上方。
通过 WA_TransparentForMouseEvents 属性确保鼠标事件穿透到下层 Widget。
支持双手独立准星：左手蓝色，右手红色。
"""

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget


class VRCrosshairOverlay(QWidget):
    """VR 射线交互准星叠加层（双手独立）。

    左手准星：蓝色十字
    右手准星：红色十字
    透明覆盖在测试 UI 上方，不拦截鼠标事件。

    用法：
        crosshair = VRCrosshairOverlay(parent_widget)
        crosshair.update_position(0, 100.0, 200.0)  # 左手
        crosshair.update_position(1, 500.0, 300.0)  # 右手
    """

    # 准星样式常量
    _CIRCLE_RADIUS = 12
    _CROSS_LENGTH = 18
    _PEN_WIDTH = 2

    # 左手样式（蓝色）
    _COLOR_A_CROSS = QColor(60, 120, 255, 220)
    _COLOR_A_CIRCLE = QColor(60, 120, 255, 180)
    _COLOR_A_TEXT = QColor(200, 220, 255, 200)

    # 右手样式（红色）
    _COLOR_B_CROSS = QColor(255, 60, 60, 220)
    _COLOR_B_CIRCLE = QColor(255, 60, 60, 180)
    _COLOR_B_TEXT = QColor(255, 200, 200, 200)

    # 通用样式
    _COLOR_BG = QColor(0, 0, 0, 120)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        # 两个准星的状态：0=左手, 1=右手
        self._positions = [QPointF(0, 0), QPointF(0, 0)]
        self._visible = [False, False]

        # 关键属性：鼠标事件穿透 + 透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # 不获取焦点
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def update_position(self, hand: int, x: float, y: float):
        """更新指定手的准星位置。

        Args:
            hand: 0=左手, 1=右手
            x: 水平坐标（像素）
            y: 垂直坐标（像素）
        """
        if 0 <= hand <= 1:
            self._positions[hand] = QPointF(x, y)
            self._visible[hand] = True
            self.update()

    def hide_crosshair(self, hand: int | None = None):
        """隐藏准星。

        Args:
            hand: 0=左手, 1=右手, None=隐藏全部
        """
        if hand is None:
            self._visible = [False, False]
        elif 0 <= hand <= 1:
            self._visible[hand] = False
        self.update()

    def hide_all(self):
        """隐藏所有准星。"""
        self._visible = [False, False]
        self.update()

    def paintEvent(self, event):
        """绘制准星。"""
        if not any(self._visible):
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 绘制左手准星（蓝色）
        if self._visible[0]:
            self._draw_crosshair(
                painter,
                0,
                self._positions[0],
                self._COLOR_A_CROSS,
                self._COLOR_A_CIRCLE,
                self._COLOR_A_TEXT,
            )

        # 绘制右手准星（红色）
        if self._visible[1]:
            self._draw_crosshair(
                painter,
                1,
                self._positions[1],
                self._COLOR_B_CROSS,
                self._COLOR_B_CIRCLE,
                self._COLOR_B_TEXT,
            )

        painter.end()

    def _draw_crosshair(
        self,
        painter: QPainter,
        hand: int,
        pos: QPointF,
        color_cross,
        color_circle,
        color_text,
    ):
        """绘制单个准星。"""
        x = pos.x()
        y = pos.y()

        # 绘制圆圈
        painter.setPen(QPen(color_circle, self._PEN_WIDTH))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(pos, self._CIRCLE_RADIUS, self._CIRCLE_RADIUS)

        # 绘制十字线
        painter.setPen(QPen(color_cross, self._PEN_WIDTH))
        painter.drawLine(
            QPointF(x - self._CROSS_LENGTH, y),
            QPointF(x + self._CROSS_LENGTH, y),
        )
        painter.drawLine(
            QPointF(x, y - self._CROSS_LENGTH),
            QPointF(x, y + self._CROSS_LENGTH),
        )

        # 绘制坐标文本背景
        label = "L" if hand == 0 else "R"
        text = f"{label} ({x:.0f}, {y:.0f})"
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
        painter.setPen(color_text)
        painter.drawText(bg_rect, Qt.AlignmentFlag.AlignCenter, text)
