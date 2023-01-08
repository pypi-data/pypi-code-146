from typing import Optional, List

from PySide6.QtCore import QItemSelection, QItemSelectionModel, Slot
from PySide6.QtWidgets import QPushButton, QMessageBox

from picture_comparator_muri.controller.action_buttons import ActionButtonsController
from picture_comparator_muri.controller.comparator import Comparator
from picture_comparator_muri.model.display_settings import DisplayMode
from picture_comparator_muri.model.group_selection_model import GroupSelectionModel
from picture_comparator_muri.model.image_group import ImageGroup
from picture_comparator_muri.model.image_info import ImageInfo
from picture_comparator_muri.model.watched_list import WatchedList
from picture_comparator_muri.view.group_list_view import GroupListView
from picture_comparator_muri.view.main_window_ui import Ui_MainWindow
from picture_comparator_muri.view.renamer_dialog import RenamerDialog


class GroupList:
    def __init__(self, main_window_controller):
        from picture_comparator_muri.controller.main_window import MainWindowController
        self.main_window_controller: MainWindowController = main_window_controller
        self.comparator = Comparator(main_window_controller)
        self.action_buttons: ActionButtonsController = main_window_controller.action_buttons
        self.delete_button: QPushButton = self.ui.delete_button
        self.display_settings = self.action_buttons.display_settings

        self.list_view: GroupListView = self.ui.current_group_list_view
        self.image_group: Optional[ImageGroup] = None
        self.images = WatchedList([])
        self.list_view.model().set_list(self.images)
        self.list_view.set_display_settings(self.display_settings)

        self.selection: GroupSelectionModel = self.list_view.selectionModel()
        self.selection.selectionChanged.connect(self.selection_changed)
        self.selection.markingChanged.connect(self.markings_changed)

        self.action_buttons.DisplayModeChanged.connect(self.display_mode_changed)
        self.delete_button.clicked.connect(self.delete_marked)
        self.main_window_controller.window.DeleteKeyPressed.connect(self.delete_marked)

    @property
    def ui(self) -> Ui_MainWindow:
        return self.main_window_controller.window.ui

    def clear(self):
        self.image_group = None
        self.images.clear()
        self.comparator.clear()
        self.update_selection()

    def set_group(self, image_group: ImageGroup):
        with self.selection.select_manually:
            self.selection.clear()
        image_group.clear_markings()
        self.image_group = image_group
        self.image_group.set_identical()
        self.images.replace(image_group)
        self.comparator.reset()
        self.update_selection()

    def update_selection(self):
        index = self.list_view.model().createIndex(-1, -1)
        selection = QItemSelection(index, index)
        self.selection.select(selection, QItemSelectionModel.Select)

    def selection_changed(self, selected, deselected):
        # Workaround for marking images as selected
        if not self.image_group:
            return
        for image in self.image_group:
            image.selected = False
        for index in self.selection.selection().indexes():
            index.data().selected = True
        images = [index.data() for index in self.selection.selection().indexes()]
        images.sort(key=lambda i: i.path)
        self.comparator.set_images(images, False)

    def display_mode_changed(self, display_mode: DisplayMode):
        self.update_selection()

    def markings_changed(self, markings: List[ImageInfo]):
        self.delete_button.setEnabled(bool(markings))

    @Slot()
    def delete_marked(self, *args):
        if self.image_group and self.image_group.has_marked():
            to_remove: List[ImageInfo] = self.image_group.marked_for_deletion()
            file_list: str = '\n'.join(file.path for file in to_remove)
            reply = QMessageBox.warning(self.main_window_controller.window, "Move to the trash?",
                                        f"Do you want to remove marked files?\n{file_list}",
                                        QMessageBox.Apply | QMessageBox.Cancel)
            if reply == QMessageBox.Apply:
                not_removed = self.image_group.delete_marked()
                if not_removed:
                    file_list = '\n'.join(image.path for image in not_removed)
                    QMessageBox.warning(self.main_window_controller.window, "Unable to remove files.", "Unable to move listed files to trash:\n" + file_list)
                if len(self.image_group) > 1:
                    self.images.remove_multiple(to_remove)
                    self.image_group.reset_identical()

                    # Because of problems with selection after removing item, we just reset it.
                    new_indexes = self.selection.get_indexes_of_elements([i for i in self.images if i.selected])
                    self.selection.new_selection(new_indexes)
                    self.comparator.update_view()
                else:
                    # No images to compare. Drop current match group.
                    self.main_window_controller.matches.remove_current_match()

    @Slot()
    def show_rename_dialog(self):
        if not self.image_group:
            return
        dialog = RenamerDialog(self.main_window_controller.window, self.image_group, [i for i in self.images if i.selected])
        result = dialog.exec()
        if result:
            renames = dialog.file_system_model.filter.renames
            self.image_group.rename(renames)
            self.images.replace(self.image_group)
            # Reselect elements, as changing images breaks selection model
            images = [image for image in self.images if image.selected]
            indexes = self.selection.get_indexes_of_elements(images)
            self.selection.new_selection(indexes)
