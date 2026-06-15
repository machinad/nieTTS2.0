from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer


def svg_icon(svg_data: bytes, color: str = "#6b6a68", size: int = 20) -> QIcon:
    """Render SVG bytes to a QIcon with the given color."""
    svg = svg_data.replace(b"currentColor", color.encode())
    renderer = QSvgRenderer(QByteArray(svg))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)
