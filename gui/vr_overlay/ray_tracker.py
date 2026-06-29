"""感应式射线追踪器（双手独立）。

每帧获取控制器姿态，计算射线与覆盖层的交点。
支持双手独立追踪，各自显示准星，触发器切换鼠标控制权。
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# 延迟导入 openvr
_openvr = None


def _ensure_openvr():
    global _openvr
    if _openvr is None:
        import openvr as ov

        _openvr = ov
    return _openvr


@dataclass
class ControllerHit:
    """单个控制器的射线命中结果。"""

    controller_index: int
    widget_pos: QPointF
    u: float
    v: float
    distance: float
    origin: tuple[float, float, float] = (0, 0, 0)
    direction: tuple[float, float, float] = (0, 0, 0)
    hit_world_pos: tuple[float, float, float] = (0, 0, 0)


@dataclass
class ControllerState:
    """单个控制器的追踪状态。"""

    index: int
    is_hitting: bool = False
    hit: ControllerHit | None = None
    trigger_pressed: bool = False
    was_trigger_pressed: bool = False


class VRRayTracker:
    """感应式射线追踪器（双手独立）。

    每帧：
    1. getDeviceToAbsoluteTrackingPose() → 控制器 3x4 矩阵
    2. 从矩阵提取位置 + 前方向量
    3. computeOverlayIntersection() → UV + 距离
    4. 双手独立追踪，各自返回命中结果
    5. 触发器按下时，该手柄获得鼠标事件控制权
    """

    def __init__(
        self,
        overlay,
        overlay_handle,
        input_handler,
        tex_width: int = 1792,
        tex_height: int = 1208,
    ) -> None:
        self._overlay = overlay
        self._overlay_handle = overlay_handle
        self._input_handler = input_handler
        self._tex_width = tex_width
        self._tex_height = tex_height

        self._vr_system = None
        self._controller_indices: list[int] = []
        self._controller_states: dict[int, ControllerState] = {}

    def init(self) -> None:
        """初始化（在 OpenVR 初始化后调用）。"""
        ov = _ensure_openvr()
        self._vr_system = ov.VRSystem()
        logger.info("射线追踪器: overlay_handle=%s", self._overlay_handle)
        self._find_controllers()
        logger.info("射线追踪器初始化完成, 控制器: %s", self._controller_indices)

    def _find_controllers(self) -> None:
        """查找已连接的控制器设备索引。"""
        ov = _ensure_openvr()
        self._controller_indices = []
        for i in range(1, 16):  # 设备 0 是 HMD，1-15 是其他设备
            try:
                device_class = self._vr_system.getTrackedDeviceClass(i)
                if device_class == ov.TrackedDeviceClass_Controller:
                    self._controller_indices.append(i)
                    if i not in self._controller_states:
                        self._controller_states[i] = ControllerState(index=i)
                    logger.debug("发现控制器: index=%d", i)
            except Exception:
                pass

    def update(self) -> None:
        """每帧调用，追踪所有控制器射线与覆盖层的交点。"""
        if self._vr_system is None or self._overlay is None:
            return

        # 定期重新扫描控制器（热插拔支持）
        if not self._controller_indices:
            self._find_controllers()
            if not self._controller_indices:
                return

        ov = _ensure_openvr()

        try:
            # 获取所有设备姿态（显式分配数组）
            pose_array = (ov.TrackedDevicePose_t * ov.k_unMaxTrackedDeviceCount)()
            self._vr_system.getDeviceToAbsoluteTrackingPose(
                ov.TrackingUniverseStanding,
                0.0,
                pose_array,
            )
            poses = pose_array

            # 收集所有命中的控制器
            all_hits: list[ControllerHit] = []

            for idx in self._controller_indices:
                state = self._controller_states.get(idx)
                if state is None:
                    state = ControllerState(index=idx)
                    self._controller_states[idx] = state

                pose = poses[idx]

                if not pose.bPoseIsValid:
                    state.is_hitting = False
                    state.hit = None
                    continue

                # 从 3x4 矩阵提取射线（用 pitched 方向，和激光束一致）
                m = pose.mDeviceToAbsoluteTracking
                origin = _extract_position(m)
                direction = _extract_pitched_forward(m)

                # computeOverlayIntersection
                params = ov.VROverlayIntersectionParams_t()
                params.vSource = ov.HmdVector3_t(*origin)
                params.vDirection = ov.HmdVector3_t(*direction)
                params.eOrigin = ov.TrackingUniverseStanding

                results = ov.VROverlayIntersectionResults_t()
                hit, results = self._overlay.computeOverlayIntersection(
                    self._overlay_handle,
                    params,
                )

                if hit:
                    uv = results.vUVs
                    widget_pos = self._uv_to_widget_pos(uv.v[0], uv.v[1])
                    # 计算交点世界坐标
                    hit_world_pos = (
                        origin[0] + direction[0] * results.fDistance,
                        origin[1] + direction[1] * results.fDistance,
                        origin[2] + direction[2] * results.fDistance,
                    )
                    controller_hit = ControllerHit(
                        controller_index=idx,
                        widget_pos=widget_pos,
                        u=uv.v[0],
                        v=uv.v[1],
                        distance=results.fDistance,
                        origin=origin,
                        direction=direction,
                        hit_world_pos=hit_world_pos,
                    )
                    state.is_hitting = True
                    state.hit = controller_hit
                    all_hits.append(controller_hit)

                    logger.debug(
                        "控制器 %d: 命中 UV=(%.3f, %.3f) dist=%.2f",
                        idx,
                        uv.v[0],
                        uv.v[1],
                        results.fDistance,
                    )
                else:
                    state.is_hitting = False
                    state.hit = None

                # 检查触发器状态
                self._check_trigger(idx, state)

            # 通知 input_handler 更新所有控制器状态
            self._input_handler.update_controller_hits(all_hits)

        except Exception as e:
            logger.debug("射线追踪异常: %s", e)

    def _check_trigger(self, controller_index: int, state: ControllerState) -> None:
        """检查控制器触发器状态，处理按下/释放事件。"""
        try:
            result, controller_state = self._vr_system.getControllerState(controller_index)
            if not result:
                return

            # 触发器是 axis1（通常）
            trigger_value = controller_state.rAxis[1].x  # 0.0 ~ 1.0
            trigger_pressed = trigger_value > 0.5

            state.was_trigger_pressed = state.trigger_pressed
            state.trigger_pressed = trigger_pressed

            if trigger_pressed and not state.was_trigger_pressed:
                # 触发器按下 → 该手柄获得鼠标控制权
                if state.is_hitting and state.hit:
                    self._input_handler.process_trigger_press(
                        controller_index,
                        state.hit.widget_pos,
                    )
                    logger.debug("触发器按下: controller=%d", controller_index)
            elif not trigger_pressed and state.was_trigger_pressed:
                # 触发器释放
                self._input_handler.process_trigger_release(controller_index)
                logger.debug("触发器释放: controller=%d", controller_index)

        except Exception:
            pass

    def _uv_to_widget_pos(self, u: float, v: float) -> QPointF:
        """将归一化 UV 坐标转换为 Widget 像素坐标。"""
        if self._input_handler is None:
            return QPointF(0, 0)

        widget = self._input_handler._widget
        ww = widget.width()
        wh = widget.height()

        x = max(0.0, min(u * ww, ww - 1))
        y = max(0.0, min(v * wh, wh - 1))
        return QPointF(x, y)


def _extract_position(m) -> tuple[float, float, float]:
    """从 HmdMatrix34_t 提取位置（平移分量）。"""
    return (m.m[0][3], m.m[1][3], m.m[2][3])


def _extract_forward(m) -> tuple[float, float, float]:
    """从 HmdMatrix34_t 提取前方向量（-Z 方向）。"""
    return (-m.m[0][2], -m.m[1][2], -m.m[2][2])


def _extract_pitched_forward(m, pitch_deg: float = -38) -> tuple[float, float, float]:
    """从设备矩阵提取 pitched 前方向（世界空间）。

    在控制器局部空间中应用 pitch 旋转，然后转换到世界空间。
    这样方向在控制器扭转时保持一致（局部空间旋转不影响世界空间方向）。

    Args:
        m: HmdMatrix34_t 设备矩阵
        pitch_deg: 俯仰偏移角度（度），默认 -38°
    """
    # 控制器局部空间中的 pitched 前方向
    # 原始前方向 = (0, 0, -1)
    # 绕 X 轴旋转 pitch_deg 后 = (0, sin(pitch_deg), -cos(pitch_deg))
    pitch_rad = math.radians(pitch_deg)
    local_x = 0.0
    local_y = math.sin(pitch_rad)
    local_z = -math.cos(pitch_rad)

    # 转换到世界空间：world = R × local
    return (
        m.m[0][0] * local_x + m.m[0][1] * local_y + m.m[0][2] * local_z,
        m.m[1][0] * local_x + m.m[1][1] * local_y + m.m[1][2] * local_z,
        m.m[2][0] * local_x + m.m[2][1] * local_y + m.m[2][2] * local_z,
    )
