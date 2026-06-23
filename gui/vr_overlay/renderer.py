"""FBO 渲染管线：Widget → FBO → OpenGL Texture → OpenVR

正确实现：
- QOpenGLContext + QOffscreenSurface 管理 GL 上下文
- QOpenGLPaintDevice 作为 QPainter 目标（不是 QOpenGLFramebufferObject）
- drawPixmap 替代 widget.render()（避免类型兼容问题）
- render_widget 不释放 GL 上下文，finish() 后释放
"""

import logging
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QOpenGLContext, QSurfaceFormat, QOffscreenSurface, QPainter
from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLPaintDevice
from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class VROverlayRenderer:
    """使用 FBO 将 QWidget 渲染为 GPU 纹理，供 setOverlayTexture 使用。

    渲染流程：
        widget.grab() → QPixmap(GPU) → drawPixmap → FBO texture(GPU)
        → setOverlayTexture(handle, texture) → SteamVR 直接读取 GPU 纹理
    """

    def __init__(self, width: int = 1792, height: int = 1208):
        self._width = width
        self._height = height
        self._fbo: Optional[QOpenGLFramebufferObject] = None
        self._context: Optional[QOpenGLContext] = None
        self._surface: Optional[QOffscreenSurface] = None

    @property
    def size(self) -> QSize:
        return QSize(self._width, self._height)

    def init_gl(self) -> bool:
        """初始化 GL 上下文和 FBO。返回是否成功。"""
        try:
            fmt = QSurfaceFormat()
            fmt.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
            fmt.setSwapInterval(0)

            self._surface = QOffscreenSurface()
            self._surface.setFormat(fmt)
            self._surface.create()

            self._context = QOpenGLContext()
            self._context.setFormat(fmt)
            if not self._context.create():
                logger.error("OpenGL 上下文创建失败")
                return False

            if not self._context.makeCurrent(self._surface):
                logger.error("无法激活 OpenGL 上下文")
                return False

            self._fbo = QOpenGLFramebufferObject(QSize(self._width, self._height))
            if not self._fbo.isValid():
                logger.error("FBO 创建失败")
                self._context.doneCurrent()
                return False

            self._context.doneCurrent()
            logger.info("FBO 渲染器初始化成功: %dx%d, texture=%d",
                        self._width, self._height, self._fbo.texture())
            return True

        except Exception as e:
            logger.error("FBO 初始化异常: %s", e)
            return False

    def resize(self, width: int, height: int):
        """调整 FBO 尺寸。"""
        if width == self._width and height == self._height:
            return
        self._width = width
        self._height = height
        if self._context and self._surface:
            self._context.makeCurrent(self._surface)
            self._fbo = QOpenGLFramebufferObject(QSize(width, height))
            self._context.doneCurrent()
            logger.info("FBO 尺寸变更: %dx%d", width, height)

    def render_widget(self, widget: QWidget) -> Optional[int]:
        """将 widget 渲染到 FBO，返回纹理 ID。

        注意：不释放 GL 上下文！调用方必须在 setOverlayTexture 后调用 finish()。
        """
        if self._fbo is None or self._context is None:
            return None

        try:
            self._context.makeCurrent(self._surface)
            self._fbo.bind()

            # QOpenGLPaintDevice 是 QPaintDevice，QPainter 可以绑定
            paint_device = QOpenGLPaintDevice(self._fbo.size())
            painter = QPainter(paint_device)
            pixmap = widget.grab()
            painter.drawPixmap(0, 0, self._width, self._height, pixmap)
            painter.end()

            self._fbo.release()
            # 不调用 doneCurrent()！上下文保持 current
            return int(self._fbo.texture())

        except Exception as e:
            logger.error("Widget 渲染失败: %s", e)
            if self._fbo and self._fbo.isBound():
                self._fbo.release()
            return None

    def get_texture_struct(self, texture_id: int):
        """构造 OpenVR Texture_t 结构体。"""
        try:
            import openvr
            texture = openvr.Texture_t()
            texture.handle = texture_id
            texture.eType = openvr.TextureType_OpenGL
            texture.eColorSpace = openvr.ColorSpace_Gamma
            return texture
        except ImportError:
            logger.error("openvr 模块未安装")
            return None

    def finish(self):
        """在 setOverlayTexture 调用后释放 GL 上下文。"""
        if self._context:
            self._context.doneCurrent()

    def cleanup(self):
        """释放 OpenGL 资源。"""
        if self._fbo is not None:
            try:
                if self._context and self._surface:
                    self._context.makeCurrent(self._surface)
                    if self._fbo.isBound():
                        self._fbo.release()
                    self._context.doneCurrent()
            except Exception as e:
                logger.warning("FBO 清理警告: %s", e)
            finally:
                self._fbo = None
        self._context = None
        self._surface = None
        logger.debug("FBO 已释放")
