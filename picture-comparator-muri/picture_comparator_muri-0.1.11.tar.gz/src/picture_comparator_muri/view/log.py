from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QShowEvent, QPixmap, QMouseEvent
from PySide6.QtWidgets import QWidget, QLabel

from picture_comparator_muri.view.log_ui import Ui_LogWidget


class LogView(QWidget):
    LogShowed = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_LogWidget()
        self.ui.setupUi(self)

    def showEvent(self, event: QShowEvent) -> None:
        self.LogShowed.emit()
        super().showEvent(event)


class StatusbarIcon(QLabel):
    warning_pixmap = QIcon.fromTheme('data-warning').pixmap(20, 20)
    error_pixmap = QIcon.fromTheme('data-error').pixmap(20, 20)
    Clicked = Signal()

    def __init__(self):
        super().__init__()

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        super().mouseReleaseEvent(ev)
        self.Clicked.emit()

    def show_warning(self):
        self.setPixmap(self.warning_pixmap)

    def show_error(self):
        self.setPixmap(self.error_pixmap)

    def clear_notification(self):
        self.setPixmap(QPixmap())
