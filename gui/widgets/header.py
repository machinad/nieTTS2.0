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
