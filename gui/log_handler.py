import logging

from PySide6.QtCore import QObject, Signal


class QtLogHandler(logging.Handler, QObject):
    log_received = Signal(str, str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)
        self._enabled = True

    def disable(self):
        self._enabled = False

    def emit(self, record: logging.LogRecord):
        if not self._enabled:
            return
        try:
            level = record.levelname.lower()
            if level == "warning":
                level = "warn"
            message = f"[{record.name}] {record.getMessage()}"
            self.log_received.emit(level, message)
        except RuntimeError:
            self._enabled = False
        except Exception:
            self.handleError(record)
