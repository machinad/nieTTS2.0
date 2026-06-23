"""OpenVR 生命周期管理 + 事件轮询（async 协程驱动）。

负责：
- 异步初始化 OpenVR 运行时（阻塞 C FFI 调用在子线程，Qt 对象在主线程）
- 创建和管理覆盖层
- 设置覆盖层位置（控制器相对 / HMD 相对）
- 60Hz 主循环：轮询 VR 事件 → 处理 → 渲染 → 提交纹理
- 异步清理资源

架构：
    asyncio.create_task(manager.run(widget, config))
        → asyncio.to_thread(_init_openvr_blocking)  子线程执行阻塞 OpenVR 调用
        → _setup_qt_components()                     主线程创建 Qt 对象
        → 60Hz while 循环（pump → render → sleep）
    await manager.stop() 异步关闭
"""

import asyncio
import logging
import time
from typing import Optional

from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)

# OpenVR 常量（延迟导入，避免未安装时崩溃）
openvr = None
_OPENVR_IMPORTED = False


def _ensure_openvr():
    """延迟导入 openvr 模块。"""
    global openvr, _OPENVR_IMPORTED
    if not _OPENVR_IMPORTED:
        try:
            import openvr as _openvr
            openvr = _openvr
            _OPENVR_IMPORTED = True
        except ImportError:
            logger.error("openvr 模块未安装，请执行: pip install openvr")
            raise
    return openvr


class VROverlayManager:
    """OpenVR 覆盖层生命周期管理器（async 协程驱动）。

    职责：
        1. run(widget, config) → 异步初始化 + 60Hz 主循环
        2. stop() → 异步停止循环 + 清理资源
        3. show() / hide() → 控制覆盖层可见性
        4. mark_dirty() → 标记需要重绘

    用法：
        manager = VROverlayManager()
        asyncio.create_task(manager.run(widget, config))
        # ... 应用运行 ...
        await manager.stop()
    """

    # 主循环目标帧率
    _TARGET_FPS = 60

    def __init__(self):
        # OpenVR 句柄
        self._overlay_handle = None
        self._vr_system = None
        self._vr_overlay = None

        # 子模块
        self._renderer = None
        self._input_handler = None
        self._widget = None
        self._crosshair = None
        self._ray_tracker = None

        # 状态
        self._initialized = False
        self._visible = False
        self._dirty = True  # 脏标记：需要重绘
        self._running = False  # 主循环运行标志

        # asyncio 任务引用
        self._loop_task: Optional[asyncio.Task] = None

        # 配置（默认值，可从 config.json 覆盖）
        self._config = {
            "width_meters": 2.0,
            "texture_width": 1792,
            "texture_height": 1208,
            "distance_meters": 1.5,
            "vertical_offset": -0.1,
            "alpha": 0.9,
        }

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def is_visible(self) -> bool:
        return self._visible

    def set_config(self, config: dict):
        """从 config.json 加载配置。"""
        vr_cfg = config.get("vr_overlay", {})
        self._config.update(vr_cfg)
        logger.info("VR 覆盖层配置已加载: %s", self._config)

    # ── 异步生命周期 ──────────────────────────────────────────

    async def run(self, widget: QWidget, config: Optional[dict] = None):
        """主入口：异步初始化 + 60Hz 事件循环。

        调用方通过 asyncio.create_task() 启动，返回时资源已清理。
        """
        if config:
            self.set_config(config)
        self._widget = widget

        # 异步初始化（阻塞 OpenVR 调用在子线程，Qt 对象在主线程）
        if not await self._init_openvr():
            logger.warning("VR 覆盖层初始化失败，主循环不启动")
            return

        self._loop_task = asyncio.current_task()
        self._running = True
        dt = 1.0 / self._TARGET_FPS
        logger.info("VR 覆盖层主循环启动 (%dHz)", self._TARGET_FPS)

        try:
            while self._running:
                t0 = time.monotonic()

                # 1. 轮询 OpenVR 事件
                self._pump_events()

                # 2. 感应式射线追踪（每帧检测控制器与覆盖层的交点）
                if self._ray_tracker:
                    self._ray_tracker.update()

                # 3. 按需渲染并提交纹理
                self._render_and_submit()

                # 4. 精确休眠到下一帧
                elapsed = time.monotonic() - t0
                await asyncio.sleep(max(0, dt - elapsed))

        except asyncio.CancelledError:
            logger.debug("VR 主循环被取消")
        except Exception as e:
            logger.error("VR 主循环异常: %s", e)
        finally:
            await self._cleanup()

    async def stop(self):
        """停止主循环并清理资源。"""
        self._running = False
        if self._loop_task is not None and not self._loop_task.done():
            self._loop_task.cancel()
            try:
                await self._loop_task
            except (asyncio.CancelledError, Exception):
                pass
            self._loop_task = None
        else:
            # 循环已退出但 _cleanup 可能未执行
            await self._cleanup()

    # ── 异步初始化 ────────────────────────────────────────────

    async def _init_openvr(self) -> bool:
        """两阶段初始化：子线程阻塞 OpenVR → 主线程 Qt 对象。"""

        # 阶段 1：所有阻塞的 OpenVR C FFI 调用 → 子线程
        try:
            ok = await asyncio.to_thread(self._init_openvr_blocking)
        except Exception as e:
            logger.error("OpenVR 初始化线程异常: %s", e)
            return False
        if not ok:
            return False

        # 阶段 2：Qt 对象（QWidget/QOpenGLContext 必须主线程）
        return self._setup_qt_components()

    def _init_openvr_blocking(self) -> bool:
        """阻塞式 OpenVR 初始化 —— 在子线程中执行。

        包含所有可能阻塞的 C FFI 调用：
        import openvr, isHmdPresent, init, createOverlay, setOverlay* 等。
        """
        # 导入 openvr
        try:
            ov = _ensure_openvr()
        except ImportError:
            return False

        # 预检查 SteamVR 状态
        try:
            if not ov.isHmdPresent():
                logger.error("未检测到 VR 头显设备")
                return False
            if not ov.isRuntimeInstalled():
                logger.error("未安装 SteamVR 运行时")
                return False
            logger.info("SteamVR 预检查通过")
        except Exception as e:
            logger.error("SteamVR 状态检查失败: %s", e)
            return False

        # 初始化 OpenVR（覆盖层模式）
        try:
            self._vr_system = ov.init(ov.VRApplication_Overlay)
            logger.info("OpenVR 初始化成功（覆盖层模式）")
        except Exception as e:
            logger.error("OpenVR 初始化失败: %s", e)
            return False

        # 获取 Overlay 接口
        try:
            self._vr_overlay = ov.VROverlay()
            logger.info("VROverlay 接口获取成功")
        except Exception as e:
            logger.error("VROverlay 接口获取失败: %s", e)
            self._cleanup_vr()
            return False

        # 创建覆盖层
        try:
            self._overlay_handle = self._vr_overlay.createOverlay(
                "nietts_vr_overlay",           # 唯一键
                "nieTTS 2.0 VR Overlay"        # 显示名称
            )
            logger.info("覆盖层创建成功, handle=%s", self._overlay_handle)
        except Exception as e:
            logger.error("覆盖层创建失败: %s", e)
            self._cleanup_vr()
            return False

        # 设置覆盖层参数
        try:
            width = self._config["width_meters"]
            self._vr_overlay.setOverlayWidthInMeters(self._overlay_handle, width)

            alpha = self._config.get("alpha", 0.9)
            self._vr_overlay.setOverlayAlpha(self._overlay_handle, alpha)

            logger.info("覆盖层参数设置完成: width=%.1fm, alpha=%.1f", width, alpha)
        except Exception as e:
            logger.error("覆盖层参数设置失败: %s", e)
            self._cleanup_vr()
            return False

        # 设置覆盖层位置
        if not self._setup_transform():
            self._cleanup_vr()
            return False

        # 显示覆盖层
        try:
            self._vr_overlay.showOverlay(self._overlay_handle)
            logger.info("VR 覆盖层已显示")
        except Exception as e:
            logger.error("显示覆盖层失败: %s", e)
            self._cleanup_vr()
            return False

        # 启用输入（必须在 showOverlay 之后）
        try:
            tex_w = self._config.get("texture_width", 1792)
            tex_h = self._config.get("texture_height", 1208)

            self._vr_overlay.setOverlayInputMethod(
                self._overlay_handle,
                ov.VROverlayInputMethod_Mouse
            )

            # 设置鼠标缩放（纹理尺寸）
            mouse_scale = ov.HmdVector2_t()
            mouse_scale.v[0] = tex_w
            mouse_scale.v[1] = tex_h
            self._vr_overlay.setOverlayMouseScale(self._overlay_handle, mouse_scale)

            # 设置交互 Flag（不启用 SteamVR 内置激光，使用自定义射线追踪）
            self._vr_overlay.setOverlayFlag(
                self._overlay_handle,
                ov.VROverlayFlags_SendVRDiscreteScrollEvents,
                True
            )

            logger.info("输入方法设置完成: mouse_scale=%dx%d", tex_w, tex_h)
        except Exception as e:
            logger.error("输入方法设置失败: %s", e)
            self._cleanup_vr()
            return False

        logger.info("OpenVR 子线程初始化完成")
        return True

    def _setup_qt_components(self) -> bool:
        """Qt 对象初始化 —— 在主线程中执行。

        QOpenGLContext、QOffscreenSurface、QWidget 必须在主线程创建。
        """
        tex_w = self._config.get("texture_width", 1792)
        tex_h = self._config.get("texture_height", 1208)

        # 初始化渲染器
        from gui.vr_overlay.renderer import VROverlayRenderer
        self._renderer = VROverlayRenderer(tex_w, tex_h)
        if not self._renderer.init_gl():
            logger.error("FBO 渲染器初始化失败")
            self._cleanup_vr()
            return False

        # 初始化准星
        from gui.vr_overlay.crosshair import VRCrosshairOverlay
        self._crosshair = VRCrosshairOverlay(self._widget)
        self._crosshair.resize(self._widget.size())
        self._crosshair.show()

        # 初始化输入处理器
        from gui.vr_overlay.input_handler import VRInputHandler
        tex_w = self._config.get("texture_width", 1792)
        tex_h = self._config.get("texture_height", 1208)
        self._input_handler = VRInputHandler(
            self._widget, self._crosshair, manager=self,
            tex_w=tex_w, tex_h=tex_h,
        )

        # 初始化感应式射线追踪器
        from gui.vr_overlay.ray_tracker import VRRayTracker
        self._ray_tracker = VRRayTracker(
            overlay=self._vr_overlay,
            overlay_handle=self._overlay_handle,
            input_handler=self._input_handler,
            tex_width=tex_w,
            tex_height=tex_h,
        )
        self._ray_tracker.init()

        # 标记脏，主循环首帧会渲染
        self._dirty = True
        self._visible = True
        self._initialized = True
        logger.info("VR 覆盖层 Qt 组件初始化完成")
        return True

    # ── 事件轮询 ──────────────────────────────────────────────

    def _pump_events(self):
        """轮询并处理 VR 事件。"""
        if not self._initialized or self._vr_overlay is None:
            return

        try:
            ov = _ensure_openvr()
            event = ov.VREvent_t()

            result, _ = self._vr_overlay.pollNextOverlayEvent(self._overlay_handle, event)
            while result:
                logger.debug("VR事件: type=%d device=%d", event.eventType, event.trackedDeviceIndex)
                if self._input_handler:
                    self._input_handler.process_vr_event(event)
                result, _ = self._vr_overlay.pollNextOverlayEvent(self._overlay_handle, event)
        except Exception as e:
            logger.warning("VR 事件轮询异常: %s", e)

    # ── 渲染提交 ──────────────────────────────────────────────

    def _render_and_submit(self):
        """渲染 Widget 并提交纹理到 OpenVR。"""
        if not self._initialized or not self._visible:
            return
        if self._renderer is None or self._widget is None:
            return
        if not self._dirty:
            return  # 跳过无变化的帧
        self._dirty = False

        try:
            # 渲染 Widget 到 FBO（GL 上下文保持 current）
            texture_id = self._renderer.render_widget(self._widget)
            if texture_id is None:
                self._renderer.finish()
                return

            # 提交纹理到 OpenVR（需要 GL 上下文 current）
            texture = self._renderer.get_texture_struct(texture_id)
            if texture is not None:
                self._vr_overlay.setOverlayTexture(self._overlay_handle, texture)
            self._renderer.finish()
        except Exception as e:
            self._renderer.finish()
            logger.warning("渲染提交异常: %s", e)

    def mark_dirty(self):
        """标记覆盖层需要重绘。"""
        self._dirty = True

    # ── 覆盖层控制 ────────────────────────────────────────────

    def show(self):
        """显示覆盖层。"""
        if not self._initialized:
            logger.warning("VR 覆盖层未初始化")
            return

        try:
            self._vr_overlay.showOverlay(self._overlay_handle)
            self._visible = True
            self._dirty = True
            logger.info("VR 覆盖层已显示")
        except Exception as e:
            logger.error("显示覆盖层失败: %s", e)

    def hide(self):
        """隐藏覆盖层。"""
        if not self._initialized:
            return

        try:
            self._vr_overlay.hideOverlay(self._overlay_handle)
            self._visible = False
            logger.info("VR 覆盖层已隐藏")
        except Exception as e:
            logger.error("隐藏覆盖层失败: %s", e)

    def toggle(self):
        """切换覆盖层可见性。"""
        if self._visible:
            self.hide()
        else:
            self.show()

    def move_relative(self, dx: float = 0, dy: float = 0, dz: float = 0):
        """相对移动覆盖层（米）。"""
        if not self._initialized:
            return

        try:
            ov = _ensure_openvr()
            # 获取当前变换
            transform = ov.HmdMatrix34_t()
            tracking_origin = ov.TrackingUniverseSeated
            self._vr_overlay.getOverlayTransformAbsolute(
                self._overlay_handle, tracking_origin, transform
            )

            # 修改平移
            transform.m[0][3] += dx
            transform.m[1][3] += dy
            transform.m[2][3] += dz

            self._vr_overlay.setOverlayTransformAbsolute(
                self._overlay_handle, tracking_origin, transform
            )
            logger.info("覆盖层移动: dx=%.2f, dy=%.2f, dz=%.2f", dx, dy, dz)
        except Exception as e:
            logger.error("覆盖层移动失败: %s", e)

    # ── 位置设置 ──────────────────────────────────────────────

    def _setup_transform(self) -> bool:
        """设置覆盖层位置（相对于 HMD）。"""
        try:
            ov = _ensure_openvr()

            # 构造变换矩阵：向前 distance 米，向下 vertical_offset 米
            distance = self._config.get("distance_meters", 1.5)
            v_offset = self._config.get("vertical_offset", -0.1)

            # HmdMatrix34_t 是 3x4 行主序矩阵
            transform = ov.HmdMatrix34_t()
            # 旋转部分（单位矩阵）
            transform.m[0][0] = 1.0
            transform.m[0][1] = 0.0
            transform.m[0][2] = 0.0
            transform.m[1][0] = 0.0
            transform.m[1][1] = 1.0
            transform.m[1][2] = 0.0
            transform.m[2][0] = 0.0
            transform.m[2][1] = 0.0
            transform.m[2][2] = 1.0
            # 平移部分（-Z 向前，+Y 向上）
            transform.m[0][3] = 0.0           # X: 居中
            transform.m[1][3] = v_offset      # Y: 向下偏移
            transform.m[2][3] = -distance     # Z: 向前

            self._vr_overlay.setOverlayTransformTrackedDeviceRelative(
                self._overlay_handle,
                ov.k_unTrackedDeviceIndex_Hmd,
                transform
            )
            logger.info("覆盖层位置设置完成: distance=%.1fm, offset=%.1fm", distance, v_offset)
            return True
        except Exception as e:
            logger.error("覆盖层位置设置失败: %s", e)
            return False

    # ── 清理 ──────────────────────────────────────────────────

    def _cleanup_vr(self):
        """清理 OpenVR 资源。"""
        if self._vr_overlay is not None and self._overlay_handle is not None:
            try:
                self._vr_overlay.destroyOverlay(self._overlay_handle)
            except Exception:
                pass
            self._overlay_handle = None

        try:
            _ensure_openvr().shutdown()
        except Exception:
            pass

        self._vr_system = None
        self._vr_overlay = None

    async def _cleanup(self):
        """释放所有资源。"""
        # 清理渲染器（Qt 对象，必须主线程）
        if self._renderer is not None:
            self._renderer.cleanup()
            self._renderer = None

        # 清理 OpenVR（C FFI 调用，移到子线程避免阻塞）
        if self._vr_overlay is not None or self._vr_system is not None:
            try:
                await asyncio.to_thread(self._cleanup_vr)
            except Exception as e:
                logger.warning("OpenVR 清理异常: %s", e)

        self._initialized = False
        self._visible = False
        logger.info("VR 覆盖层资源已释放")
