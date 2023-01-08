import os.path
from itertools import chain
from pathlib import Path
from typing import Optional, Union, Any

from PySide6.QtCore import QDir, QModelIndex, QStringListModel, QSortFilterProxyModel, QPersistentModelIndex, Qt
from PySide6.QtWidgets import QDialog, QFileSystemModel, QDialogButtonBox

from picture_comparator_muri.utils import path_from_index
from picture_comparator_muri.view.directory_picker_ui import Ui_Dialog


class DotDotInCurrentFilterModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        data = self.sourceModel().index(source_row, 0, source_parent).data()
        if data == '..':
            path = path_from_index(source_parent)
            path = os.path.join(*path)
            return path == self.sourceModel().rootPath()
        return True

    def filterAcceptsColumn(self, source_column: int, source_parent: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        if source_column != 0:
            return False
        return True


class DirectoryPicker(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        for button in self.ui.buttonBox.buttons():
            if self.ui.buttonBox.standardButton(button) == QDialogButtonBox.Ok:
                self.ok_button = button

        self.ok_button.setEnabled(False)

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setFilter(QDir.AllDirs | QDir.NoDot)
        self.file_system_model.setRootPath(QDir.currentPath())
        self.filter_model = DotDotInCurrentFilterModel(self)
        self.filter_model.setSourceModel(self.file_system_model)
        self.directories_model = QStringListModel()
        self.directories_list = []
        self.directories_model.setStringList(self.directories_list)

        self.ui.file_system_tree_view.setModel(self.filter_model)
        self.ui.directories_list.setModel(self.directories_model)

        root_index = self.file_system_model.index(QDir.currentPath())
        root_index = self.filter_model.mapFromSource(root_index)
        self.ui.file_system_tree_view.setRootIndex(root_index)
        self.ui.file_system_tree_view.setSortingEnabled(True)
        self.ui.file_system_tree_view.doubleClicked.connect(self.on_item_double_clicked)
        self.ui.file_system_tree_view.sortByColumn(0, Qt.AscendingOrder)

        self.file_system_selection = self.ui.file_system_tree_view.selectionModel()
        self.directories_selection = self.ui.directories_list.selectionModel()

    @property
    def include_subdirectories(self) -> bool:
        return self.ui.check_subdirectories_box.isChecked()

    def on_item_double_clicked(self, index: QModelIndex):
        """Goes to double clicked directory."""
        path = path_from_index(index)
        new_path = os.path.join(*path)
        self.file_system_model.setRootPath(new_path)
        root_index = self.file_system_model.index(new_path)
        root_index = self.filter_model.mapFromSource(root_index)
        self.ui.file_system_tree_view.setRootIndex(root_index)

    def selected_path(self) -> Optional[str]:
        """Returns path to currently selected directory or None if no directory is selected."""
        selection = self.file_system_selection.selection()
        if selection.count():
            path = os.path.join(*path_from_index(selection.indexes()[0]))
            return os.path.abspath(path)

    def selected_directory(self) -> Optional[str]:
        """Returns path to currently selected directory from picked directories list."""
        selection = self.directories_selection.selection()
        if selection.count():
            return selection.indexes()[0].data()

    def toggle_add_remove_buttons(self):
        selected_path = self.selected_path()
        if selected_path:
            path = Path(selected_path)
            if self.include_subdirectories:
                add_enabled = not any(Path(d) in chain([path], path.parents) for d in self.directories_list)
            else:
                add_enabled = selected_path not in self.directories_list
        else:
            add_enabled = True
        self.ui.add_button.setEnabled(add_enabled)
        self.ui.remove_button.setEnabled(bool(self.selected_directory()))
