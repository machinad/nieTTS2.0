"""FBO 渲染管线：Widget → OpenGL 纹理。

使用 QOffscreenSurface + QOpenGLFramebufferObject 将 PySide6 Widget
离屏渲染为 OpenGL 纹理，供 OpenXR Swapchain 使用。
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize
from PySide6.QtGui import QOffscreenSurface, QOpenGLContext, QPainter, QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLPaintDevice

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class OverlayRenderer:
    """离屏渲染器：将 QWidget 渲染为 OpenGL 纹理。"""

    def __init__(
        self,
        width: int,
        height: int,
        shared_context: QOpenGLContext | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self._shared_context = shared_context
        self._surface: QOffscreenSurface | None = None
        self._context: QOpenGLContext | None = None
        self._fbo: QOpenGLFramebufferObject | None = None
        self._initialized = False

    def init_gl(self) -> None:
        """初始化 OpenGL 资源（必须在主线程调用）。"""
        if self._initialized:
            return

        self._surface = QOffscreenSurface()
        self._surface.setFormat(
            self._shared_context.format() if self._shared_context
            else QSurfaceFormat.defaultFormat()
        )
        self._surface.create()

        self._context = QOpenGLContext()
        if self._shared_context is not None:
            self._context.setShareContext(self._shared_context)
        self._context.create()

        self._context.makeCurrent(self._surface)
        self._fbo = QOpenGLFramebufferObject(QSize(self.width, self.height))
        self._context.doneCurrent()

        self._initialized = True
        logger.info("OpenXR FBO 渲染器初始化: %dx%d, texture=%s",
                     self.width, self.height, self._fbo.texture())

    def render_widget(self, widget: QWidget) -> int:
        """将 QWidget 渲染到 FBO 并返回纹理 ID。

        注意：调用后 GL 上下文保持 current，必须调用 finish() 释放。
        """
        if not self._initialized or self._fbo is None:
            raise RuntimeError("渲染器未初始化")

        self._context.makeCurrent(self._surface)
        self._fbo.bind()

        paint_device = QOpenGLPaintDevice(self._fbo.size())
        painter = QPainter(paint_device)
        pixmap = widget.grab()
        painter.drawPixmap(0, 0, self.width, self.height, pixmap)
        painter.end()

        self._fbo.release()
        # 不调用 doneCurrent()，上下文保持 current
        return int(self._fbo.texture())

    def finish(self) -> None:
        """释放 GL 上下文（在纹理提交后调用）。"""
        if self._context is not None:
            self._context.doneCurrent()

    def get_texture_id(self) -> int:
        """获取当前 FBO 纹理 ID。"""
        if self._fbo is None:
            return 0
        return int(self._fbo.texture())

    def cleanup(self) -> None:
        """清理 OpenGL 资源。"""
        if self._fbo is not None:
            if self._context is not None and self._surface is not None:
                self._context.makeCurrent(self._surface)
                self._fbo.release()
                self._fbo = None
                self._context.doneCurrent()
            else:
                self._fbo = None

        if self._context is not None:
            self._context.destroy()
            self._context = None

        if self._surface is not None:
            self._surface.destroy()
            self._surface = None

        self._initialized = False
        logger.info("OpenXR FBO 渲染器已清理")
