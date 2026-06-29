"""射线-UI 相交计算模块。

从 OpenXR 手柄 aim pose 提取射线，计算与 overlay 面板的交点，
将交点 UV 坐标映射到 Qt Widget 像素坐标。
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
from PySide6.QtCore import QPointF


class RayHit(NamedTuple):
    """射线命中结果。"""

    hit: bool
    distance: float  # 射线参数 t（交点到射线原点的距离，米）
    u: float  # 水平归一化坐标 [0, 1]，0=左, 1=右
    v: float  # 垂直归一化坐标 [0, 1]，0=上, 1=下


class QuadSurface:
    """定义一个 3D 四边形面板的几何参数。

    面板中心在 center，宽度沿 right 方向，高度沿 up 方向。
    """

    def __init__(
        self,
        center: np.ndarray,
        normal: np.ndarray,
        right: np.ndarray,
        up: np.ndarray,
        width: float,
        height: float,
    ) -> None:
        self.center = center
        self.normal = normal / np.linalg.norm(normal)
        self.right = right / np.linalg.norm(right)
        self.up = up / np.linalg.norm(up)
        self.width = width
        self.height = height

    @classmethod
    def from_pose_and_size(
        cls,
        pose_position: tuple[float, float, float],
        pose_orientation: tuple[float, float, float, float],
        width: float,
        height: float,
    ) -> QuadSurface:
        """从 OpenXR Posef 和尺寸构造面板。

        Args:
            pose_position: 面板中心位置 (x, y, z)
            pose_orientation: 面板朝向四元数 (x, y, z, w)
            width: 面板宽度（米）
            height: 面板高度（米）
        """
        center = np.array(pose_position, dtype=np.float64)
        right, up, normal = _basis_from_quaternion(pose_orientation)
        return cls(center, normal, right, up, width, height)


def _basis_from_quaternion(
    q: tuple[float, float, float, float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """从四元数 (x, y, z, w) 提取局部坐标轴。

    返回 (right, up, forward)，其中 forward 是面板法线方向（-Z）。
    """
    x, y, z, w = q
    # 旋转矩阵的列
    right = np.array(
        [
            1 - 2 * (y * y + z * z),
            2 * (x * y + w * z),
            2 * (x * z - w * y),
        ]
    )
    up = np.array(
        [
            2 * (x * y - w * z),
            1 - 2 * (x * x + z * z),
            2 * (y * z + w * x),
        ]
    )
    forward = np.array(
        [
            2 * (x * z + w * y),
            2 * (y * z - w * x),
            1 - 2 * (x * x + y * y),
        ]
    )
    return right, up, -forward  # OpenXR: -Z 是前方


def quaternion_to_forward(q: tuple[float, float, float, float]) -> np.ndarray:
    """从四元数 (x, y, z, w) 提取前方向量（OpenXR: -Z 是前方）。"""
    x, y, z, w = q
    fx = -(2 * (x * z - w * y))
    fy = -(2 * (y * z + w * x))
    fz = -(1 - 2 * (x * x + y * y))
    return np.array([fx, fy, fz], dtype=np.float64)


def ray_quad_intersection(
    ray_origin: np.ndarray,
    ray_direction: np.ndarray,
    quad: QuadSurface,
) -> RayHit:
    """计算射线与四边形面板的交点。

    Args:
        ray_origin: 射线起点 (3,)
        ray_direction: 射线方向 (3,)，不需要归一化
        quad: 目标面板

    Returns:
        RayHit: 命中结果，包含 hit/distance/u/v
    """
    # 归一化射线方向
    dir_len = np.linalg.norm(ray_direction)
    if dir_len < 1e-10:
        return RayHit(False, 0.0, 0.0, 0.0)
    ray_dir = ray_direction / dir_len

    # 射线-平面相交
    denom = np.dot(ray_dir, quad.normal)
    if abs(denom) < 1e-6:
        return RayHit(False, 0.0, 0.0, 0.0)

    t = np.dot(quad.center - ray_origin, quad.normal) / denom
    if t < 0.01:  # 最近 1cm，避免手柄内部误触
        return RayHit(False, 0.0, 0.0, 0.0)

    # 交点
    hit_point = ray_origin + t * ray_dir
    local = hit_point - quad.center

    # 投影到面板局部坐标
    half_w = quad.width / 2.0
    half_h = quad.height / 2.0

    u_local = np.dot(local, quad.right)
    v_local = np.dot(local, quad.up)

    if abs(u_local) > half_w or abs(v_local) > half_h:
        return RayHit(False, 0.0, 0.0, 0.0)

    # 归一化到 [0, 1]
    u = (u_local / half_w + 1.0) / 2.0
    v = (1.0 - v_local / half_h) / 2.0  # Y 轴翻转：0=上, 1=下

    return RayHit(True, float(t), float(u), float(v))


def uv_to_widget_pos(
    u: float,
    v: float,
    widget_width: int,
    widget_height: int,
) -> QPointF:
    """将归一化 UV 坐标转换为 Qt Widget 像素坐标。

    Args:
        u: 水平归一化坐标 [0, 1]，0=左, 1=右
        v: 垂直归一化坐标 [0, 1]，0=上, 1=下
        widget_width: Widget 宽度（像素）
        widget_height: Widget 高度（像素）

    Returns:
        QPointF: Widget 坐标
    """
    x = u * widget_width
    y = v * widget_height
    return QPointF(
        max(0.0, min(x, widget_width - 1.0)),
        max(0.0, min(y, widget_height - 1.0)),
    )


def compute_ray_length(hit: RayHit, max_length: float = 5.0) -> float:
    """计算射线显示长度（命中时为交点距离，否则为最大长度）。"""
    return hit.distance if hit.hit else max_length
