"""VR 事件 → Qt 事件转换。

负责将 OpenVR 的鼠标事件（VREvent_MouseMove / MouseButtonDown / MouseButtonUp）
转换为 PySide6 的 QMouseEvent，并通过 QApplication.postEvent() 分发到 Widget。
"""

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QWidget

if TYPE_CHECKING:
    from gui.vr_overlay.crosshair import VRCrosshairOverlay

logger = logging.getLogger(__name__)

# 延迟导入 openvr 事件常量（避免直接 import openvr 时的循环依赖）
_openvr_consts: dict = {}
_consts_loaded = False


def _load_vr_constants():
    """从 openvr 模块加载事件常量。"""
    global _openvr_consts, _consts_loaded
    if _consts_loaded:
        return
    try:
        import openvr
        _openvr_consts = {
            "MouseMove": openvr.VREvent_MouseMove,
            "MouseButtonDown": openvr.VREvent_MouseButtonDown,
            "MouseButtonUp": openvr.VREvent_MouseButtonUp,
            "FocusEnter": openvr.VREvent_FocusEnter,
            "FocusLeave": openvr.VREvent_FocusLeave,
            "ScrollDiscrete": openvr.VREvent_ScrollDiscrete,
            "OverlayShown": openvr.VREvent_OverlayShown,
            "OverlayHidden": openvr.VREvent_OverlayHidden,
        }
    except ImportError:
        logger.warning("openvr 模块未安装，使用硬编码事件常量")
        _openvr_consts = {
            "MouseMove": 300,
            "MouseButtonDown": 301,
            "MouseButtonUp": 302,
            "FocusEnter": 303,
            "FocusLeave": 304,
            "ScrollDiscrete": 305,
            "OverlayShown": 500,
            "OverlayHidden": 501,
        }
    _consts_loaded = True


class VRInputHandler:
    """将 VR 事件转换为 Qt 事件并分发到目标 Widget。

    处理流程：
        VREvent_MouseMove
            → 坐标转换: (fU, fV) → (x, y)
            → 更新准星位置
            → 生成 QMouseEvent(MouseMove)
            → QApplication.postEvent(widget)
    """

    def __init__(
        self,
        widget: QWidget,
        crosshair: "VRCrosshairOverlay | None" = None,
        manager=None,
        tex_w: int = 1792,
        tex_h: int = 1208,
    ):
        self._widget = widget
        self._crosshair = crosshair
        self._manager = manager
        self._tex_w = tex_w
        self._tex_h = tex_h
        self._last_pos = QPointF(0, 0)
        self._button_pressed = False

    def set_crosshair(self, crosshair: "VRCrosshairOverlay"):
        """设置准星叠加层引用。"""
        self._crosshair = crosshair

    def process_vr_event(self, event) -> bool:
        """处理单个 VR 事件。

        Args:
            event: openvr.VREvent_t 实例

        Returns:
            是否处理了该事件
        """
        _load_vr_constants()
        event_type = event.eventType

        if event_type == _openvr_consts["MouseMove"]:
            self._handle_mouse_move(event.data.mouse)
            return True

        elif event_type == _openvr_consts["MouseButtonDown"]:
            self._handle_mouse_down(event.data.mouse)
            return True

        elif event_type == _openvr_consts["MouseButtonUp"]:
            self._handle_mouse_up(event.data.mouse)
            return True

        elif event_type == _openvr_consts["OverlayShown"]:
            self._handle_overlay_shown()
            return True

        elif event_type == _openvr_consts["OverlayHidden"]:
            self._handle_overlay_hidden()
            return True

        return False

    def _vr_to_widget_pos(self, vr_x: float, vr_y: float) -> QPointF:
        """VR 纹理像素坐标 → Widget 像素坐标。

        OpenVR 覆盖层坐标系（setOverlayInputMethod(Mouse)）：
            (0,0) = 左上角
            (texture_width, texture_height) = 右下角
            坐标单位是像素，不是归一化的 0.0-1.0

        需要从纹理空间缩放到 widget 空间。
        """
        ww = self._widget.width()
        wh = self._widget.height()
        # 纹理坐标 → widget 坐标（等比缩放）
        wx = max(0.0, min(vr_x * ww / self._tex_w, ww - 1))
        wy = max(0.0, min(vr_y * wh / self._tex_h, wh - 1))
        return QPointF(wx, wy)

    def _resolve_target(self, pos: QPointF) -> QWidget:
        """找到点击位置的子 widget。"""
        child = self._widget.childAt(pos.toPoint())
        return child if child is not None else self._widget

    def _create_mouse_event(
        self,
        event_type: QEvent.Type,
        local_pos: QPointF,
        global_pos: QPointF,
        button: Qt.MouseButton = Qt.MouseButton.LeftButton,
    ) -> QMouseEvent:
        """构造 Qt 鼠标事件。"""
        return QMouseEvent(
            event_type,
            local_pos,
            global_pos,
            button,
            button if event_type != QEvent.Type.MouseButtonRelease else Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier,
        )

    def _send_event(self, pos: QPointF, qt_event: QMouseEvent):
        """发送事件到子 widget。"""
        target = self._resolve_target(pos)
        # 将全局坐标转换为目标 widget 的本地坐标
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        local_pos = target.mapFromGlobal(global_pos)
        # 重新构造事件，使用目标 widget 的坐标
        event = QMouseEvent(
            qt_event.type(),
            QPointF(local_pos),
            global_pos,
            qt_event.button(),
            qt_event.buttons(),
            qt_event.modifiers()
        )
        QApplication.sendEvent(target, event)

    def _handle_mouse_move(self, mouse_data):
        """处理 VR 鼠标移动事件。"""
        logger.debug("MouseMove: vr=(%.1f, %.1f)", mouse_data.x, mouse_data.y)
        pos = self._vr_to_widget_pos(mouse_data.x, mouse_data.y)

        # 更新准星位置
        if self._crosshair:
            self._crosshair.update_position(pos.x(), pos.y())

        # 生成并分发 Qt 鼠标移动事件
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        if self._button_pressed:
            qt_event = self._create_mouse_event(
                QEvent.Type.MouseMove, pos, global_pos, Qt.MouseButton.LeftButton
            )
        else:
            qt_event = self._create_mouse_event(
                QEvent.Type.MouseMove, pos, global_pos, Qt.MouseButton.NoButton
            )
        self._send_event(pos, qt_event)
        self._last_pos = pos

        # 每次鼠标移动都标记脏，确保 VR 纹理更新
        if self._manager:
            self._manager.mark_dirty()

    def _handle_mouse_down(self, mouse_data):
        """处理 VR 鼠标按下事件。"""
        pos = self._vr_to_widget_pos(mouse_data.x, mouse_data.y)
        self._button_pressed = True

        global_pos = self._widget.mapToGlobal(pos.toPoint())
        qt_event = self._create_mouse_event(
            QEvent.Type.MouseButtonPress, pos, global_pos, Qt.MouseButton.LeftButton
        )
        self._send_event(pos, qt_event)
        # 点击时标记脏
        if self._manager:
            self._manager.mark_dirty()
        logger.debug("VR 鼠标按下: (%.1f, %.1f)", pos.x(), pos.y())

    def _handle_mouse_up(self, mouse_data):
        """处理 VR 鼠标释放事件。"""
        pos = self._vr_to_widget_pos(mouse_data.x, mouse_data.y)
        self._button_pressed = False

        global_pos = self._widget.mapToGlobal(pos.toPoint())
        qt_event = self._create_mouse_event(
            QEvent.Type.MouseButtonRelease, pos, global_pos, Qt.MouseButton.LeftButton
        )
        self._send_event(pos, qt_event)
        # 释放时标记脏
        if self._manager:
            self._manager.mark_dirty()
        logger.debug("VR 鼠标释放: (%.1f, %.1f)", pos.x(), pos.y())

    def _handle_overlay_shown(self):
        """覆盖层显示事件。"""
        logger.debug("VR 覆盖层已显示")

    def _handle_overlay_hidden(self):
        """覆盖层隐藏事件。"""
        logger.debug("VR 覆盖层已隐藏")
        # 隐藏时重置准星
        if self._crosshair:
            self._crosshair.hide_crosshair()
