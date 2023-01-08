from typing import List, Union, Any, Iterable

from PySide6.QtCore import Signal, QObject, QModelIndex, QPersistentModelIndex, QAbstractTableModel
from PySide6.QtGui import Qt


class WatchedList(QObject):
    ElementAdded = Signal(object, int)
    ContentChanged = Signal()

    def __init__(self, elements: List):
        super().__init__()
        self._elements: List = elements

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, item):
        if not isinstance(item, int) and not isinstance(item, slice):
            raise TypeError('list indices must be integers or slices, not str')
        return self._elements[item]

    def append(self, element):
        self._elements.append(element)
        self.ElementAdded.emit(element, len(self) - 1)

    def insert(self, index: int, element):
        self._elements.insert(index, element)
        self.ElementAdded.emit(element, index)

    def clear(self):
        self._elements.clear()
        self.ContentChanged.emit()

    def replace(self, elements: Iterable):
        self._elements.clear()
        self._elements.extend(elements)
        self.ContentChanged.emit()

    def remove(self, item):
        if item in self._elements:
            self._elements.remove(item)
            self.ContentChanged.emit()

    def remove_multiple(self, to_be_removed: Iterable):
        were_any_removed = False
        for item in to_be_removed:
            if item in self._elements:
                self._elements.remove(item)
                were_any_removed = True
        if were_any_removed:
            self.ContentChanged.emit()


class WatchedListModel(QAbstractTableModel):
    def __init__(self, elements: WatchedList = None):
        super().__init__()
        self.elements = None
        self._previous_len = 0
        if elements is not None:
            self.set_list(elements)

    def set_list(self, elements: WatchedList):
        old_len = 0
        if self.elements is not None:
            self.elements.ElementAdded.disconnect(self._element_added)
            old_len = len(self.elements)

        if old_len < len(elements):
            self.beginInsertRows(QModelIndex(), old_len, len(elements))
        else:
            self.beginRemoveRows(QModelIndex(), old_len, len(elements))
        self.elements = elements
        self.elements.ElementAdded.connect(self._element_added)
        self.elements.ContentChanged.connect(self.update_view)
        if old_len < len(elements):
            self.endInsertRows()
        else:
            self.endRemoveRows()

    def update_view(self):
        self.beginResetModel()
        self.endResetModel()

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.elements) if self.elements else 0

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return 1

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...):
        if not index.isValid() or index.row() >= len(self.elements) or role != Qt.DisplayRole:
            return None
        return self.elements[index.row()]

    def _element_added(self, _: Any, index: int):
        self.beginInsertRows(QModelIndex(), index, index)
        self.endInsertRows()
        return self.index(index, 0, QModelIndex())
