from __future__ import annotations

import hashlib
import os.path
import shutil
from typing import Sequence, Dict, Optional

from PySide6.QtCore import QDir, QModelIndex, Signal
from PySide6.QtWidgets import QDialog, QButtonGroup, QAbstractButton, QMessageBox

from picture_comparator_muri.model.file import FileInfo
from picture_comparator_muri.model.image_group import ImageGroup
from picture_comparator_muri.model.image_info import ImageInfo
from picture_comparator_muri.model.renamer_model import RenamerFilter, RenamerModel, DisplayMode
from picture_comparator_muri.view.renamer_ui import Ui_Renamer


class RenamerDialog(QDialog):
    ItemDoubleClicked = Signal(QModelIndex)

    def __init__(self, parent, group: ImageGroup, selected: Sequence[ImageInfo]):
        super().__init__(parent)
        self.image_group = group
        self.selected = selected

        self.root_path = os.path.commonpath(tuple(i.path for i in selected))

        self.ui = Ui_Renamer()
        self.ui.setupUi(self)
        self.show_selected_all_buttons = QButtonGroup()
        self.show_selected_all_buttons.addButton(self.ui.show_selected_button)
        self.show_selected_all_buttons.addButton(self.ui.show_group_button)
        self.show_selected_all_buttons.addButton(self.ui.show_images_button)
        self.show_selected_all_buttons.addButton(self.ui.show_all_button)
        self.show_selected_all_buttons.buttonClicked.connect(self.show_changed)
        self.ui.show_hidden_button.clicked.connect(self.view_changed)
        self.ui.enable_all_button.clicked.connect(self.view_changed)

        self.display_mode: DisplayMode = DisplayMode.SELECTED

        self.file_filter = RenamerFilter(self)
        self.file_system_model = RenamerModel(self, self.file_filter)

        self.ui.file_view.setModel(self.file_system_model)
        self.ui.file_view.doubleClicked.connect(self.on_item_double_clicked)

    def show_changed(self, button: QAbstractButton):
        self.file_system_model.layoutAboutToBeChanged.emit()
        self.display_mode = DisplayMode(button.objectName())
        self.file_system_model.layoutChanged.emit()

    def view_changed(self, button: QAbstractButton):
        self.file_system_model.layoutAboutToBeChanged.emit()
        self.file_system_model.layoutChanged.emit()

    def on_item_double_clicked(self, index: QModelIndex):
        file: FileInfo = index.internalPointer()
        if file.is_dir:
            self.file_system_model.file = file

    def accept(self) -> None:
        super().accept()
        Rename.widget = self
        renames = [Rename(old.path, new) for old, new in self.file_system_model.filter.renames.items()]
        Rename.renames = {r.old: r for r in renames}
        while renames:
            rename = renames.pop(0)
            if not rename.commit():
                renames.append(rename)


class Rename:
    widget = None
    renames: Dict[str, Rename] = None  # {src, rename_obj}

    def __init__(self, old: str, new: str):
        self.old = old
        self.new = new
        self.blocked_by: Optional[Rename] = None

    def commit(self) -> bool:
        if not os.path.exists(self.new):
            try:
                shutil.move(self.old, self.new)
                return True
            except OSError:
                QMessageBox.critical(self.widget, "Renaming error.", "Unable to rename file.")
                return False
        # File exists but we plan to move it
        if self.new in self.renames:
            self.blocked_by = self.renames[self.new]
            if self.is_deadlock(self.blocked_by):
                tmp_path = self.get_tmp_path()
                shutil.move(self.old, tmp_path)
                self.old = tmp_path
            return False

    def is_deadlock(self, blocking: Rename):
        while blocking.blocked_by:
            if blocking.blocked_by is self:
                return True
            blocking = blocking.blocked_by
        return False

    @staticmethod
    def get_tmp_path():
        path = os.path.join(QDir.tempPath(), hashlib.sha256('asdasd'.encode('utf-8')).hexdigest())
        while os.path.exists(path):
            path += '_'
        return path
