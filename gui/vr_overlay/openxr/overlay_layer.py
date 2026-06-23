"""CompositionLayerQuad 构建模块。

将 OpenXR Swapchain 包装为 CompositionLayerQuad 合成层，
支持头显相对、手柄相对、世界固定三种定位模式。
"""

from __future__ import annotations

import logging
from enum import Enum

import xr

logger = logging.getLogger(__name__)


class PositionMode(Enum):
    """覆盖层定位模式。"""
    HEAD = "head"       # 相对头显（VIEW 空间）
    CONTROLLER = "controller"  # 相对手柄（需要每帧更新 pose）
    WORLD = "world"     # 相对世界（LOCAL 空间，固定位置）


def build_quad_layer(
    swapchain: xr.Swapchain,
    space: xr.Space,
    pose: xr.Posef,
    width_meters: float,
    height_meters: float,
    tex_width: int,
    tex_height: int,
    alpha: float = 1.0,
) -> xr.CompositionLayerQuad:
    """构建一个 CompositionLayerQuad。

    Args:
        swapchain: 纹理交换链
        space: 定位参考空间
        pose: 面板在空间中的位置和朝向
        width_meters: 面板物理宽度（米）
        height_meters: 面板物理高度（米）
        tex_width: 纹理像素宽度
        tex_height: 纹理像素高度
        alpha: 透明度

    Returns:
        xr.CompositionLayerQuad 实例
    """
    flags = xr.CompositionLayerFlags.BLEND_TEXTURE_SOURCE_ALPHA_BIT
    if alpha < 1.0:
        flags = flags | xr.CompositionLayerFlags.BLEND_TEXTURE_SOURCE_ALPHA_BIT

    return xr.CompositionLayerQuad(
        layer_flags=flags,
        space=space,
        eye_visibility=xr.EyeVisibility.BOTH,
        sub_image=xr.SwapchainSubImage(
            swapchain=swapchain,
            image_rect=xr.Rect2Di(
                offset=xr.Offset2Di(0, 0),
                extent=xr.Extent2Di(tex_width, tex_height),
            ),
            image_array_index=0,
        ),
        pose=pose,
        size=xr.Extent2Df(width=width_meters, height=height_meters),
    )


def create_head_relative_space(
    session: xr.Session,
    distance: float = 1.5,
    vertical_offset: float = -0.1,
) -> xr.Space:
    """创建头显相对的参考空间（面板始终在视野前方）。

    Args:
        session: OpenXR 会话
        distance: 距离头显的距离（米）
        vertical_offset: 垂直偏移（负值=向下）

    Returns:
        xr.Space 参考空间
    """
    return xr.create_reference_space(session, xr.ReferenceSpaceCreateInfo(
        reference_space_type=xr.ReferenceSpaceType.VIEW,
        pose_in_reference_space=xr.Posef(
            orientation=xr.Quaternionf(x=0.0, y=0.0, z=0.0, w=1.0),
            position=xr.Vector3f(x=0.0, y=vertical_offset, z=-distance),
        ),
    ))


def create_world_relative_space(
    session: xr.Session,
    x: float = 0.0,
    y: float = 1.5,
    z: float = -2.0,
) -> xr.Space:
    """创建世界固定的参考空间。

    Args:
        session: OpenXR 会话
        x, y, z: 面板在世界空间中的位置

    Returns:
        xr.Space 参考空间
    """
    return xr.create_reference_space(session, xr.ReferenceSpaceCreateInfo(
        reference_space_type=xr.ReferenceSpaceType.LOCAL,
        pose_in_reference_space=xr.Posef(
            orientation=xr.Quaternionf(x=0.0, y=0.0, z=0.0, w=1.0),
            position=xr.Vector3f(x=x, y=y, z=z),
        ),
    ))


def get_quad_world_pose(
    space_location: xr.SpaceLocation,
) -> xr.Posef:
    """从 SpaceLocation 提取有效的 Posef。

    如果位置或朝向无效，返回默认值。
    """
    if (space_location.location_flags &
            xr.SpaceLocationFlags.POSITION_VALID and
            space_location.location_flags &
            xr.SpaceLocationFlags.ORIENTATION_VALID):
        return space_location.pose
    return xr.Posef(
        orientation=xr.Quaternionf(x=0.0, y=0.0, z=0.0, w=1.0),
        position=xr.Vector3f(x=0.0, y=1.5, z=-2.0),
    )
