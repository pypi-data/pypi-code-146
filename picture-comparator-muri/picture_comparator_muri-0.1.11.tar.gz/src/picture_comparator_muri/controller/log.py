from PySide6.QtCore import Slot

from picture_comparator_muri.model.log_engine import LogEngine, LogMessage, LogMessageModel, LogType
from picture_comparator_muri.model.watched_list import WatchedList
from picture_comparator_muri.view.log import LogView, StatusbarIcon
from picture_comparator_muri.view.main_window import MainWindow


class LogController:
    def __init__(self, window: MainWindow):
        self.log_engine: LogEngine = LogEngine()
        self.log_view: LogView = LogView()
        self.window = window
        self.list = WatchedList([])
        self.model = LogMessageModel(self.list)
        self.log_view.ui.log_table_view.setModel(self.model)
        self.statusbar_notification: LogType = LogType.INFO
        self.statusbar_icon = StatusbarIcon()
        self.window.ui.statusbar.addPermanentWidget(self.statusbar_icon)

        self.log_view.LogShowed.connect(self.log_window_shown)
        self.statusbar_icon.Clicked.connect(self.statusbar_icon_clicked)

    def show(self):
        self.log_view.show()

    def log_message(self, message: LogMessage):
        self.log_engine.log_message(message)
        self.list.append(message)
        if message.show_on_statusbar:
            self.window.ui.statusbar.showMessage(message.message, 2000)
            if message.log_type != LogType.INFO:
                self.show_statusbar_notification(message.log_type)

    def show_statusbar_notification(self, log_type: LogType):
        if self.log_view.isHidden():
            if log_type == LogType.WARNING and self.statusbar_notification == LogType.INFO:
                self.statusbar_icon.show_warning()
            elif log_type == LogType.ERROR:
                self.statusbar_icon.show_error()

    @Slot()
    def log_window_shown(self):
        self.statusbar_icon.clear_notification()

    @Slot()
    def statusbar_icon_clicked(self):
        self.show()
