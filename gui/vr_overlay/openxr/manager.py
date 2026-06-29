"""OpenXR 覆盖层生命周期管理器。

负责 OpenXR 实例/会话/交换链的创建和销毁，
90Hz async 主循环，事件轮询，射线交互，纹理提交。

三阶段初始化：
  阶段 1（子线程）：xr.create_instance → xr.get_system
  阶段 2（主线程）：创建 GL 上下文 → GraphicsBinding → xr.create_session
  阶段 3（子线程）：创建 Swapchain / ActionSet / 参考空间
"""

from __future__ import annotations

import asyncio
import ctypes
import logging
import time
from typing import TYPE_CHECKING

import xr

from gui.vr_overlay.openxr.input_handler import OpenXRInputHandler
from gui.vr_overlay.openxr.overlay_layer import (
    PositionMode,
    build_quad_layer,
    create_head_relative_space,
)
from gui.vr_overlay.openxr.renderer import OverlayRenderer

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class OpenXROverlayManager:
    """OpenXR 覆盖层管理器。"""

    def __init__(self) -> None:
        # OpenXR 核心对象
        self._instance: xr.Instance | None = None
        self._system_id: xr.SystemId | None = None
        self._session: xr.Session | None = None
        self._session_running = False

        # 交换链
        self._swapchain: xr.Swapchain | None = None
        self._swapchain_images: list = []

        # 参考空间
        self._overlay_space: xr.Space | None = None

        # 输入动作
        self._action_set: xr.ActionSet | None = None
        self._aim_action: xr.Action | None = None
        self._trigger_action: xr.Action | None = None
        self._aim_space: xr.Space | None = None
        self._right_hand_path: int = 0

        # Qt/渲染组件
        self._renderer: OverlayRenderer | None = None
        self._input_handler: OpenXRInputHandler | None = None
        self._context_provider = None  # pyopenxr GL 上下文提供者

        # 配置
        self._config: dict = {}
        self._tex_width = 1792
        self._tex_height = 1208
        self._width_meters = 2.0
        self._height_meters = 1.5
        self._distance_meters = 1.5
        self._vertical_offset = -0.1
        self._alpha = 0.9
        self._position_mode = PositionMode.HEAD

        # 状态
        self._running = False
        self._dirty = True
        self._widget: QWidget | None = None

        # 会话状态
        self._session_state = xr.SessionState.UNKNOWN
        self._frame_state: xr.FrameState | None = None
        self._overlay_mode = False  # 是否以覆盖层模式运行
        self._overlay_visible = True  # 覆盖层是否可见

    def mark_dirty(self) -> None:
        """标记需要重新渲染纹理。"""
        self._dirty = True

    async def run(self, widget: QWidget, config: dict) -> None:
        """启动覆盖层主循环。"""
        self._widget = widget
        self._config = config
        self._running = True

        # 读取配置
        vr_cfg = config.get("vr_overlay", {})
        self._tex_width = vr_cfg.get("texture_width", 1792)
        self._tex_height = vr_cfg.get("texture_height", 1208)
        self._width_meters = vr_cfg.get("width_meters", 2.0)
        self._distance_meters = vr_cfg.get("distance_meters", 1.5)
        self._vertical_offset = vr_cfg.get("vertical_offset", -0.1)
        self._alpha = vr_cfg.get("alpha", 0.9)

        # 计算面板高度（保持宽高比）
        aspect = self._tex_height / self._tex_width
        self._height_meters = self._width_meters * aspect

        # 定位模式
        mode_str = vr_cfg.get("position_mode", "head")
        try:
            self._position_mode = PositionMode(mode_str)
        except ValueError:
            self._position_mode = PositionMode.HEAD

        logger.info(
            "OpenXR 覆盖层配置: %dx%d, %.1fm x %.1fm, 距离=%.1fm",
            self._tex_width,
            self._tex_height,
            self._width_meters,
            self._height_meters,
            self._distance_meters,
        )

        try:
            # ── 阶段 1：子线程 — 创建实例和系统 ──
            ok = await asyncio.to_thread(self._init_xr_instance)
            if not ok:
                logger.error("OpenXR 实例创建失败")
                return

            # ── 阶段 2：主线程 — 创建 GL 上下文 + Session ──
            ok = self._init_gl_and_session(widget)
            if not ok:
                logger.error("OpenXR GL/Session 创建失败")
                return

            # ── 阶段 3：子线程 — 创建交换链、动作等资源 ──
            ok = await asyncio.to_thread(self._init_xr_resources)
            if not ok:
                logger.error("OpenXR 资源创建失败")
                return

            # ── 主循环 90Hz ──
            frame_interval = 1.0 / 90.0
            while self._running:
                loop_start = time.monotonic()

                self._poll_events()

                if self._session_state == xr.SessionState.FOCUSED:
                    self._process_frame()

                elapsed = time.monotonic() - loop_start
                sleep_time = max(0, frame_interval - elapsed)
                await asyncio.sleep(sleep_time)

        except asyncio.CancelledError:
            logger.info("OpenXR 主循环被取消")
        except Exception as e:
            logger.error("OpenXR 主循环异常: %s", e, exc_info=True)
        finally:
            await self._cleanup()

    # ── 阶段 1：子线程 — 实例和系统 ──

    def _init_xr_instance(self) -> bool:
        """创建 OpenXR 实例和获取系统（子线程安全）。"""
        try:
            try:
                xr.expose_packaged_api_layers()
            except Exception:
                pass

            # 优先尝试覆盖层扩展，失败则回退到标准模式
            extensions = ["XR_KHR_opengl_enable"]
            try:
                # 检查 XR_EXTX_overlay 是否可用
                available = xr.enumerate_instance_extension_properties()
                available_names = {e.extension_name for e in available}
                if "XR_EXTX_overlay" in available_names:
                    extensions.append("XR_EXTX_overlay")
                    logger.info("XR_EXTX_overlay 扩展可用")
                else:
                    logger.warning("XR_EXTX_overlay 扩展不可用，将以标准模式运行")
            except Exception:
                logger.warning("无法查询扩展列表，尝试启用 XR_EXTX_overlay")

            if "XR_EXTX_overlay" not in extensions:
                # 上面的检查可能跳过了，仍然尝试添加
                extensions.append("XR_EXTX_overlay")

            self._instance = xr.create_instance(
                xr.InstanceCreateInfo(
                    application_info=xr.ApplicationInfo(
                        application_name="nieTTS VR Overlay",
                        application_version=1,
                        engine_name="nieTTS",
                        engine_version=1,
                    ),
                    enabled_extension_names=extensions,
                )
            )
            logger.info("OpenXR 实例创建成功, 扩展: %s", extensions)

            self._system_id = xr.get_system(
                self._instance,
                xr.SystemGetInfo(
                    form_factor=xr.FormFactor.HEAD_MOUNTED_DISPLAY,
                ),
            )
            logger.info("OpenXR 系统获取成功: system_id=%s", self._system_id)

            return True

        except xr.ExtensionNotPresentError:
            # XR_EXTX_overlay 不可用，回退到只启用 OpenGL 扩展
            logger.warning("XR_EXTX_overlay 不可用，回退到标准 VR 模式")
            try:
                self._instance = xr.create_instance(
                    xr.InstanceCreateInfo(
                        application_info=xr.ApplicationInfo(
                            application_name="nieTTS VR Overlay",
                            application_version=1,
                            engine_name="nieTTS",
                            engine_version=1,
                        ),
                        enabled_extension_names=["XR_KHR_opengl_enable"],
                    )
                )
                logger.info("OpenXR 实例创建成功（标准模式）")

                self._system_id = xr.get_system(
                    self._instance,
                    xr.SystemGetInfo(
                        form_factor=xr.FormFactor.HEAD_MOUNTED_DISPLAY,
                    ),
                )
                logger.info("OpenXR 系统获取成功: system_id=%s", self._system_id)
                return True
            except Exception as e2:
                logger.error("OpenXR 回退也失败: %s", e2, exc_info=True)
                return False

        except Exception as e:
            logger.error("OpenXR 实例/系统创建失败: %s", e, exc_info=True)
            return False

    # ── 阶段 2：主线程 — GL 上下文 + Session ──

    def _init_gl_and_session(self, widget: QWidget) -> bool:
        """创建 OpenGL 上下文和 OpenXR 会话（必须在主线程）。

        使用 pyopenxr 内置的 PySide6OffscreenContextProvider 和
        WGLGraphicsBinding，确保 GL 上下文格式符合 OpenXR 要求。
        """
        from xr.utils.gl import WGLGraphicsBinding
        from xr.utils.gl.pyside import PySide6OffscreenContextProvider

        try:
            # 创建符合 OpenXR 要求的 GL 上下文（4.1 Core, depth=24, stencil=8）
            self._context_provider = PySide6OffscreenContextProvider()
            self._context_provider.make_current()

            # 用 pyopenxr 内置工具提取 HDC/HGLRC 并构造 GraphicsBinding
            graphics_binding = WGLGraphicsBinding(self._context_provider)

            logger.info("GL 图形绑定创建成功: %s", graphics_binding.graphics_binding)

            # 查询 OpenGL 图形要求（验证兼容性）
            try:
                from xr.ext.KHR.opengl_enable import get_graphics_requirements

                reqs = get_graphics_requirements(self._instance, self._system_id)
                logger.info(
                    "OpenGL 版本要求: min=%s, max=%s", reqs.min_api_version_supported, reqs.max_api_version_supported
                )
            except Exception as e:
                logger.debug("查询 OpenGL 要求失败（非致命）: %s", e)

            # 构造 SessionCreateInfo 的 next 链
            # 链顺序: SessionCreateInfo → SessionCreateInfoOverlayEXTX → GraphicsBinding
            # 检查是否支持 overlay 扩展
            try:
                # 创建 overlay 信息，链入 graphics_binding 之前
                overlay_info = xr.SessionCreateInfoOverlayEXTX(
                    create_flags=xr.OverlaySessionCreateFlagsEXTX.NONE,
                    session_layers_placement=0,
                )
                # graphics_binding.next 指向 overlay_info
                graphics_binding.graphics_binding.next = ctypes.pointer(overlay_info)
                self._overlay_mode = True
                logger.info("覆盖层模式: SessionCreateInfoOverlayEXTX 已链接")
            except Exception as e:
                logger.warning("无法创建 overlay 会话信息（回退标准模式）: %s", e)
                self._overlay_mode = False

            # 创建 Session
            self._session = xr.create_session(
                self._instance,
                xr.SessionCreateInfo(
                    system_id=self._system_id,
                    next=graphics_binding.pointer,
                ),
            )
            if self._overlay_mode:
                logger.info("OpenXR 覆盖层会话创建成功")
            else:
                logger.info("OpenXR 标准会话创建成功")

            # 释放上下文（Session 已经持有引用）
            self._context_provider.done_current()

            # 创建渲染器（使用独立上下文，与 context_provider 共享资源）
            self._renderer = OverlayRenderer(
                self._tex_width,
                self._tex_height,
                shared_context=self._context_provider.context,
            )
            self._renderer.init_gl()

            logger.info("阶段 2 完成: GL 上下文 + Session + 渲染器")
            return True

        except Exception as e:
            logger.error("阶段 2 失败: %s", e, exc_info=True)
            if self._context_provider is not None:
                try:
                    self._context_provider.done_current()
                except Exception:
                    pass
            return False

    # ── 阶段 3：子线程 — 交换链、动作等 ──

    def _init_xr_resources(self) -> bool:
        """创建交换链、输入动作、参考空间（子线程安全）。"""
        try:
            # 查询运行时支持的交换链格式
            supported_formats = xr.enumerate_swapchain_formats(self._session)
            logger.info(
                "运行时支持 %d 种交换链格式: %s", len(supported_formats), [hex(f) for f in supported_formats[:10]]
            )

            # 选择一个 GL 格式（优先 RGBA8，其次 SRGB8_ALPHA8，再其次列表第一个）
            # GL_RGBA8=0x8058, GL_SRGB8_ALPHA8=0x8C43, GL_RGBA16F=0x881A
            preferred = [0x8058, 0x8C43, 0x881A, 0x805B]
            swapchain_format = None
            for fmt in preferred:
                if fmt in supported_formats:
                    swapchain_format = fmt
                    break
            if swapchain_format is None and len(supported_formats) > 0:
                swapchain_format = supported_formats[0]

            if swapchain_format is None:
                logger.error("没有可用的交换链格式")
                return False

            logger.info("选择交换链格式: %s", hex(swapchain_format))

            # 创建交换链
            self._swapchain = xr.create_swapchain(
                self._session,
                xr.SwapchainCreateInfo(
                    usage_flags=(xr.SwapchainUsageFlags.COLOR_ATTACHMENT_BIT | xr.SwapchainUsageFlags.SAMPLED_BIT),
                    format=swapchain_format,
                    sample_count=1,
                    width=self._tex_width,
                    height=self._tex_height,
                    face_count=1,
                    array_size=1,
                    mip_count=1,
                ),
            )
            logger.info("OpenXR 交换链创建成功, format=%s", hex(swapchain_format))

            # 枚举交换链图像
            self._swapchain_images = xr.enumerate_swapchain_images(
                self._swapchain,
                xr.SwapchainImageOpenGLKHR,
            )
            logger.info("交换链图像数量: %d", len(self._swapchain_images))

            # 创建参考空间
            self._overlay_space = create_head_relative_space(
                self._session,
                distance=self._distance_meters,
                vertical_offset=self._vertical_offset,
            )
            logger.info("覆盖层参考空间创建成功")

            # 创建输入动作
            self._setup_input_actions()

            # 创建输入处理器
            self._input_handler = OpenXRInputHandler(
                widget=self._widget,
                tex_width=self._tex_width,
                tex_height=self._tex_height,
                overlay_width_meters=self._width_meters,
                overlay_height_meters=self._height_meters,
            )
            self._input_handler.set_manager(self)

            logger.info("阶段 3 完成: 交换链 + 动作 + 输入处理器")
            return True

        except Exception as e:
            logger.error("阶段 3 失败: %s", e, exc_info=True)
            return False

    def _setup_input_actions(self) -> None:
        """创建和绑定输入动作。"""
        self._action_set = xr.create_action_set(
            self._instance,
            xr.ActionSetCreateInfo(
                action_set_name="overlay_interaction",
                localized_action_set_name="Overlay Interaction",
                priority=0,
            ),
        )

        self._aim_action = xr.create_action(
            self._action_set,
            xr.ActionCreateInfo(
                action_name="aim",
                action_type=xr.ActionType.POSE_INPUT,
                localized_action_name="Controller Aim",
            ),
        )
        self._trigger_action = xr.create_action(
            self._action_set,
            xr.ActionCreateInfo(
                action_name="trigger",
                action_type=xr.ActionType.BOOLEAN_INPUT,
                localized_action_name="Trigger Click",
            ),
        )

        self._right_hand_path = xr.string_to_path(
            self._instance,
            "/user/hand/right",
        )

        # 绑定到多种控制器
        profile_paths = [
            "/interaction_profiles/valve/index_controller",
            "/interaction_profiles/htc/vive_controller",
            "/interaction_profiles/oculus/touch_controller",
            "/interaction_profiles/khr/simple_controller",
        ]

        for profile_path in profile_paths:
            try:
                profile = xr.string_to_path(self._instance, profile_path)
                xr.suggest_interaction_profile_bindings(
                    self._instance,
                    xr.InteractionProfileSuggestedBinding(
                        interaction_profile=profile,
                        count_suggested_bindings=2,
                        suggested_bindings=[
                            xr.ActionSuggestedBinding(
                                action=self._aim_action,
                                binding=xr.string_to_path(
                                    self._instance,
                                    "/user/hand/right/input/aim/pose",
                                ),
                            ),
                            xr.ActionSuggestedBinding(
                                action=self._trigger_action,
                                binding=xr.string_to_path(
                                    self._instance,
                                    "/user/hand/right/input/trigger/click",
                                ),
                            ),
                        ],
                    ),
                )
                logger.info("输入绑定成功: %s", profile_path)
            except Exception as e:
                logger.debug("输入绑定跳过 %s: %s", profile_path, e)

        self._aim_space = xr.create_action_space(
            self._session,
            xr.ActionSpaceCreateInfo(
                action=self._aim_action,
                subaction_path=self._right_hand_path,
            ),
        )

        try:
            xr.attach_session_action_sets(
                self._session,
                xr.SessionActionSetsAttachInfo(
                    count_action_sets=1,
                    action_sets=[self._action_set],
                ),
            )
            logger.info("动作集已附加")
        except Exception as e:
            logger.warning("动作集附加失败（可能需要在会话开始后）: %s", e)

    # ── 事件轮询 ──

    def _poll_events(self) -> None:
        """轮询 OpenXR 事件。"""
        if self._instance is None:
            return

        while True:
            try:
                event_buffer = xr.poll_event(self._instance)
                event_type = xr.StructureType(event_buffer.type)

                if event_type == xr.StructureType.EVENT_DATA_SESSION_STATE_CHANGED:
                    state_event = ctypes.cast(
                        ctypes.pointer(event_buffer),
                        ctypes.POINTER(xr.EventDataSessionStateChanged),
                    ).contents
                    self._handle_session_state_changed(state_event)

                elif event_type == xr.StructureType.EVENT_DATA_INTERACTION_PROFILE_CHANGED:
                    logger.info("交互配置已变化")

                elif event_type == xr.StructureType.EVENT_DATA_INSTANCE_LOSS_PENDING:
                    logger.warning("实例即将丢失")
                    self._running = False
                    return

                elif event_type == xr.StructureType.EVENT_DATA_EVENTS_LOST:
                    logger.warning("有事件丢失")

                elif event_type == xr.StructureType.EVENT_DATA_MAIN_SESSION_VISIBILITY_CHANGED_EXTX:
                    # 覆盖层模式：主会话可见性变化
                    vis_event = ctypes.cast(
                        ctypes.pointer(event_buffer),
                        ctypes.POINTER(xr.EventDataMainSessionVisibilityChangedEXTX),
                    ).contents
                    self._overlay_visible = bool(vis_event.visible)
                    logger.info("覆盖层可见性: %s", "可见" if self._overlay_visible else "隐藏")

            except xr.EventUnavailable:
                break
            except Exception as e:
                logger.debug("事件轮询异常: %s", e)
                break

    def _handle_session_state_changed(self, event) -> None:
        """处理会话状态变化。"""
        old_state = self._session_state
        self._session_state = xr.SessionState(event.state)
        logger.info("会话状态: %s → %s", old_state.name, self._session_state.name)

        if self._session_state == xr.SessionState.READY:
            try:
                xr.begin_session(
                    self._session,
                    xr.SessionBeginInfo(
                        primary_view_configuration_type=xr.ViewConfigurationType.PRIMARY_STEREO,
                    ),
                )
                self._session_running = True
                logger.info("会话已开始")
            except Exception as e:
                logger.error("开始会话失败: %s", e)

        elif self._session_state == xr.SessionState.STOPPING:
            try:
                xr.end_session(self._session)
                self._session_running = False
                logger.info("会话已结束")
            except Exception as e:
                logger.error("结束会话失败: %s", e)

        elif self._session_state == xr.SessionState.EXITING:
            self._running = False

    # ── 帧处理 ──

    def _process_frame(self) -> None:
        """处理一帧：等待帧 → 输入 → 渲染 → 提交。"""
        if self._session is None or not self._session_running:
            return

        try:
            self._frame_state = xr.wait_frame(self._session)
            xr.begin_frame(self._session)

            self._sync_and_process_input()

            layers = self._render_and_submit()

            xr.end_frame(
                self._session,
                xr.FrameEndInfo(
                    display_time=self._frame_state.predicted_display_time,
                    environment_blend_mode=xr.EnvironmentBlendMode.OPAQUE,
                    layer_count=len(layers),
                    layers=layers if layers else None,
                ),
            )

        except xr.FrameDiscarded:
            logger.debug("帧被丢弃")
        except xr.SessionLossPending:
            logger.warning("会话即将丢失")
            self._running = False
        except Exception as e:
            logger.debug("帧处理异常: %s", e)

    def _sync_and_process_input(self) -> None:
        """同步动作状态并处理射线输入。"""
        if (
            self._action_set is None
            or self._aim_space is None
            or self._overlay_space is None
            or self._frame_state is None
        ):
            return

        try:
            xr.sync_actions(
                self._session,
                xr.ActionsSyncInfo(
                    count_active_action_sets=1,
                    active_action_sets=[
                        xr.ActiveActionSet(
                            action_set=self._action_set,
                            subaction_path=0,
                        )
                    ],
                ),
            )

            aim_state = xr.get_action_state_pose(
                self._session,
                xr.ActionStateGetInfo(
                    action=self._aim_action,
                    subaction_path=self._right_hand_path,
                ),
            )

            if not aim_state.is_active:
                return

            space_location = xr.locate_space(
                self._aim_space,
                self._overlay_space,
                self._frame_state.predicted_display_time,
            )

            if not (space_location.location_flags & xr.SpaceLocationFlags.POSITION_VALID):
                return

            trigger_state_obj = xr.get_action_state_boolean(
                self._session,
                xr.ActionStateGetInfo(
                    action=self._trigger_action,
                    subaction_path=self._right_hand_path,
                ),
            )
            trigger_pressed = bool(trigger_state_obj.current_state)

            # 更新面板几何
            self._input_handler.update_quad_surface(
                xr.Posef(
                    orientation=xr.Quaternionf(x=0, y=0, z=0, w=1),
                    position=xr.Vector3f(x=0, y=0, z=0),
                )
            )

            controller_pos = (
                space_location.pose.position.x,
                space_location.pose.position.y,
                space_location.pose.position.z,
            )
            controller_rot = (
                space_location.pose.orientation.x,
                space_location.pose.orientation.y,
                space_location.pose.orientation.z,
                space_location.pose.orientation.w,
            )

            hit = self._input_handler.process_input(
                controller_pos,
                controller_rot,
                trigger_pressed,
            )

            # 更新 widget 状态显示
            if self._widget is not None and hasattr(self._widget, "update_ray_status"):
                if hit.hit:
                    pos = self._input_handler.last_widget_pos
                    self._widget.update_crosshair_coord(pos.x(), pos.y())
                    self._widget.update_ray_status(True, hit.u, hit.v, hit.distance)
                else:
                    self._widget.update_ray_status(False, 0, 0, 0)
                self._widget.update_trigger_status(trigger_pressed)

        except Exception as e:
            logger.debug("输入处理异常: %s", e)

    # ── 渲染和提交 ──

    def _render_and_submit(self) -> list:
        """渲染 Widget 到纹理并构建合成层。"""
        layers = []

        if self._swapchain is None or self._renderer is None or self._overlay_space is None or self._widget is None:
            return layers

        if not self._dirty:
            return self._build_layers()

        try:
            self._renderer.render_widget(self._widget)

            xr.acquire_swapchain_image(
                self._swapchain,
                xr.SwapchainImageAcquireInfo(),
            )

            xr.wait_swapchain_image(
                self._swapchain,
                xr.SwapchainImageWaitInfo(
                    timeout=xr.Duration(1_000_000_000),
                ),
            )

            xr.release_swapchain_image(self._swapchain, xr.SwapchainImageReleaseInfo())

            self._renderer.finish()

            self._dirty = False

        except Exception as e:
            logger.debug("渲染提交异常: %s", e)
            if self._renderer is not None:
                self._renderer.finish()

        return self._build_layers()

    def _build_layers(self) -> list:
        """构建合成层列表。"""
        layers = []

        if self._swapchain is None or self._overlay_space is None:
            return layers

        panel_pose = xr.Posef(
            orientation=xr.Quaternionf(x=0.0, y=0.0, z=0.0, w=1.0),
            position=xr.Vector3f(x=0.0, y=0.0, z=0.0),
        )

        quad = build_quad_layer(
            swapchain=self._swapchain,
            space=self._overlay_space,
            pose=panel_pose,
            width_meters=self._width_meters,
            height_meters=self._height_meters,
            tex_width=self._tex_width,
            tex_height=self._tex_height,
            alpha=self._alpha,
        )

        layers.append(ctypes.pointer(quad))
        return layers

    # ── 清理 ──

    async def stop(self) -> None:
        """异步停止覆盖层。"""
        logger.info("正在停止 OpenXR 覆盖层...")
        self._running = False
        await asyncio.sleep(0.1)

    async def _cleanup(self) -> None:
        """清理所有资源。"""
        logger.info("清理 OpenXR 资源...")

        # GL 资源必须在主线程清理（GL 上下文绑定到创建线程）
        if self._renderer is not None:
            self._renderer.cleanup()
            self._renderer = None

        if self._context_provider is not None:
            try:
                self._context_provider.destroy()
            except Exception:
                pass
            self._context_provider = None

        # OpenXR 资源在子线程清理（与 GL 无关）
        await asyncio.to_thread(self._cleanup_openxr)

        self._input_handler = None
        logger.info("OpenXR 资源清理完成")

    def _cleanup_openxr(self) -> None:
        """清理 OpenXR 资源。"""
        try:
            if self._aim_space is not None:
                xr.destroy_space(self._aim_space)
                self._aim_space = None

            if self._action_set is not None:
                xr.destroy_action_set(self._action_set)
                self._action_set = None

            if self._overlay_space is not None:
                xr.destroy_space(self._overlay_space)
                self._overlay_space = None

            if self._swapchain is not None:
                xr.destroy_swapchain(self._swapchain)
                self._swapchain = None

            if self._session is not None:
                if self._session_running:
                    try:
                        xr.end_session(self._session)
                    except Exception:
                        pass
                xr.destroy_session(self._session)
                self._session = None

            if self._instance is not None:
                xr.destroy_instance(self._instance)
                self._instance = None

        except Exception as e:
            logger.warning("OpenXR 清理异常: %s", e)

    def show(self) -> None:
        """显示覆盖层。"""
        self._dirty = True

    def hide(self) -> None:
        """隐藏覆盖层。"""
        pass

    def toggle(self) -> None:
        """切换显示/隐藏。"""
        self._dirty = True

    def move_relative(self, dx: float, dy: float, dz: float) -> None:
        """相对移动覆盖层（暂不实现）。"""
        logger.debug("move_relative 暂不实现: (%.2f, %.2f, %.2f)", dx, dy, dz)
