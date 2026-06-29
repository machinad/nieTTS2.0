import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)


class ConfigNotifier:
    """配置变更通知器，与 ConfigManager 解耦。

    调用方在 config.update() 成功后调用 notify(source)，
    注册方通过 on_change(callback, listen_source) 监听对端变更。

    source 约定:
      - "gui"    : 变更来自 GUI
      - "webui"  : 变更来自 WebUI
      - None     : 来源未知
    """

    def __init__(self):
        self._listeners: list[tuple[Callable, str | None]] = []

    def on_change(self, callback: Callable, source: str | None = None):
        """注册监听。source=None 监听所有来源，source="gui" 只监听 GUI 变更"""
        self._listeners.append((callback, source))

    def remove_listener(self, callback: Callable):
        """移除指定回调的所有注册"""
        self._listeners = [(cb, s) for cb, s in self._listeners if cb is not callback]

    def notify(self, source: str | None = None):
        """通知所有关心该 source 的监听者"""
        for cb, listen_source in self._listeners:
            if listen_source is None or listen_source == source:
                try:
                    cb(source)
                except Exception as e:
                    logger.error("配置通知回调失败: %s", e)
