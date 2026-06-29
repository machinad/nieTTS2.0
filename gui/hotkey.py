import ctypes
import ctypes.wintypes
import logging

from PySide6.QtCore import (
    QAbstractNativeEventFilter,
    QMetaObject,
    QObject,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QPushButton

logger = logging.getLogger(__name__)

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

user32.RegisterHotKey.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
user32.RegisterHotKey.restype = ctypes.c_int
user32.UnregisterHotKey.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
user32.UnregisterHotKey.restype = ctypes.c_int

WM_HOTKEY = 0x0312

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004

_QT_KEY_NAMES = {
    Qt.Key.Key_Space: "Space",
    Qt.Key.Key_Tab: "Tab",
    Qt.Key.Key_Return: "Enter",
    Qt.Key.Key_Enter: "Enter",
    Qt.Key.Key_Escape: "Esc",
    Qt.Key.Key_Backspace: "Backspace",
    Qt.Key.Key_Delete: "Delete",
    Qt.Key.Key_Insert: "Insert",
    Qt.Key.Key_Home: "Home",
    Qt.Key.Key_End: "End",
    Qt.Key.Key_PageUp: "PageUp",
    Qt.Key.Key_PageDown: "PageDown",
    Qt.Key.Key_Up: "Up",
    Qt.Key.Key_Down: "Down",
    Qt.Key.Key_Left: "Left",
    Qt.Key.Key_Right: "Right",
    Qt.Key.Key_F1: "F1",
    Qt.Key.Key_F2: "F2",
    Qt.Key.Key_F3: "F3",
    Qt.Key.Key_F4: "F4",
    Qt.Key.Key_F5: "F5",
    Qt.Key.Key_F6: "F6",
    Qt.Key.Key_F7: "F7",
    Qt.Key.Key_F8: "F8",
    Qt.Key.Key_F9: "F9",
    Qt.Key.Key_F10: "F10",
    Qt.Key.Key_F11: "F11",
    Qt.Key.Key_F12: "F12",
}


def _qt_key_to_display(key: int) -> str:
    if key in _QT_KEY_NAMES:
        return _QT_KEY_NAMES[key]
    if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
        return chr(key - Qt.Key.Key_A + ord("A"))
    if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
        return chr(key - Qt.Key.Key_0 + ord("0"))
    return f"0x{key:02X}"


def build_display(ctrl: bool, shift: bool, alt: bool, qt_key: int) -> str:
    parts = []
    if ctrl:
        parts.append("Ctrl")
    if shift:
        parts.append("Shift")
    if alt:
        parts.append("Alt")
    if qt_key > 0:
        parts.append(_qt_key_to_display(qt_key))
    return "+".join(parts)


class _NativeHotkeyFilter(QAbstractNativeEventFilter):
    """Intercepts WM_HOTKEY messages in Qt's main-thread message pump."""

    def __init__(self, manager: GlobalHotkeyManager):
        super().__init__()
        self._manager = manager

    def nativeEventFilter(self, eventType, message):
        if eventType == b"windows_generic_MSG":
            addr = int(message)
            if addr:
                try:
                    msg = ctypes.cast(addr, ctypes.POINTER(ctypes.wintypes.MSG)).contents
                    if msg.message == WM_HOTKEY:
                        logger.debug("nativeEventFilter 捕获 WM_HOTKEY, wParam=%d", msg.wParam)
                        QMetaObject.invokeMethod(
                            self._manager,
                            "hotkey_pressed",
                            Qt.ConnectionType.QueuedConnection,
                        )
                except Exception:
                    logger.debug("WM_HOTKEY 处理异常", exc_info=True)
        return (False, 0)


class GlobalHotkeyManager(QObject):
    """Win32 global hotkey via RegisterHotKey + QAbstractNativeEventFilter."""

    hotkey_pressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hotkey_id = 1
        self._registered = False
        self._current_cfg: dict = {}
        self._filter: _NativeHotkeyFilter | None = None

    def install_filter(self):
        """Install the native event filter on QApplication. Call once at startup."""
        if self._filter is None:
            self._filter = _NativeHotkeyFilter(self)
            app = QApplication.instance()
            if app:
                app.installNativeEventFilter(self._filter)
                logger.info("WM_HOTKEY 原生事件过滤器已安装")

    def register(self, ctrl: bool, shift: bool, alt: bool, key_vk: int) -> tuple[bool, str]:
        self.unregister()

        mod_flags = 0
        if alt:
            mod_flags |= MOD_ALT
        if ctrl:
            mod_flags |= MOD_CONTROL
        if shift:
            mod_flags |= MOD_SHIFT

        logger.info(
            "正在注册全局热键: ctrl=%s shift=%s alt=%s vk=0x%02X mod=0x%02X", ctrl, shift, alt, key_vk, mod_flags
        )
        result = user32.RegisterHotKey(None, self._hotkey_id, mod_flags, key_vk)
        if result == 0:
            err = kernel32.GetLastError()
            logger.error(
                "RegisterHotKey 失败: ctrl=%s shift=%s alt=%s vk=0x%02X, error=%d，热键可能被其他程序占用",
                ctrl,
                shift,
                alt,
                key_vk,
                err,
            )
            return False, f"RegisterHotKey 失败 (错误码 {err})，热键可能被其他程序占用"

        self._registered = True
        self._current_cfg = {
            "ctrl": ctrl,
            "shift": shift,
            "alt": alt,
            "key": key_vk,
        }
        logger.info("全局热键已注册: ctrl=%s shift=%s alt=%s vk=0x%02X", ctrl, shift, alt, key_vk)
        return True, ""

    def unregister(self):
        if self._registered:
            if not user32.UnregisterHotKey(None, self._hotkey_id):
                logger.warning("UnregisterHotKey 失败, error=%d", kernel32.GetLastError())
            self._registered = False
            logger.info("全局热键已注销")

    def update_hotkey(self, cfg: dict) -> tuple[bool, str]:
        combo_keys = ("ctrl", "shift", "alt", "key")
        new_combo = {k: cfg.get(k) for k in combo_keys}
        old_combo = {k: self._current_cfg.get(k) for k in combo_keys}
        if new_combo == old_combo and self._registered:
            return True, ""
        ctrl = cfg.get("ctrl", True)
        shift = cfg.get("shift", False)
        alt = cfg.get("alt", False)
        key_vk = cfg.get("key", 0)
        if not key_vk:
            return False, "无效的按键配置"
        return self.register(ctrl, shift, alt, key_vk)

    def get_display_text(self) -> str:
        if not self._current_cfg:
            return "未设置"
        return self._current_cfg.get("display", "未设置")

    def close(self):
        self.unregister()
        if self._filter is not None:
            app = QApplication.instance()
            if app:
                app.removeNativeEventFilter(self._filter)
            self._filter = None


class HotkeyRecordButton(QPushButton):
    """Button that enters recording mode to capture a hotkey combination."""

    hotkey_recorded = Signal(dict)
    recording_started = Signal()
    recording_cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._recording = False
        self._ctrl = False
        self._shift = False
        self._alt = False
        self._key_vk = 0
        self._key_qt = 0
        self._has_non_modifier = False
        self._saved_text = ""

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(36)
        self.setMinimumWidth(160)
        self._update_style_normal()
        self.clicked.connect(self._on_click)

    def set_display(self, text: str):
        self.setText(text)

    def start_recording(self):
        self._recording = True
        self._saved_text = self.text()
        self._ctrl = False
        self._shift = False
        self._alt = False
        self._key_vk = 0
        self._key_qt = 0
        self._has_non_modifier = False
        self.setText("请按下快捷键...")
        self._update_style_recording()
        self.setFocus()
        self.grabKeyboard()
        self.recording_started.emit()

    def cancel_recording(self):
        self._recording = False
        self._has_non_modifier = False
        self.releaseKeyboard()
        self.setText(self._saved_text)
        self._update_style_normal()
        self.recording_cancelled.emit()

    def _on_click(self):
        if not self._recording:
            self.start_recording()

    def keyPressEvent(self, event: QKeyEvent):
        if not self._recording:
            super().keyPressEvent(event)
            return

        key = event.key()
        vk = event.nativeVirtualKey()

        if key == Qt.Key.Key_Escape:
            self.cancel_recording()
            return

        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            self._ctrl = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
            self._shift = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
            self._alt = bool(event.modifiers() & Qt.KeyboardModifier.AltModifier)
            display = build_display(self._ctrl, self._shift, self._alt, 0)
            self.setText(f"{display}+..." if display else "请按下快捷键...")
            return

        self._ctrl = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
        self._shift = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        self._alt = bool(event.modifiers() & Qt.KeyboardModifier.AltModifier)
        self._key_qt = key
        self._key_vk = vk
        self._has_non_modifier = True

        display = build_display(self._ctrl, self._shift, self._alt, self._key_qt)
        self.setText(display)

    def keyReleaseEvent(self, event: QKeyEvent):
        if not self._recording:
            super().keyReleaseEvent(event)
            return

        key = event.key()
        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            if self._has_non_modifier and self._key_vk:
                self._finish_recording()
                return

    def _finish_recording(self):
        self._recording = False
        self._has_non_modifier = False
        self.releaseKeyboard()
        self._update_style_normal()

        if self._key_vk:
            display = build_display(self._ctrl, self._shift, self._alt, self._key_qt)
            self.setText(display)
            self.hotkey_recorded.emit(
                {
                    "ctrl": self._ctrl,
                    "shift": self._shift,
                    "alt": self._alt,
                    "key": self._key_vk,
                    "display": display,
                }
            )
            logger.info("快捷键录制完成: %s", display)
        else:
            self.cancel_recording()

    def focusOutEvent(self, event):
        if self._recording:
            QTimer.singleShot(50, self._check_focus_on_blur)
        super().focusOutEvent(event)

    def _check_focus_on_blur(self):
        if self._recording and not self.hasFocus():
            self.cancel_recording()

    def _update_style_normal(self):
        self.setStyleSheet(
            "QPushButton {"
            "  background: #ffffff;"
            "  border: 1px solid rgba(0, 0, 0, 0.08);"
            "  border-radius: 8px;"
            "  padding: 6px 14px;"
            "  font-size: 14px;"
            "  color: #1a1a1a;"
            "  font-family: 'Consolas', 'JetBrains Mono', monospace;"
            "}"
            "QPushButton:hover {"
            "  border-color: rgba(0, 0, 0, 0.14);"
            "  background: #f0eeeb;"
            "}"
        )

    def _update_style_recording(self):
        self.setStyleSheet(
            "QPushButton {"
            "  background: rgba(214, 96, 138, 0.1);"
            "  border: 2px solid #d6608a;"
            "  border-radius: 8px;"
            "  padding: 6px 14px;"
            "  font-size: 14px;"
            "  color: #d6608a;"
            "  font-family: 'Consolas', 'JetBrains Mono', monospace;"
            "}"
        )
