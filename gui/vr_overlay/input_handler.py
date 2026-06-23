"""VR 事件 → Qt 事件转换（双手独立）。

负责将 OpenVR 的鼠标事件（VREvent_MouseMove / MouseButtonDown / MouseButtonUp）
转换为 PySide6 的 QMouseEvent，并通过 QApplication.sendEvent() 分发到 Widget。

支持双手独立射线追踪：两个手柄各自显示准星，触发器切换鼠标控制权。
"""

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QWidget

if TYPE_CHECKING:
    from gui.vr_overlay.crosshair import VRCrosshairOverlay
    from gui.vr_overlay.ray_tracker import ControllerHit

logger = logging.getLogger(__name__)

# 延迟导入 openvr 事件常量
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
    """将 VR 事件转换为 Qt 事件并分发到目标 Widget（双手独立）。

    双手各自独立：
    - 左手准星（蓝色）、右手准星（红色）同时显示
    - 触发器按下时，该手柄获得鼠标事件控制权
    - Qt 鼠标事件同一时刻只能来自一个手柄
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

        # 双手状态
        self._last_pos_a = QPointF(0, 0)  # 左手最后位置
        self._last_pos_b = QPointF(0, 0)  # 右手最后位置
        self._active_hand: int | None = None  # 当前拥有鼠标控制权的手（0=左, 1=右）
        self._button_pressed = False

        # 控制器索引 → 手的映射（第一个控制器=左手，第二个=右手）
        self._controller_hand_map: dict[int, int] = {}

    def set_crosshair(self, crosshair: "VRCrosshairOverlay"):
        """设置准星叠加层引用。"""
        self._crosshair = crosshair

    def _get_hand(self, controller_index: int) -> int:
        """获取控制器对应的手（0=左, 1=右）。"""
        if controller_index not in self._controller_hand_map:
            # 分配：第一个未分配的控制器=0，第二个=1
            used = set(self._controller_hand_map.values())
            if 0 not in used:
                self._controller_hand_map[controller_index] = 0
            elif 1 not in used:
                self._controller_hand_map[controller_index] = 1
            else:
                # 都已分配，覆盖最旧的
                self._controller_hand_map[controller_index] = 0
        return self._controller_hand_map[controller_index]

    def update_controller_hits(self, hits: list["ControllerHit"]) -> None:
        """更新所有控制器的命中状态（由 VRRayTracker 每帧调用）。

        Args:
            hits: 所有命中的控制器列表
        """
        # 先隐藏所有准星
        if self._crosshair:
            self._crosshair.hide_all()

        # 更新每个命中的控制器的准星
        for hit in hits:
            hand = self._get_hand(hit.controller_index)

            # 更新准星位置
            if self._crosshair:
                self._crosshair.update_position(
                    hand, hit.widget_pos.x(), hit.widget_pos.y(),
                )

            # 更新最后位置
            if hand == 0:
                self._last_pos_a = hit.widget_pos
            else:
                self._last_pos_b = hit.widget_pos

            # 如果当前没有激活的手，或激活的手就是这个手，发送鼠标移动
            if self._active_hand is None or self._active_hand == hand:
                self._send_mouse_move(hit.widget_pos, hand)

        # 标记脏（准星位置变化）
        if hits and self._manager:
            self._manager.mark_dirty()

    def process_trigger_press(self, controller_index: int, widget_pos: QPointF) -> None:
        """处理触发器按下（由 VRRayTracker 调用）。

        触发器按下时，该手柄获得鼠标事件控制权。
        """
        hand = self._get_hand(controller_index)
        self._active_hand = hand
        self._button_pressed = True

        global_pos = self._widget.mapToGlobal(widget_pos.toPoint())
        qt_event = self._create_mouse_event(
            QEvent.Type.MouseButtonPress, widget_pos, global_pos, Qt.MouseButton.LeftButton,
        )
        self._send_event(widget_pos, qt_event)

        if self._manager:
            self._manager.mark_dirty()
        logger.debug("触发器按下: hand=%d pos=(%.1f, %.1f)", hand, widget_pos.x(), widget_pos.y())

    def process_trigger_release(self, controller_index: int) -> None:
        """处理触发器释放（由 VRRayTracker 调用）。"""
        hand = self._get_hand(controller_index)

        # 只有当前激活的手才能释放
        if self._active_hand != hand:
            return

        self._button_pressed = False
        pos = self._last_pos_a if hand == 0 else self._last_pos_b

        global_pos = self._widget.mapToGlobal(pos.toPoint())
        qt_event = self._create_mouse_event(
            QEvent.Type.MouseButtonRelease, pos, global_pos, Qt.MouseButton.LeftButton,
        )
        self._send_event(pos, qt_event)

        # 释放后清除激活状态
        self._active_hand = None

        if self._manager:
            self._manager.mark_dirty()
        logger.debug("触发器释放: hand=%d pos=(%.1f, %.1f)", hand, pos.x(), pos.y())

    def _send_mouse_move(self, pos: QPointF, hand: int) -> None:
        """发送鼠标移动事件。"""
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        if self._button_pressed and self._active_hand == hand:
            qt_event = self._create_mouse_event(
                QEvent.Type.MouseMove, pos, global_pos, Qt.MouseButton.LeftButton,
            )
        else:
            qt_event = self._create_mouse_event(
                QEvent.Type.MouseMove, pos, global_pos, Qt.MouseButton.NoButton,
            )
        self._send_event(pos, qt_event)

    # ── OpenVR 事件处理（保留兼容）──

    def process_vr_event(self, event) -> bool:
        """处理单个 VR 事件（SteamVR 内置事件）。"""
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
            return True
        elif event_type == _openvr_consts["OverlayHidden"]:
            if self._crosshair:
                self._crosshair.hide_all()
            return True
        return False

    def _vr_to_widget_pos(self, vr_x: float, vr_y: float) -> QPointF:
        """VR 纹理像素坐标 → Widget 像素坐标。"""
        ww = self._widget.width()
        wh = self._widget.height()
        wx = max(0.0, min(vr_x * ww / self._tex_w, ww - 1))
        wy = max(0.0, min(vr_y * wh / self._tex_h, wh - 1))
        return QPointF(wx, wy)

    def _handle_mouse_move(self, mouse_data):
        """处理 VR 鼠标移动事件（SteamVR 内置）。"""
        pos = self._vr_to_widget_pos(mouse_data.x, mouse_data.y)
        if self._crosshair:
            self._crosshair.update_position(0, pos.x(), pos.y())
        self._send_mouse_move(pos, 0)
        self._last_pos_a = pos
        if self._manager:
            self._manager.mark_dirty()

    def _handle_mouse_down(self, mouse_data):
        """处理 VR 鼠标按下事件（SteamVR 内置）。"""
        pos = self._vr_to_widget_pos(mouse_data.x, mouse_data.y)
        self._active_hand = 0
        self._button_pressed = True
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        qt_event = self._create_mouse_event(
            QEvent.Type.MouseButtonPress, pos, global_pos, Qt.MouseButton.LeftButton,
        )
        self._send_event(pos, qt_event)
        if self._manager:
            self._manager.mark_dirty()

    def _handle_mouse_up(self, mouse_data):
        """处理 VR 鼠标释放事件（SteamVR 内置）。"""
        pos = self._vr_to_widget_pos(mouse_data.x, mouse_data.y)
        self._button_pressed = False
        self._active_hand = None
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        qt_event = self._create_mouse_event(
            QEvent.Type.MouseButtonRelease, pos, global_pos, Qt.MouseButton.LeftButton,
        )
        self._send_event(pos, qt_event)
        if self._manager:
            self._manager.mark_dirty()

    # ── 工具方法 ──

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
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        local_pos = target.mapFromGlobal(global_pos)
        event = QMouseEvent(
            qt_event.type(),
            QPointF(local_pos),
            global_pos,
            qt_event.button(),
            qt_event.buttons(),
            qt_event.modifiers(),
        )
        QApplication.sendEvent(target, event)
