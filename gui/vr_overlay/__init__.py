"""VR 覆盖层模块。

提供 SteamVR (OpenVR) 覆盖层功能，用于在 VR 场景中显示 nieTTS UI。
支持感应式射线交互：控制器靠近覆盖层时自动产生射线。

模块结构：
    manager.py      - OpenVR 生命周期管理 + 60Hz async 主循环
    renderer.py     - FBO 渲染管线（Widget → 纹理）
    input_handler.py - VR 事件 / 射线命中 → Qt 事件转换
    ray_tracker.py  - 感应式射线追踪器（控制器姿态 → 射线求交）
    crosshair.py    - 准星叠加层
    test_widget.py  - 测试 UI

用法：
    import asyncio
    from gui.vr_overlay import VROverlayManager, VROverlayTestWidget

    manager = VROverlayManager()
    widget = VROverlayTestWidget(manager=manager)
    asyncio.create_task(manager.run(widget, config))
    # ... 应用运行 ...
    await manager.stop()
"""

from gui.vr_overlay.crosshair import VRCrosshairOverlay
from gui.vr_overlay.manager import VROverlayManager
from gui.vr_overlay.ray_tracker import VRRayTracker
from gui.vr_overlay.test_widget import VROverlayTestWidget

__all__ = [
    "VROverlayManager",
    "VRCrosshairOverlay",
    "VRRayTracker",
    "VROverlayTestWidget",
]
