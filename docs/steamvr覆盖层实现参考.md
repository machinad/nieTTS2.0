# SteamVR 覆盖层实现参考

> nieTTS 项目中将 PySide6 GUI 注入 SteamVR 覆盖层的完整实现参考。
> **目标**：Agent 通过本文档能完整正确实现功能，不再踩之前的坑。

---

## 1. 架构总览

### 1.1 渲染管线（FBO + setOverlayTexture）

```
PySide Widget (QWidget)
     ↓ widget.grab() → QPixmap (GPU 资源)
QOpenGLFramebufferObject (GPU 离屏渲染)
     ↓ painter.drawPixmap() → GPU→GPU blit，无 CPU 拷贝
OpenGL Texture (稳定 ID，由 fbo.texture() 返回，创建后不变)
     ↓ openvr.setOverlayTexture(handle, texture)
OpenVR Overlay (SteamVR 直接读取 GPU 纹理)
```

**关键**：纹理 ID 在 FBO 生命周期内不变。`setOverlayTexture` 每帧调用但传入相同 ID，只是通知 SteamVR 内容已更新。

### 1.2 输入管线

```
手柄射线指向覆盖层 → SteamVR compositor 检测交叉
     ↓
VREvent_t (MouseMove=300, MouseDown=301, MouseUp=302, Scroll=305)
     ↓ pollNextOverlayEvent() 每 50ms 轮询
input_handler._to_widget_pos() → VR 坐标 → widget 坐标
     ↓ _resolve_target() → childAt(pos) 找到子 widget (按钮等)
QApplication.sendEvent(target, QMouseEvent) → 转发到子 widget
```

### 1.3 文件结构

```
gui/vr_overlay/
├── __init__.py          # 导出 VROverlayManager, VROverlayTestWidget
├── gl_renderer.py       # FBO 渲染器（核心，不可替换为其他方案）
├── input_handler.py     # VR 事件 → Qt 事件转换
├── manager.py           # OpenVR 生命周期、事件轮询、纹理提交
├── renderer.py          # 备用：CPU 缓冲区渲染器（setOverlayRaw 方案，有闪烁）
└── widget.py            # 测试 UI
```

**只有 `gl_renderer.py` + `setOverlayTexture` 能实现无闪烁渲染。`renderer.py` 是备用方案，有闪烁。**

---

## 2. 关键实现细节

### 2.1 OpenVR 初始化顺序（必须严格遵守）

```python
# 1. 初始化 OpenVR
openvr.init(openvr.VRApplication_Overlay)
overlay = openvr.IVROverlay()
handle = overlay.createOverlay("com.nietts.vr_overlay", "nieTTS VR Panel")

# 2. 设置覆盖层属性
overlay.setOverlayWidthInMeters(handle, width_meters)
overlay.setOverlayAlpha(handle, 1.0)

# 3. 定位
overlay.setOverlayTransformTrackedDeviceRelative(handle, device_idx, matrix)

# 4. 创建渲染器（FBO + GL 上下文）
renderer = GLOverlayRenderer(texture_width, texture_height)

# 5. 首次渲染并显示
renderer.render_widget(widget)        # 渲染到 FBO
overlay.setOverlayTexture(handle, vr_texture)  # 提交纹理
renderer.finish()                     # 释放 GL 上下文
overlay.showOverlay(handle)           # 显示覆盖层

# 6. 启用输入（必须在 showOverlay 之后）
overlay.setOverlayInputMethod(handle, openvr.VROverlayInputMethod_Mouse)
overlay.setOverlayMouseScale(handle, HmdVector2_t(texture_w, texture_h))
overlay.setOverlayFlag(handle, VROverlayFlags_SendVRDiscreteScrollEvents, True)
overlay.setOverlayFlag(handle, VROverlayFlags_MakeOverlaysInteractiveIfVisible, True)
```

### 2.2 GL 上下文生命周期（致命陷阱）

```python
# gl_renderer.py — render_widget 中
self._context.makeCurrent(self._surface)  # 激活上下文
self._fbo.bind()
# ... 渲染 ...
self._fbo.release()
return self._vr_texture  # ← 不调用 doneCurrent()！上下文保持 current

# manager.py — _render_overlay 中
texture = self._renderer.render_widget(self._vr_panel)
self._overlay.setOverlayTexture(self._handle, texture)  # 需要上下文 current
self._renderer.finish()  # ← 在 setOverlayTexture 之后才释放上下文
```

**`setOverlayTexture` 内部调用 `glBindTexture`，必须在 GL 上下文 current 时调用。**

### 2.3 show/hide 同步 MakeOverlaysInteractiveIfVisible

```python
def show(self):
    overlay.setOverlayFlag(handle, VROverlayFlags_MakeOverlaysInteractiveIfVisible, True)
    overlay.showOverlay(handle)

def hide(self):
    overlay.setOverlayFlag(handle, VROverlayFlags_MakeOverlaysInteractiveIfVisible, False)
    overlay.hideOverlay(handle)
```

**不设置此 flag → 需要打开 SteamVR 面板才能交互。**
**在 `start()` 中也要设置此 flag，否则首次显示时无法交互。**

---

## 3. 致命陷阱（必须避免）

### 3.1 VREvent_t 数据路径

```python
# ❌ 错误 — 没有 event.mouse 属性
mouse = event_data.mouse

# ✅ 正确 — 鼠标数据在 .data 子结构下
mouse = event_data.data.mouse
scroll_y = event_data.data.scroll.ydelta
keyboard = event_data.data.keyboard.cNewInput
```

### 3.2 QPoint vs QPointF

```python
# mapFromGlobal() 返回 QPoint（不是 QPointF）
local_pos = target.mapFromGlobal(widget.mapToGlobal(pos.toPoint()))
# local_pos 是 QPoint，没有 .toPoint() 方法

# ❌ 错误
target.mapToGlobal(local_pos.toPoint())  # QPoint 没有 toPoint()

# ✅ 正确
target.mapToGlobal(local_pos)  # 直接用 QPoint
```

### 3.3 QWheelEvent 参数类型

```python
# ❌ 错误 — pixelDelta/angleDelta 必须是 QPoint
QWheelEvent(pos, globalPos, QPointF(0, 0), QPointF(0, delta), ...)

# ✅ 正确
QWheelEvent(pos, globalPos, QPoint(0, 0), QPoint(0, delta), ...)
```

### 3.4 PySide6 OpenGL 模块导入

```python
# ❌ 错误 — 这些类不在 QtGui 模块
from PySide6.QtGui import QOpenGLFramebufferObject
from PySide6.QtGui import QOpenGLPaintDevice

# ✅ 正确 — 在 QtOpenGL 模块
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtOpenGL import QOpenGLPaintDevice
```

### 3.5 FBO 不能直接作为 QPainter 目标

```python
# ❌ 错误 — PySide6 类型系统不兼容
painter = QPainter(self._fbo)  # TypeError

# ✅ 正确 — 用 QOpenGLPaintDevice 作为中间层
paint_device = QOpenGLPaintDevice(self._fbo.size())
painter = QPainter(paint_device)
painter.drawPixmap(0, 0, width, height, pixmap)
```

### 3.6 drawPixmap 高 DPI 缩放

```python
# ❌ 错误 — 高 DPI 屏幕上 pixmap 的 devicePixelRatio=2，只显示 1/4 面积
painter.drawPixmap(0, 0, pixmap)

# ✅ 正确 — 显式指定目标尺寸
painter.drawPixmap(0, 0, self.width, self.height, pixmap)
```

### 3.7 Y 轴坐标系

**当前实现**：不使用 `setPaintFlipped(True)`，纹理用 Qt 坐标系（Y=0 在顶部）。坐标映射不翻转 Y 轴：

```python
# input_handler.py — _to_widget_pos
wx = vr_x / self.texture_width * ww
wy = vr_y / self.texture_height * wh  # 直接映射，不翻转
```

如果使用 `setPaintFlipped(True)`（纹理用 OpenGL 坐标系），则需要翻转 Y：

```python
wy = (1.0 - vr_y / self.texture_height) * wh  # 翻转 Y
```

**两种方案二选一，不能混用。**

---

## 4. 渲染器实现

### 4.1 GLOverlayRenderer（gl_renderer.py）— 推荐

```python
class GLOverlayRenderer:
    def __init__(self, width, height):
        # GL 上下文 + 离屏表面
        self._surface = QOffscreenSurface()
        self._surface.create()
        self._context = QOpenGLContext()
        self._context.create()

        # FBO（包含一个 GL 纹理，ID 固定）
        self._context.makeCurrent(self._surface)
        self._fbo = QOpenGLFramebufferObject(QSize(width, height))
        self._context.doneCurrent()

        # OpenVR 纹理结构（只创建一次）
        self._vr_texture = openvr.Texture_t()
        self._vr_texture.handle = self._fbo.texture()  # GLuint
        self._vr_texture.eType = openvr.TextureType_OpenGL
        self._vr_texture.eColorSpace = openvr.ColorSpace_Gamma

    def render_widget(self, widget):
        self._context.makeCurrent(self._surface)
        self._fbo.bind()
        paint_device = QOpenGLPaintDevice(self._fbo.size())
        painter = QPainter(paint_device)
        pixmap = widget.grab()
        painter.drawPixmap(0, 0, self.width, self.height, pixmap)
        painter.end()
        self._fbo.release()
        # 不调用 doneCurrent()！
        return self._vr_texture

    def finish(self):
        self._context.doneCurrent()  # 在 setOverlayTexture 之后调用
```

### 4.2 OverlayRenderer（renderer.py）— 备用（有闪烁）

```python
class OverlayRenderer:
    def __init__(self, width, height):
        self._buf = ctypes.create_string_buffer(width * height * 4)
        self._last_hash = None

    def render_widget(self, widget):
        # widget.grab() → QPixmap → QImage → ctypes buffer
        # 通过哈希比较检测内容变化
        # 返回 (buf, w, h) 或 (None, 0, 0)
```

---

## 5. 输入处理

### 5.1 事件分发到子 widget

```python
def _resolve_target(self, widget, pos):
    child = widget.childAt(pos.toPoint())
    return child if child is not None else widget

def _handle_mouse_button(self, pos, widget, pressed):
    target = self._resolve_target(widget, pos)
    local_pos = target.mapFromGlobal(widget.mapToGlobal(pos.toPoint()))
    event = QMouseEvent(event_type, local_pos, target.mapToGlobal(local_pos), ...)
    QApplication.sendEvent(target, event)  # 发送到子 widget，不是父 widget
```

### 5.2 坐标映射

```python
def _to_widget_pos(self, event_data, widget):
    mouse = event_data.data.mouse  # 注意：.data.mouse
    vr_x = mouse.x
    vr_y = mouse.y
    ww = widget.width()
    wh = widget.height()
    wx = vr_x / self.texture_width * ww
    wy = vr_y / self.texture_height * wh  # 不翻转（无 setPaintFlipped）
    return QPointF(wx, wy)
```

### 5.3 事件类型

| ID | 名称 | 处理 |
|----|------|------|
| 300 | MouseMove | 转发 QMouseEvent(MouseMove) + 更新准星 |
| 301 | MouseDown | 转发 QMouseEvent(MouseButtonPress) |
| 302 | MouseUp | 转发 QMouseEvent(MouseButtonRelease) |
| 303 | FocusEnter | 仅通知 widget |
| 304 | FocusLeave | 仅通知 widget |
| 305 | ScrollDiscrete | 转发 QWheelEvent |
| 108, 500, 501, 508, 1707 | 各种 | **忽略**（_IGNORE_EVENTS） |

---

## 6. 配置参数

```json
{
    "vr_overlay": {
        "enabled": false,
        "width_meters": 1.5,
        "position_mode": "hmd",
        "distance": 2.0,
        "texture_width": 960,
        "texture_height": 540
    }
}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enabled` | `false` | 启动时自动创建覆盖层 |
| `width_meters` | `1.5` | 覆盖层物理宽度（米） |
| `position_mode` | `hmd` | 定位：`hmd` / `controller` / `world` |
| `distance` | `2.0` | 距离参考设备（米） |
| `texture_width` | `960` | 纹理像素宽度 |
| `texture_height` | `540` | 纹理像素高度 |

---

## 7. 定位矩阵

```python
m = openvr.HmdMatrix34_t()
m.m[0][0] = 1;  m.m[0][1] = 0;  m.m[0][2] = 0;  m.m[0][3] = 0
m.m[1][0] = 0;  m.m[1][1] = 1;  m.m[1][2] = 0;  m.m[1][3] = 0.3   # 上方 0.3m
m.m[2][0] = 0;  m.m[2][1] = 0;  m.m[2][2] = 1;  m.m[2][3] = -dist # 前方 dist 米
overlay.setOverlayTransformTrackedDeviceRelative(handle, device_idx, m)
```

---

## 8. 调试技巧

### 检查 SteamVR 是否运行

```python
import openvr
try:
    openvr.init(openvr.VRApplication_Overlay)
    print("SteamVR 运行中")
    openvr.shutdown()
except Exception as e:
    print(f"SteamVR 不可用: {e}")
```

### 检查覆盖层状态

```python
visible = overlay.isOverlayVisible(handle)
input_method = overlay.getOverlayInputMethod(handle)
print(f"visible={visible}, input={input_method}")  # 1=可见, input=1=鼠标
```

### 检查 FBO 纹理 ID

```python
renderer = GLOverlayRenderer(960, 540)
print(f"texture_id={renderer._fbo.texture()}")  # 应为正整数
```

### 检查 GL 上下文

```python
print(f"context valid={renderer._context.isValid()}")
print(f"surface valid={renderer._surface.isValid()}")
print(f"FBO valid={renderer._fbo.isValid()}")
```
