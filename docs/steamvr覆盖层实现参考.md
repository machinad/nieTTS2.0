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
VREvent_t (MouseMove=300, MouseDown=301, MouseUp=302)
     ↓ pollNextOverlayEvent() 每帧轮询（60Hz）
input_handler._vr_to_widget_pos() → VR 纹理坐标 → widget 坐标（缩放）
     ↓ _resolve_target() → childAt(pos) 找到子 widget (按钮等)
QApplication.sendEvent(target, QMouseEvent) → 转发到子 widget
     ↓ mark_dirty() → 触发 VR 纹理重渲染
```

### 1.3 异步架构（60Hz 协程主循环）

```
asyncio.create_task(manager.run(widget, config))
     │
     ├── asyncio.to_thread(_init_openvr_blocking)  ← 子线程：所有阻塞 OpenVR C FFI 调用
     │     import openvr / isHmdPresent / init / createOverlay / setOverlay* / showOverlay
     │
     ├── _setup_qt_components()                     ← 主线程：QOpenGLContext / QWidget 必须主线程
     │     VROverlayRenderer / VRCrosshairOverlay / VRInputHandler
     │
     └── 60Hz while 循环
           ├── _pump_events()          轮询 OpenVR 事件
           ├── _render_and_submit()    按需渲染（_dirty 标记）
           └── await asyncio.sleep()   精确休眠到下一帧（单调时钟）

await manager.stop()  ← 异步关闭：取消循环 → 清理 Qt 对象 → asyncio.to_thread(cleanup OpenVR)
```

**为什么用 async 而不是 QTimer**：
- `asyncio.to_thread` 将阻塞的 OpenVR 初始化移到子线程，GUI 不卡死
- `asyncio.sleep` 精确控制 60Hz 帧率（单调时钟）
- 自然集成 qasync 事件循环，与 Qt GUI 共享主线程

### 1.4 文件结构

```
gui/vr_overlay/
├── __init__.py          # 导出所有公共类
├── manager.py           # OpenVR 生命周期、async 主循环、事件轮询、纹理提交
├── renderer.py          # FBO 渲染器（GL 上下文 + QOpenGLPaintDevice）
├── input_handler.py     # VR 事件 → Qt 事件转换 + 坐标缩放
├── crosshair.py         # 准星叠加层（独立 QWidget，鼠标事件穿透）
└── test_widget.py       # 测试 UI（按钮、滑块、状态显示）
```

---

## 2. 关键实现细节

### 2.1 两阶段初始化（致命陷阱：必须分线程）

```python
# manager.py — _init_openvr()

# 阶段 1：子线程执行所有阻塞的 OpenVR C FFI 调用
ok = await asyncio.to_thread(self._init_openvr_blocking)

# 阶段 2：主线程创建 Qt 对象（QWidget/QOpenGLContext 必须主线程）
self._setup_qt_components()
```

**`_init_openvr_blocking()`（子线程）包含**：
1. `import openvr` — 加载 C 扩展
2. `isHmdPresent()` / `isRuntimeInstalled()` — 检查 SteamVR
3. `openvr.init(VRApplication_Overlay)` — 初始化 OpenVR 运行时
4. `VROverlay()` + `createOverlay()` — 创建覆盖层
5. `setOverlayWidthInMeters` / `setOverlayAlpha` — 设置参数
6. `setOverlayTransformTrackedDeviceRelative` — 定位
7. `showOverlay` — 显示
8. `setOverlayInputMethod` / `setOverlayMouseScale` / `setOverlayFlag` — 启用输入

**`_setup_qt_components()`（主线程）包含**：
1. `VROverlayRenderer` + `init_gl()` — FBO + GL 上下文
2. `VRCrosshairOverlay` — 准星 QWidget
3. `VRInputHandler` — 事件处理器

**为什么必须分线程**：`openvr.init()` 等 C FFI 调用可能阻塞 3-10 秒（等待 SteamVR 响应）。如果在主线程执行，Qt 事件循环完全冻结，GUI 无响应。

### 2.2 OpenVR 初始化顺序（必须严格遵守）

```python
# _init_openvr_blocking() 中的顺序：

# 1. 初始化 OpenVR
ov = openvr
ov.init(ov.VRApplication_Overlay)

# 2. 获取 Overlay 接口
overlay = ov.VROverlay()

# 3. 创建覆盖层
handle = overlay.createOverlay("nietts_vr_overlay", "nieTTS 2.0 VR Overlay")

# 4. 设置覆盖层属性
overlay.setOverlayWidthInMeters(handle, 2.0)
overlay.setOverlayAlpha(handle, 0.9)

# 5. 定位
overlay.setOverlayTransformTrackedDeviceRelative(handle, k_unTrackedDeviceIndex_Hmd, matrix)

# 6. 显示覆盖层（必须在启用输入之前）
overlay.showOverlay(handle)

# 7. 启用输入（必须在 showOverlay 之后）
overlay.setOverlayInputMethod(handle, VROverlayInputMethod_Mouse)
overlay.setOverlayMouseScale(handle, HmdVector2_t(tex_w, tex_h))
overlay.setOverlayFlag(handle, VROverlayFlags_MakeOverlaysInteractiveIfVisible, True)
overlay.setOverlayFlag(handle, VROverlayFlags_SendVRDiscreteScrollEvents, True)
```

### 2.3 GL 上下文生命周期（致命陷阱）

```python
# renderer.py — render_widget 中
self._context.makeCurrent(self._surface)  # 激活上下文
self._fbo.bind()
# ... 渲染 ...
self._fbo.release()
return int(self._fbo.texture())  # ← 不调用 doneCurrent()！上下文保持 current

# manager.py — _render_and_submit 中
texture_id = self._renderer.render_widget(self._widget)
texture = self._renderer.get_texture_struct(texture_id)
self._vr_overlay.setOverlayTexture(self._overlay_handle, texture)  # 需要上下文 current
self._renderer.finish()  # ← 在 setOverlayTexture 之后才释放上下文
```

**`setOverlayTexture` 内部调用 `glBindTexture`，必须在 GL 上下文 current 时调用。**

### 2.4 pollNextOverlayEvent 返回值（致命陷阱）

```python
# ❌ 错误 — 返回值是元组，不是布尔值！永远为 True → 无限循环
while overlay.pollNextOverlayEvent(handle, event):
    ...

# ✅ 正确 — 解包元组，检查第一个元素
result, _ = overlay.pollNextOverlayEvent(handle, event)
while result:
    process(event)
    result, _ = overlay.pollNextOverlayEvent(handle, event)
```

**`pollNextOverlayEvent` 返回 `(int, VREvent_t)` 元组。直接 `while` 检查元组永远为 True（非空元组），导致无限循环冻结 GUI。**

### 2.5 mark_dirty 必须在每次 MouseMove 时调用

```python
# ❌ 错误 — 只在拖拽时标记脏，悬停时 VR 纹理不更新
if self._button_pressed:
    if self._manager:
        self._manager.mark_dirty()

# ✅ 正确 — 每次鼠标移动都标记脏
if self._manager:
    self._manager.mark_dirty()
```

**准星的 `update()` 只触发 Qt Widget 重绘，但 VR 纹理（FBO）不会重新提交给 OpenVR。必须调用 `mark_dirty()` 才会触发 `_render_and_submit()` 重新渲染纹理。**

### 2.6 show/hide 同步 MakeOverlaysInteractiveIfVisible

```python
def show(self):
    overlay.setOverlayFlag(handle, VROverlayFlags_MakeOverlaysInteractiveIfVisible, True)
    overlay.showOverlay(handle)

def hide(self):
    overlay.setOverlayFlag(handle, VROverlayFlags_MakeOverlaysInteractiveIfVisible, False)
    overlay.hideOverlay(handle)
```

**不设置此 flag → 需要打开 SteamVR 面板才能交互。**
**在 `_init_openvr_blocking` 中也要设置此 flag，否则首次显示时无法交互。**

### 2.7 准星叠加层

```python
# crosshair.py — VRCrosshairOverlay
class VRCrosshairOverlay(QWidget):
    def __init__(self, parent):
        # 关键属性：鼠标事件穿透 + 透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
```

**准星是独立 QWidget，覆盖在测试 UI 上方。`WA_TransparentForMouseEvents` 确保鼠标事件穿透到下层 Widget。**

### 2.8 坐标映射（VR 纹理坐标 → Widget 坐标）

```python
# input_handler.py — _vr_to_widget_pos
def _vr_to_widget_pos(self, vr_x, vr_y):
    ww = self._widget.width()    # 800
    wh = self._widget.height()   # 600
    # 纹理坐标 → widget 坐标（等比缩放 + 边界 clamp）
    wx = max(0.0, min(vr_x * ww / self._tex_w, ww - 1))
    wy = max(0.0, min(vr_y * wh / self._tex_h, wh - 1))
    return QPointF(wx, wy)
```

**OpenVR 的鼠标坐标基于纹理空间（1792×1208），不是 widget 空间（800×600）。必须乘以 `widget_size / texture_size` 缩放因子。**

### 2.9 Y 轴坐标系

**当前实现**：不使用 `setPaintFlipped(True)`，纹理用 Qt 坐标系（Y=0 在顶部）。坐标映射不翻转 Y 轴：

```python
wy = vr_y * wh / self._tex_h  # 直接映射，不翻转
```

如果使用 `setPaintFlipped(True)`（纹理用 OpenGL 坐标系），则需要翻转 Y：

```python
wy = (1.0 - vr_y / self._tex_h) * wh  # 翻转 Y
```

**两种方案二选一，不能混用。**

---

## 3. 致命陷阱（必须避免）

### 3.1 pollNextOverlayEvent 返回元组

```python
# ❌ 错误 — 元组永远为 True，无限循环
while overlay.pollNextOverlayEvent(handle, event):  # (int, VREvent_t) 永远 truthy

# ✅ 正确
result, _ = overlay.pollNextOverlayEvent(handle, event)
while result:
    ...
    result, _ = overlay.pollNextOverlayEvent(handle, event)
```

### 3.2 VREvent_t 数据路径

```python
# ❌ 错误 — 没有 event.mouse 属性
mouse = event_data.mouse

# ✅ 正确 — 鼠标数据在 .data 子结构下
mouse = event_data.data.mouse
scroll_y = event_data.data.scroll.ydelta
keyboard = event_data.data.keyboard.cNewInput
```

### 3.3 QPoint vs QPointF

```python
# mapFromGlobal() 返回 QPoint（不是 QPointF）
local_pos = target.mapFromGlobal(widget.mapToGlobal(pos.toPoint()))
# local_pos 是 QPoint，没有 .toPoint() 方法

# ❌ 错误
target.mapToGlobal(local_pos.toPoint())  # QPoint 没有 toPoint()

# ✅ 正确
target.mapToGlobal(local_pos)  # 直接用 QPoint
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

### 3.7 OpenVR 初始化必须在子线程

```python
# ❌ 错误 — 在 async 函数中直接调用，阻塞 Qt 事件循环
async def _init_openvr(self):
    openvr.init(...)  # 阻塞 3-10 秒，GUI 冻结
    await asyncio.sleep(0)  # 太晚了，上面已经阻塞

# ✅ 正确 — 用 asyncio.to_thread 移到子线程
async def _init_openvr(self):
    ok = await asyncio.to_thread(self._init_openvr_blocking)  # GUI 不受影响
```

### 3.8 mark_dirty 必须在 MouseMove 时调用

```python
# ❌ 错误 — 准星位置更新了但 VR 纹理不重渲染
self._crosshair.update_position(x, y)  # Qt Widget 重绘
# 没有 mark_dirty() → VR 纹理不变 → 准星在 VR 中不动

# ✅ 正确
self._crosshair.update_position(x, y)
if self._manager:
    self._manager.mark_dirty()  # 触发 VR 纹理重渲染
```

---

## 4. 渲染器实现（renderer.py）

### 4.1 VROverlayRenderer

```python
class VROverlayRenderer:
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
        return int(self._fbo.texture())

    def get_texture_struct(self, texture_id):
        """构造 OpenVR Texture_t 结构体。每帧重新创建。"""
        texture = openvr.Texture_t()
        texture.handle = texture_id
        texture.eType = openvr.TextureType_OpenGL
        texture.eColorSpace = openvr.ColorSpace_Gamma
        return texture

    def finish(self):
        self._context.doneCurrent()  # 在 setOverlayTexture 之后调用
```

---

## 5. 输入处理（input_handler.py）

### 5.1 事件分发到子 widget

```python
def _resolve_target(self, pos):
    child = self._widget.childAt(pos.toPoint())
    return child if child is not None else self._widget

def _send_event(self, pos, qt_event):
    target = self._resolve_target(pos)
    global_pos = self._widget.mapToGlobal(pos.toPoint())
    local_pos = target.mapFromGlobal(global_pos)
    event = QMouseEvent(qt_event.type(), QPointF(local_pos), global_pos, ...)
    QApplication.sendEvent(target, event)  # 发送到子 widget，不是父 widget
```

### 5.2 坐标映射（含缩放）

```python
def _vr_to_widget_pos(self, vr_x, vr_y):
    ww = self._widget.width()    # 800
    wh = self._widget.height()   # 600
    # 纹理坐标 → widget 坐标（等比缩放 + 边界 clamp）
    wx = max(0.0, min(vr_x * ww / self._tex_w, ww - 1))
    wy = max(0.0, min(vr_y * wh / self._tex_h, wh - 1))
    return QPointF(wx, wy)
```

### 5.3 事件类型

| ID | 名称 | 处理 |
|----|------|------|
| 300 | MouseMove | 转发 QMouseEvent(MouseMove) + 更新准星 + mark_dirty |
| 301 | MouseDown | 转发 QMouseEvent(MouseButtonPress) + mark_dirty |
| 302 | MouseUp | 转发 QMouseEvent(MouseButtonRelease) + mark_dirty |
| 303 | FocusEnter | 已加载常量，未实现处理 |
| 304 | FocusLeave | 已加载常量，未实现处理 |
| 305 | ScrollDiscrete | 已启用 flag，未实现处理 |
| 500 | OverlayShown | 日志记录 |
| 501 | OverlayHidden | 隐藏准星 |

### 5.4 VREvent 常量加载

```python
# 从 openvr 模块动态加载，不硬编码
def _load_vr_constants():
    import openvr
    _openvr_consts = {
        "MouseMove": openvr.VREvent_MouseMove,       # 300
        "MouseButtonDown": openvr.VREvent_MouseButtonDown,  # 301
        "MouseButtonUp": openvr.VREvent_MouseButtonUp,      # 302
        ...
    }
```

---

## 6. 配置参数

```json
{
    "vr_overlay": {
        "enabled": true,
        "width_meters": 2.0,
        "texture_width": 1792,
        "texture_height": 1208,
        "distance_meters": 1.5,
        "vertical_offset": -0.1,
        "alpha": 0.9
    }
}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enabled` | `true` | 启动时自动创建覆盖层 |
| `width_meters` | `2.0` | 覆盖层物理宽度（米） |
| `texture_width` | `1792` | 纹理像素宽度 |
| `texture_height` | `1208` | 纹理像素高度 |
| `distance_meters` | `1.5` | 距离 HMD（米） |
| `vertical_offset` | `-0.1` | 垂直偏移（负值=向下） |
| `alpha` | `0.9` | 覆盖层透明度 |

---

## 7. 定位矩阵

```python
# HmdMatrix34_t 是 3x4 行主序矩阵
m = openvr.HmdMatrix34_t()
m.m[0][0] = 1;  m.m[0][1] = 0;  m.m[0][2] = 0;  m.m[0][3] = 0        # X: 居中
m.m[1][0] = 0;  m.m[1][1] = 1;  m.m[1][2] = 0;  m.m[1][3] = -0.1     # Y: 向下 0.1m
m.m[2][0] = 0;  m.m[2][1] = 0;  m.m[2][2] = 1;  m.m[2][3] = -1.5     # Z: 向前 1.5m
overlay.setOverlayTransformTrackedDeviceRelative(handle, k_unTrackedDeviceIndex_Hmd, m)
```

---

## 8. 调试

### 8.1 启用 Debug 日志

```bash
# 开发模式
uv run gui_main.py --debug
uv run main.py --debug

# 打包后
nieTTS.exe --debug
```

`--debug` 将根日志级别设为 `DEBUG`，输出所有 VR 事件和坐标信息。

### 8.2 关键日志

```
# OpenVR 初始化
VR 覆盖层配置已加载: {...}
SteamVR 预检查通过
OpenVR 初始化成功（覆盖层模式）
覆盖层创建成功, handle=...
VR 覆盖层主循环启动 (60Hz)

# 事件轮询（--debug 模式）
VR事件: type=300 device=1        ← MouseMove
MouseMove: vr=(1060.3, 439.1)    ← VR 纹理坐标

# 纹理渲染
FBO 渲染器初始化成功: 1792x1208, texture=...
```

### 8.3 检查 SteamVR 是否运行

```python
import openvr
try:
    openvr.init(openvr.VRApplication_Overlay)
    print("SteamVR 运行中")
    openvr.shutdown()
except Exception as e:
    print(f"SteamVR 不可用: {e}")
```

### 8.4 检查覆盖层状态

```python
visible = overlay.isOverlayVisible(handle)
input_method = overlay.getOverlayInputMethod(handle)
print(f"visible={visible}, input={input_method}")  # 1=可见, input=1=鼠标
```

### 8.5 检查 FBO 纹理 ID

```python
renderer = VROverlayRenderer(1792, 1208)
renderer.init_gl()
print(f"texture_id={renderer._fbo.texture()}")  # 应为正整数
```

### 8.6 检查 GL 上下文

```python
print(f"context valid={renderer._context.isValid()}")
print(f"surface valid={renderer._surface.isValid()}")
print(f"FBO valid={renderer._fbo.isValid()}")
```

---

## 9. 已知限制（技术验证阶段）

以下功能已注册/启用但未实现处理：

| 功能 | 状态 | 说明 |
|------|------|------|
| 滚轮事件 (ScrollDiscrete=305) | flag 已启用，未处理 | 滑块/滚轮无法 VR 操作 |
| FocusEnter/FocusLeave (303/304) | 常量已加载，未处理 | 无 hover 进入/离开事件 |
| 右键/中键 | 未实现 | 所有按钮映射为左键 |
| 运行时配置更新 | 未实现 | `set_config()` 在 `run()` 之后无效 |
| widget 自身重绘检测 | 未实现 | QTimer/动画触发的重绘不自动同步到 VR |
