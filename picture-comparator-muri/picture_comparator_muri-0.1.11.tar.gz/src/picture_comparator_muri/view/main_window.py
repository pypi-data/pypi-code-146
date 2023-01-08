from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeyEvent, QCloseEvent
from PySide6.QtWidgets import QMainWindow, QApplication

from picture_comparator_muri.view.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    DeleteModifierTriggered = Signal(bool)
    DeleteKeyPressed = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.splitter.setSizes([400, 2000])
        self.ui.splitter_2.setSizes([1000, 200])

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            self.DeleteModifierTriggered.emit(True)
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            self.DeleteModifierTriggered.emit(False)
        elif event.key() == Qt.Key_Delete:
            self.DeleteKeyPressed.emit()
        event.accept()

    def closeEvent(self, event: QCloseEvent) -> None:
        QApplication.quit()
