"""OpenXR 输入处理：射线命中 → Qt 事件转换。

每帧获取手柄姿态，计算射线与 overlay 面板的交点，
将交点坐标映射到 Qt Widget 并发送鼠标事件。
支持感应式射线：靠近面板自动产生射线，无需按键触发。
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np
import xr
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

from gui.vr_overlay.openxr.ray_interaction import (
    QuadSurface,
    RayHit,
    quaternion_to_forward,
    ray_quad_intersection,
    uv_to_widget_pos,
)

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class OpenXRInputHandler:
    """处理 OpenXR 手柄输入，转换为 Qt 鼠标事件。"""

    def __init__(
        self,
        widget: QWidget,
        tex_width: int,
        tex_height: int,
        overlay_width_meters: float,
        overlay_height_meters: float,
    ) -> None:
        self._widget = widget
        self._tex_width = tex_width
        self._tex_height = tex_height
        self._overlay_width_meters = overlay_width_meters
        self._overlay_height_meters = overlay_height_meters
        self._manager = None

        # 状态
        self._last_hit = RayHit(False, 0.0, 0.0, 0.0)
        self._last_widget_pos = QPointF(0, 0)
        self._trigger_pressed = False
        self._last_trigger_state = False

        # 面板几何（每帧更新）
        self._quad_surface: QuadSurface | None = None

    def set_manager(self, manager) -> None:
        """设置管理器引用（用于 mark_dirty）。"""
        self._manager = manager

    def update_quad_surface(self, pose: xr.Posef) -> None:
        """根据当前面板 pose 更新 QuadSurface 几何。"""
        pos = (pose.position.x, pose.position.y, pose.position.z)
        rot = (pose.orientation.x, pose.orientation.y,
               pose.orientation.z, pose.orientation.w)
        self._quad_surface = QuadSurface.from_pose_and_size(
            pos, rot,
            self._overlay_width_meters,
            self._overlay_height_meters,
        )

    def process_input(
        self,
        controller_position: tuple[float, float, float],
        controller_orientation: tuple[float, float, float, float],
        trigger_state: bool,
    ) -> RayHit:
        """处理一帧的控制器输入。

        Args:
            controller_position: 控制器位置 (x, y, z)
            controller_orientation: 控制器朝向四元数 (x, y, z, w)
            trigger_state: 触发器是否按下

        Returns:
            RayHit: 射线命中结果
        """
        if self._quad_surface is None:
            return RayHit(False, 0.0, 0.0, 0.0)

        # 计算射线
        ray_origin = np.array(controller_position, dtype=np.float64)
        ray_direction = quaternion_to_forward(controller_orientation)

        # 射线-面板相交测试
        hit = ray_quad_intersection(ray_origin, ray_direction, self._quad_surface)
        self._last_hit = hit

        if hit.hit:
            # 转换到 Widget 坐标
            widget_pos = uv_to_widget_pos(
                hit.u, hit.v,
                self._widget.width(), self._widget.height(),
            )
            self._last_widget_pos = widget_pos

            # 发送鼠标移动事件
            self._send_mouse_move(widget_pos)

            # 处理触发器状态变化
            self._process_trigger(trigger_state, widget_pos)

            # 标记脏（准星更新 + 纹理重渲染）
            if self._manager is not None:
                self._manager.mark_dirty()
        else:
            # 射线离开面板
            if self._trigger_pressed:
                # 如果触发器仍按下但射线离开，发送释放事件
                self._send_mouse_release(self._last_widget_pos)
                self._trigger_pressed = False
            self._last_trigger_state = trigger_state

        return hit

    def _process_trigger(self, trigger_state: bool, pos: QPointF) -> None:
        """处理触发器按下/释放事件。"""
        if trigger_state and not self._last_trigger_state:
            # 按下
            self._send_mouse_press(pos)
            self._trigger_pressed = True
        elif not trigger_state and self._last_trigger_state:
            # 释放
            self._send_mouse_release(pos)
            self._trigger_pressed = False

        self._last_trigger_state = trigger_state

    def _send_mouse_move(self, pos: QPointF) -> None:
        """发送鼠标移动事件。"""
        target = self._resolve_target(pos)
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        local_pos = target.mapFromGlobal(global_pos)
        event = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            QPointF(local_pos),
            QPointF(global_pos),
            Qt.MouseButton.NoButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier,
        )
        QApplication.sendEvent(target, event)

    def _send_mouse_press(self, pos: QPointF) -> None:
        """发送鼠标按下事件。"""
        target = self._resolve_target(pos)
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        local_pos = target.mapFromGlobal(global_pos)
        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(local_pos),
            QPointF(global_pos),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        QApplication.sendEvent(target, event)
        logger.debug("射线点击: widget=(%.1f, %.1f)", pos.x(), pos.y())

    def _send_mouse_release(self, pos: QPointF) -> None:
        """发送鼠标释放事件。"""
        target = self._resolve_target(pos)
        global_pos = self._widget.mapToGlobal(pos.toPoint())
        local_pos = target.mapFromGlobal(global_pos)
        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPointF(local_pos),
            QPointF(global_pos),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier,
        )
        QApplication.sendEvent(target, event)

    def _resolve_target(self, pos: QPointF) -> QWidget:
        """查找 pos 位置的子 widget，如果没有则返回主 widget。"""
        child = self._widget.childAt(pos.toPoint())
        return child if child is not None else self._widget

    @property
    def last_hit(self) -> RayHit:
        """最近一次射线命中结果。"""
        return self._last_hit

    @property
    def last_widget_pos(self) -> QPointF:
        """最近一次命中在 Widget 上的坐标。"""
        return self._last_widget_pos

    @property
    def is_ray_active(self) -> bool:
        """射线是否正在命中面板。"""
        return self._last_hit.hit
