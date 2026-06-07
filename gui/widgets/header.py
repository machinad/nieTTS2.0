from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel


class Header(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("header")
        self.setFixedHeight(56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)

        self._title = QLabel("nieTTS 2.0")
        self._title.setObjectName("header_title")
        layout.addWidget(self._title)

        layout.addStretch()

        self._status_frame = QFrame()
        self._status_frame.setObjectName("status_disconnected")
        status_layout = QHBoxLayout(self._status_frame)
        status_layout.setContentsMargins(14, 4, 14, 4)
        status_layout.setSpacing(8)
        self._status_dot = QLabel()
        self._status_dot.setFixedSize(8, 8)
        self._status_dot.setStyleSheet(
            "background: #d04840; border-radius: 4px; border: none;"
        )
        status_layout.addWidget(self._status_dot)
        self._status_label = QLabel("已断开")
        self._status_label.setStyleSheet(
            "font-size: 13px; color: #d04840; border: none;"
        )
        status_layout.addWidget(self._status_label)
        layout.addWidget(self._status_frame)

    def set_connected(self, connected: bool):
        if connected:
            self._status_frame.setObjectName("status_connected")
            self._status_dot.setStyleSheet(
                "background: #3da85c; border-radius: 4px; border: none;"
            )
            self._status_label.setText("已连接")
            self._status_label.setStyleSheet(
                "font-size: 13px; color: #3da85c; border: none;"
            )
        else:
            self._status_frame.setObjectName("status_disconnected")
            self._status_dot.setStyleSheet(
                "background: #d04840; border-radius: 4px; border: none;"
            )
            self._status_label.setText("已断开")
            self._status_label.setStyleSheet(
                "font-size: 13px; color: #d04840; border: none;"
            )
        self._status_frame.style().unpolish(self._status_frame)
        self._status_frame.style().polish(self._status_frame)
