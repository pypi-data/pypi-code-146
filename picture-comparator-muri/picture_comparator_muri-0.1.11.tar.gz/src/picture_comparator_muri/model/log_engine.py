import datetime
from enum import Enum
from typing import Optional, Union

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QColor

from picture_comparator_muri.model.watched_list import WatchedList, WatchedListModel


class LogType(Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


class LogMessage:
    WARNING_COLOR = '#D4AA34'

    def __init__(self, log_type: LogType, message: str, show_on_statusbar: bool):
        self.log_type: LogType = log_type
        self.message: str = message
        self.show_on_statusbar: bool = show_on_statusbar
        self.time: Optional[datetime.datetime] = None

    def add_current_time(self):
        self.time = datetime.datetime.now()


class LogMessageModel(WatchedListModel):
    backgrounds = {
        LogType.INFO: None,
        LogType.WARNING: QColor.fromRgb(240, 215, 170),
        LogType.ERROR: QColor.fromRgb(240, 170, 177)
    }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return 2

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...):
        message: LogMessage = self.elements[index.row()]
        if role == Qt.BackgroundRole:
            return self.backgrounds[message.log_type]
        if not index.isValid() or index.row() >= len(self.elements) or index.column() >= 2 or role != Qt.DisplayRole:
            return None
        return message.message if index.column() == 1 else str(message.time)


class LogEngine:
    def __init__(self):
        self.messages = WatchedList([])

    def log_message(self, message: LogMessage):
        message.add_current_time()
        self.messages.append(message)
