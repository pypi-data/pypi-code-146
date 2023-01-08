from pathlib import Path
from typing import List

from PySide6.QtCore import QModelIndex

from picture_comparator_muri.view.directory_picker import DirectoryPicker


class DirectoryPickerController:
    def __init__(self):
        self.dialog = DirectoryPicker()
        self.dialog.file_system_selection.selectionChanged.connect(self.path_selection_changed)
        self.dialog.directories_selection.selectionChanged.connect(self.directories_selection_changed)
        self.dialog.ui.add_button.clicked.connect(self.add_clicked)
        self.dialog.ui.remove_button.clicked.connect(self.remove_clicked)

    @property
    def directories_list(self) -> List[str]:
        return self.dialog.directories_list

    @property
    def include_subdirectories(self) -> bool:
        return self.dialog.include_subdirectories

    def exec(self) -> int:
        return self.dialog.exec()

    def add_clicked(self):
        selected_path = self.dialog.selected_path()
        if selected_path:
            remove_list = []
            for i, existing_path in enumerate(self.directories_list):
                if Path(selected_path) in Path(existing_path).parents:
                    remove_list.append(i)
            for i in reversed(remove_list):
                del self.directories_list[i]
            self.directories_list.append(selected_path)
            self.dialog.directories_model.setStringList(self.directories_list)
            self.dialog.toggle_add_remove_buttons()
            self.toggle_ok_button()

    def remove_clicked(self):
        directory = self.dialog.selected_directory()
        if directory:
            self.directories_list.remove(directory)
            self.dialog.directories_model.setStringList(self.directories_list)
            self.dialog.toggle_add_remove_buttons()
            self.toggle_ok_button()

    def toggle_ok_button(self):
        self.dialog.ok_button.setEnabled(bool(self.directories_list))

    def path_selection_changed(self, current: QModelIndex, previous):
        self.dialog.toggle_add_remove_buttons()

    def directories_selection_changed(self, current: QModelIndex, previous):
        self.dialog.toggle_add_remove_buttons()
