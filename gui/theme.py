from PySide6.QtWidgets import QApplication

# Design tokens mapped from frontend/src/styles/global.css
QSS = """
/* ================================================================
   nieTTS 2.0 — Pure QSS theme (mirrors Vue 3 frontend design)
   ================================================================ */

/* ---- Global ---- */
* {
    font-family: "Microsoft YaHei", "DM Sans", "Noto Sans SC", sans-serif;
}

QMainWindow {
    background-color: #f5f3f0;
}

QWidget {
    background-color: #f5f3f0;
    color: #1a1a1a;
    font-size: 14px;
}

/* ---- Sidebar ---- */
QFrame#sidebar {
    background-color: #ffffff;
    border-right: 1px solid rgba(0, 0, 0, 0.06);
}

QPushButton#nav_btn {
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: left;
    font-size: 14px;
    color: #6b6a68;
    background: transparent;
}
QPushButton#nav_btn:hover {
    background: rgba(0, 0, 0, 0.03);
    color: #1a1a1a;
}
QPushButton#nav_btn[active="true"] {
    background: rgba(214, 96, 138, 0.1);
    color: #d6608a;
    font-weight: 600;
}

/* ---- Header ---- */
QFrame#header {
    background-color: #ffffff;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
QLabel#header_title {
    font-size: 16px;
    font-weight: 600;
    color: #1a1a1a;
}

/* ---- Cards ---- */
QFrame[class="card"] {
    background-color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.04);
    border-radius: 14px;
}

/* ---- Page titles ---- */
QLabel#page_title {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a1a;
}

/* ---- Description box ---- */
QLabel[class="desc_box"] {
    color: #6b6a68;
    font-size: 13px;
    padding: 12px 16px;
    background: #ffffff;
    border-radius: 10px;
    border-left: 3px solid #d6608a;
}

/* ---- Section title ---- */
QLabel[class="section_title"] {
    font-size: 12px;
    font-weight: 600;
    color: #9b9a98;
}

/* ---- Field label ---- */
QLabel[class="field_label"] {
    font-size: 12px;
    font-weight: 600;
    color: #9b9a98;
}

/* ---- Primary button ---- */
QPushButton#primary_btn {
    background-color: #d6608a;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 600;
}
QPushButton#primary_btn:hover {
    background-color: #c44e7a;
}
QPushButton#primary_btn:pressed {
    background-color: #b34070;
}
QPushButton#primary_btn:disabled {
    background-color: #c5c4c2;
    color: #ffffff;
}

/* ---- Secondary button ---- */
QPushButton#secondary_btn {
    background-color: #ffffff;
    color: #6b6a68;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 600;
}
QPushButton#secondary_btn:hover {
    background-color: #f0eeeb;
    border-color: rgba(0, 0, 0, 0.14);
    color: #1a1a1a;
}
QPushButton#secondary_btn:pressed {
    background-color: #e8e6e3;
}

/* ---- Danger button ---- */
QPushButton#danger_btn {
    background-color: #d04840;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 600;
}
QPushButton#danger_btn:hover {
    background-color: #c04440;
}
QPushButton#danger_btn:pressed {
    background-color: #b0403c;
}

/* ---- Status badge ---- */
QFrame#status_connected {
    background: rgba(61, 168, 92, 0.08);
    border: 1px solid rgba(61, 168, 92, 0.2);
    border-radius: 100px;
    padding: 6px 14px;
}
QFrame#status_disconnected {
    background: rgba(208, 72, 64, 0.08);
    border: 1px solid rgba(208, 72, 64, 0.2);
    border-radius: 100px;
    padding: 6px 14px;
}

/* ---- Log terminal ---- */
QPlainTextEdit#log_terminal {
    background-color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.04);
    border-radius: 14px;
    padding: 12px;
    font-family: "JetBrains Mono", "Fira Code", "Consolas", monospace;
    font-size: 13px;
    color: #6b6a68;
}

/* ---- Filter button ---- */
QPushButton#filter_btn {
    border: 1px solid rgba(0, 0, 0, 0.04);
    border-radius: 10px;
    padding: 7px 12px;
    font-size: 13px;
    font-weight: 500;
    color: #6b6a68;
    background: #ffffff;
}
QPushButton#filter_btn:hover {
    border-color: rgba(0, 0, 0, 0.08);
    background: #f0eeeb;
}
QPushButton#filter_btn[active="true"] {
    border-color: #d6608a;
    background: rgba(214, 96, 138, 0.1);
    color: #d6608a;
}

/* ---- Toggle row ---- */
QFrame[class="toggle_row"] {
    border-bottom: 1px solid rgba(0, 0, 0, 0.04);
    padding: 10px 0;
}

/* ---- Tab widget ---- */
QTabWidget::pane {
    border: none;
    background: transparent;
}
QTabBar {
    background: transparent;
}
QTabBar::tab {
    background: transparent;
    color: #6b6a68;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:hover {
    color: #1a1a1a;
}
QTabBar::tab:selected {
    color: #d6608a;
    border-bottom: 2px solid #d6608a;
}

/* ---- Combo box ---- */
QComboBox {
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 8px 12px;
    background: #ffffff;
    color: #1a1a1a;
    font-size: 14px;
    min-height: 20px;
}
QComboBox:hover {
    border-color: rgba(0, 0, 0, 0.14);
}
QComboBox:focus {
    border-color: #d6608a;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
    subcontrol-position: center right;
}
QComboBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6b6a68;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background: #ffffff;
    color: #1a1a1a;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    selection-background-color: rgba(214, 96, 138, 0.1);
    selection-color: #d6608a;
    outline: none;
    padding: 4px;
}
QComboBox QAbstractItemView::item {
    color: #1a1a1a;
    padding: 6px 12px;
    min-height: 28px;
}
QComboBox QAbstractItemView::item:selected {
    background: rgba(214, 96, 138, 0.1);
    color: #d6608a;
}

/* ---- Line edit ---- */
QLineEdit {
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 8px 12px;
    background: #ffffff;
    color: #1a1a1a;
    font-size: 14px;
    selection-background-color: rgba(214, 96, 138, 0.2);
}
QLineEdit:hover {
    border-color: rgba(0, 0, 0, 0.14);
}
QLineEdit:focus {
    border-color: #d6608a;
}

/* ---- Spin box ---- */
QDoubleSpinBox, QSpinBox {
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 8px 12px;
    background: #ffffff;
    color: #1a1a1a;
    font-size: 14px;
}
QDoubleSpinBox:hover, QSpinBox:hover {
    border-color: rgba(0, 0, 0, 0.14);
}
QDoubleSpinBox:focus, QSpinBox:focus {
    border-color: #d6608a;
}
QDoubleSpinBox::up-button, QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border: none;
    border-left: 1px solid rgba(0, 0, 0, 0.06);
    border-top-right-radius: 10px;
    background: transparent;
}
QDoubleSpinBox::down-button, QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border: none;
    border-left: 1px solid rgba(0, 0, 0, 0.06);
    border-bottom-right-radius: 10px;
    background: transparent;
}
QDoubleSpinBox::up-arrow, QSpinBox::up-arrow {
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid #6b6a68;
}
QDoubleSpinBox::down-arrow, QSpinBox::down-arrow {
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #6b6a68;
}

/* ---- Plain text edit ---- */
QPlainTextEdit {
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 16px;
    background: #ffffff;
    color: #1a1a1a;
    font-size: 15px;
    font-family: "Microsoft YaHei", "DM Sans", sans-serif;
    selection-background-color: rgba(214, 96, 138, 0.2);
}
QPlainTextEdit:focus {
    border-color: #d6608a;
}

/* ---- Text browser ---- */
QTextBrowser {
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 16px;
    background: #ffffff;
    color: #1a1a1a;
    font-size: 14px;
    selection-background-color: rgba(214, 96, 138, 0.2);
}

/* ---- Checkbox ---- */
QCheckBox {
    color: #1a1a1a;
    font-size: 14px;
    spacing: 8px;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(0, 0, 0, 0.14);
    border-radius: 4px;
    background: #ffffff;
}
QCheckBox::indicator:hover {
    border-color: rgba(0, 0, 0, 0.3);
}
QCheckBox::indicator:checked {
    background: #d6608a;
    border-color: #d6608a;
}

/* ---- Switch (CheckBox styled as toggle) ---- */
QCheckBox#switch {
    spacing: 8px;
    background: transparent;
}
QCheckBox#switch::indicator {
    width: 40px;
    height: 22px;
    border-radius: 11px;
    border: 2px solid rgba(0, 0, 0, 0.14);
    background: #e8e6e3;
}
QCheckBox#switch::indicator:hover {
    border-color: rgba(0, 0, 0, 0.3);
}
QCheckBox#switch::indicator:checked {
    background: #d6608a;
    border-color: #d6608a;
}

/* ---- Radio button ---- */
QRadioButton {
    color: #1a1a1a;
    font-size: 14px;
    spacing: 8px;
    background: transparent;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(0, 0, 0, 0.14);
    border-radius: 10px;
    background: #ffffff;
}
QRadioButton::indicator:hover {
    border-color: rgba(0, 0, 0, 0.3);
}
QRadioButton::indicator:checked {
    background: #d6608a;
    border-color: #d6608a;
}

/* ---- Progress bar ---- */
QProgressBar {
    border: none;
    border-radius: 3px;
    background-color: #f0eeeb;
    height: 6px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    border-radius: 3px;
    background-color: #d6608a;
}

/* ---- Scroll area ---- */
QScrollArea {
    border: none;
    background: transparent;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}

/* ---- Scrollbar ---- */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 6px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(0, 0, 0, 0.18);
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    height: 0;
    background: none;
}
QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 6px;
}
QScrollBar::handle:horizontal {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: rgba(0, 0, 0, 0.18);
}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    width: 0;
    background: none;
}

/* ---- ToolTip ---- */
QToolTip {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
}

/* ---- Menu (in case context menus appear) ---- */
QMenu {
    background-color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 4px;
}
QMenu::item {
    padding: 8px 24px;
    border-radius: 6px;
    color: #1a1a1a;
}
QMenu::item:selected {
    background: rgba(214, 96, 138, 0.1);
    color: #d6608a;
}
QMenu::separator {
    height: 1px;
    background: rgba(0, 0, 0, 0.06);
    margin: 4px 8px;
}

/* ---- Group box ---- */
QGroupBox {
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 24px;
    font-size: 14px;
    font-weight: 600;
    color: #1a1a1a;
    background: transparent;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #1a1a1a;
}

/* ---- Slider ---- */
QSlider::groove:horizontal {
    height: 4px;
    background: #e8e6e3;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    width: 16px;
    height: 16px;
    margin: -6px 0;
    background: #d6608a;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #c44e7a;
}
QSlider::sub-page:horizontal {
    background: #d6608a;
    border-radius: 2px;
}

/* ---- Label base ---- */
QLabel {
    background: transparent;
    color: #1a1a1a;
}

/* ---- PushButton base ---- */
QPushButton {
    background: transparent;
    border: none;
    color: #1a1a1a;
}
"""


def apply_theme(app: QApplication):
    app.setStyleSheet(QSS)
