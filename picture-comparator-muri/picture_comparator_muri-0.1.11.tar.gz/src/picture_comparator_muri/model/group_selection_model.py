from __future__ import annotations
from typing import Union, Optional, Set, Sequence, List

from PySide6.QtCore import QItemSelectionModel, QModelIndex, QPersistentModelIndex, QItemSelection, Signal

from picture_comparator_muri.model.display_settings import DisplaySettings, DisplayMode
from picture_comparator_muri.model.image_info import ImageInfo
from picture_comparator_muri.model.utils import first, last


class ManualSelection:
    def __init__(self, item_selection_model: GroupSelectionModel):
        self.selection_model: GroupSelectionModel = item_selection_model

    def __enter__(self):
        self.selection_model.manual_selection = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.selection_model.manual_selection = False


class CurrentSelection:
    def __init__(self):
        self.starting_index: Optional[QModelIndex] = None
        self.ending_index: Optional[QModelIndex] = None
        self.original_states = {}

    def selecting(self, selection: QItemSelection):
        if self.starting_index is None:
            if selection.indexes():
                index = first(selection.indexes())
                self.starting_index = index
                self.ending_index = self.starting_index
        else:
            # Selection.indexes() is sorted collection. If we move left, we want to get first index. If left – last.
            # This can be checked by comparing first index with starting index.
            index = first(selection.indexes())
            if index == self.starting_index:
                index = last(selection.indexes())
            self.ending_index = index


class MarkingSelection(CurrentSelection):
    """Helper class, for marking multiple elements at once."""
    def __init__(self):
        super().__init__()
        self.select: Optional[bool] = None

    def selecting(self, selection: QItemSelection) -> bool:
        if self.starting_index is None:
            if selection.indexes():
                index = first(selection.indexes())
                self.starting_index = index
                self.ending_index = self.starting_index
                image: ImageInfo = self.starting_index.data()
                self.select = not image.marked_for_deletion
                image.marked_for_deletion = self.select
                return True
        else:
            # Selection.indexes() is sorted collection. If we move left, we want to get first index. If left – last.
            # This can be checked by comparing first index with starting index.
            index = first(selection.indexes())
            if index == self.starting_index:
                index = last(selection.indexes())
            if self.is_between(index):
                end_image: ImageInfo = self.ending_index.data()
                is_change = end_image.marked_for_deletion != self.original_states[self.ending_index.row()]
                end_image.marked_for_deletion = self.original_states[self.ending_index.row()]
                self.ending_index = index
                return is_change
            elif self.ending_index != index:
                self.ending_index = index
                image: ImageInfo = index.data()
                self.original_states[index.row()] = image.marked_for_deletion
                is_change = image.marked_for_deletion != self.select
                image.marked_for_deletion = self.select
                return is_change
        return False

    def is_between(self, index: QModelIndex) -> bool:
        return (self.starting_index.row() <= index.row() < self.ending_index.row()) or (self.starting_index.row() >= index.row() > self.ending_index.row())


class GroupSelectionModel(QItemSelectionModel):
    markingChanged = Signal(list)
    # normalChanged = Signal(None, None)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.display_settings: Optional[DisplaySettings] = None
        self.select_manually: ManualSelection = ManualSelection(self)
        self.manual_selection = False
        self._current: Optional[CurrentSelection] = None

    def _result(self, selection: QItemSelection, command: QItemSelectionModel.SelectionFlags) -> Set[int]:
        result_selection = set(i.row() for i in self.selection().indexes())
        if command == QItemSelectionModel.Clear:
            return set()
        for i in selection.indexes():
            if command & QItemSelectionModel.Select:
                result_selection.add(i.row())
            else:
                result_selection.discard(i.row())
        return result_selection

    def select(self, index: Union[QModelIndex, QPersistentModelIndex], command: QItemSelectionModel.SelectionFlags) -> None:
        if not isinstance(index, QItemSelection):
            return
        if self.manual_selection:
            old_selection = self.selection()
            super().select(index, command)
            self.selectionChanged.emit(self.selection(), old_selection)
        elif self._current is None or not isinstance(self._current, MarkingSelection):
            # deselected = self._current.get_deselected(index, command) if self._current else []
            # If display mode is SINGLE, make sure only last changed end up selected
            before_len = len(self.selection().indexes())
            result_selection = self._result(index, command)
            if self.display_settings.display_mode == DisplayMode.SINGLE:
                command = QItemSelectionModel.ClearAndSelect
                if self._current is None:
                    self._current = CurrentSelection()
                self._current.selecting(index)
                if self._current.ending_index is not None:
                    index = QItemSelection(self._current.ending_index, self._current.ending_index)
                elif before_len > 0:
                    index = QItemSelection(first(self.selection().indexes()), first(self.selection().indexes()))
                else:
                    i = self.model().createIndex(0, 0)
                    index = QItemSelection(i, i)
            elif self.display_settings.display_mode == DisplayMode.ONE_BY_ONE:
                if before_len >= 2 and len(result_selection) < 2:
                    return
                elif len(result_selection) == 1:
                    for i in range(self.model().rowCount()):
                        if i not in result_selection:
                            row_index = self.model().createIndex(i, 0)
                            index = QItemSelection(row_index, row_index)
                            break
                elif len(result_selection) == 0:
                    i = self.model().createIndex(0, 0)
                    j = self.model().createIndex(1, 0)
                    index = QItemSelection(i, j)
                    command = QItemSelectionModel.ClearAndSelect
            super().select(index, command)
            # self.normalChanged.emit(None, None)
        else:  # When in marking mode:
            if self._current.selecting(index):
                self.markingChanged.emit(self.markings())  # emit marked

    def get_indexes_of_elements(self, elements: Sequence):
        indexes = []
        for i, e in enumerate(self.model().elements):
            if e in elements:
                indexes.append(i)
        return indexes

    def new_selection(self, indexes: List[int]):
        """Manually """
        if self.display_settings.display_mode == DisplayMode.SINGLE:
            if len(indexes) > 1:
                indexes = indexes[:1]
            elif len(indexes) < 1:
                indexes = [0]
        elif self.display_settings.display_mode == DisplayMode.ONE_BY_ONE:
            i = 0
            while len(indexes) < 2:
                if i not in indexes:
                    indexes.append(i)
                i += 1
        selection = QItemSelection()
        for index in indexes:
            i = self.model().createIndex(index, 0)
            selection.select(i, i)
        with self.select_manually:
            self.select(selection, QItemSelectionModel.ClearAndSelect)

    def markings(self):
        """Returns list of marked indexes."""
        return [element for element in self.model().elements if element.marked_for_deletion]

    def press_started(self):
        if self.display_settings.delete_mode:
            self._current = MarkingSelection()
        else:
            self._current = CurrentSelection()

    def press_ended(self):
        self._current = None
