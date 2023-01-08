from __future__ import annotations

import os
import re
from enum import Enum
from typing import Optional, Dict, Sequence, Union, Any, List

from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, QPersistentModelIndex, QObject, QMimeData
from PySide6.QtWidgets import QMessageBox, QDialog, QWidget, QDialogButtonBox, QTreeView

from picture_comparator_muri.model.file import FileInfo
from picture_comparator_muri.model.image_group import ImageGroup
from picture_comparator_muri.model.image_info import ImageInfo
from picture_comparator_muri.view.manual_rename_ui import Ui_Dialog


class DisplayMode(Enum):
    SELECTED = 'show_selected_button'
    GROUP = 'show_group_button'
    IMAGES = 'show_images_button'
    ALL = 'show_all_button'


class RenamerFilter:
    """
    Custom filter making sure dialog shows proper files. It handles skipping hidden files, non-applied renames and
    moving of files.
    """
    def __init__(self, widget: 'RenamerDialog'):
        self.widget: 'RenamerDialog' = widget
        self.model: Optional[RenamerModel] = None
        self.renames: Dict[Union[FileInfo, str], str] = {}  # str won't be hold in key, but can be used to get entry.

    @property
    def display_mode(self) -> DisplayMode:
        return self.widget.display_mode

    @property
    def show_hidden(self) -> bool:
        return self.widget.ui.show_hidden_button.isChecked()

    @property
    def enable_all(self) -> bool:
        return self.widget.ui.enable_all_button.isChecked()

    @property
    def group(self) -> ImageGroup:
        return self.widget.image_group

    @property
    def selected(self) -> Sequence[ImageInfo]:
        return self.widget.selected

    def visible_children(self, file: FileInfo, *, disable_sorting: bool = False, display_mode: DisplayMode = None):
        all_children = file.children.copy()  # Get starting children
        for org_file, new_path in self.renames.items():
            if os.path.dirname(org_file.path) == file and os.path.dirname(new_path) != file:
                all_children.remove(org_file)
            elif os.path.dirname(org_file.path) != file and os.path.dirname(new_path) == file:
                all_children.append(org_file)

        if os.name != 'nt' and not self.show_hidden:
            all_children = [f for f in all_children if not f.name.startswith('.')]

        if display_mode is None:
            display_mode = self.display_mode

        if display_mode == DisplayMode.SELECTED:
            files = [f for f in all_children if f.is_dir or f in self.selected]
        elif display_mode == DisplayMode.GROUP:
            files = [f for f in all_children if f.is_dir or f in self.group]
        elif display_mode == DisplayMode.IMAGES:
            files = [f for f in all_children if f.is_dir or f.type == 'image']
        else:
            files = all_children
        if not disable_sorting:
            # Sort by display name instead of original name.
            files.sort(key=lambda f: (not f.is_dir, self.displayed_name(f)))
        return files

    def parent(self, file) -> Optional[FileInfo]:
        if file not in self.renames:
            return file.parent
        parent_dir = os.path.dirname(self.renames[file])
        return self.model.get_file_info(parent_dir)

    def row_count(self, file: FileInfo):
        count = len(self.visible_children(file, disable_sorting=True))
        if file == self.model.file:  # Add '..' to the current directory.
            count += 1
        return count

    def flags(self, file: FileInfo):
        flags = Qt.ItemIsSelectable | Qt.ItemIsDropEnabled
        if file.is_dir:
            flags |= Qt.ItemIsEnabled
            # Handle '..'
            if not self.model.is_at_system_root() and file == self.model.file.parent:
                return flags | Qt.ItemNeverHasChildren
            return flags
        else:
            if self.enable_all or file in self.selected:
                flags |= Qt.ItemIsEnabled | Qt.ItemIsEditable
            return flags | Qt.ItemIsDragEnabled | Qt.ItemNeverHasChildren

    def file_at_row(self, parent: FileInfo, row: int) -> FileInfo:
        if parent == self.model.file:
            if row == 0:  #
                return parent.parent
            # Act as if there is no '..'
            row -= 1
        visible = self.visible_children(parent)
        return visible[row]

    def row(self, file: FileInfo):
        visible = self.visible_children(file.parent)
        return visible.index(file)

    def displayed_path(self, file: FileInfo):
        if file in self.renames:
            return self.renames[file]
        return file.path

    def displayed_name(self, file: FileInfo):
        if file in self.renames:
            return os.path.basename(self.renames[file])
        return file.name

    def file_exists(self, path: str) -> bool:
        path = os.path.abspath(path)
        # Another file is to be renamed under the same path
        if path in self.renames.values():
            return True
        # File exists and isn't renamed
        return os.path.exists(path) and path not in self.renames

    def rename(self, original_file: FileInfo, new_path: str) -> bool:
        new_path = os.path.abspath(new_path)
        # File was already renamed by user
        if original_file in self.renames:
            # New path is the same as original: restore original path
            if new_path == original_file:
                if self.file_exists(original_file.path):
                    QMessageBox.critical(self.widget, "Cannot set name", "File already exists.")
                    return False
                del self.renames[original_file]
                return True
            elif new_path == self.renames[original_file]:  # New path didn't change
                return False
        elif original_file == new_path:  # No change
            return False

        if self.file_exists(new_path):
            QMessageBox.critical(self.widget, "Cannot set name", "File already exists.")
            return False
        self.renames[original_file] = new_path
        return True

    def size(self, file: FileInfo):
        if file.is_dir:
            return len(self.visible_children(file, disable_sorting=True, display_mode=DisplayMode.ALL))
        return file.size


class RenamerModel(QAbstractItemModel):
    def __init__(self, widget: 'RenamerDialog', renamer_filter: RenamerFilter):
        super().__init__()
        self.widget: 'RenamerDialog' = widget
        self.root_path = self.widget.root_path
        self.filter: RenamerFilter = renamer_filter
        self.filter.model = self
        self._file: Optional[FileInfo] = None

    @property
    def file(self) -> FileInfo:
        if self._file is None:
            self._file = FileInfo(self.root_path)
        return self._file

    @file.setter
    def file(self, file: FileInfo):
        self.layoutAboutToBeChanged.emit()
        self._file = file
        self.root_path = file.path
        self.layoutChanged.emit()

    def get_file_info(self, path: str):
        file = self.file
        while os.path.commonpath((path, file.path)) != file.path:
            file = file.parent
        while os.path.commonpath((path, file.path)) != path:
            uncommon = path[len(file.path) + 1:]
            child_name = uncommon.split(os.path.sep)[0]
            file = next(file for file in file.children if file.name == child_name)
        return file

    def is_at_system_root(self) -> bool:
        return self.file.path == os.path.sep

    def has_dot_dot(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        return not parent.isValid() and not self.is_at_system_root()

    def supportedDragActions(self) -> Qt.DropActions:
        return Qt.MoveAction

    def supportedDropActions(self) -> Qt.DropActions:
        return Qt.MoveAction

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        # TODO; For now we just have name and size
        return 2

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        if parent.column() > 0:
            return 1
        if not parent.isValid():
            file = self.file
        else:
            file = parent.internalPointer()
        return self.filter.row_count(file)

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        if index.column() == 0:
            return self.filter.flags(index.internalPointer())
        return Qt.ItemIsEnabled | Qt.ItemNeverHasChildren

    def index(self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_file = self.file
        else:
            parent_file = parent.internalPointer()
        file = self.filter.file_at_row(parent_file, row)
        return self.createIndex(row, column, file)

    def parent(self, index: QModelIndex) -> QObject:
        if not index.isValid():
            return QModelIndex()
        file: FileInfo = index.internalPointer()
        parent_file = self.filter.parent(file)
        # '..' should behave as child of current dir, even though it's actually its parent
        if parent_file is None or file == self.file.parent:
            return QModelIndex()
        if parent_file == self.file:
            return QModelIndex()
        return self.createIndex(self.filter.row(parent_file), 0, parent_file)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if section == 0:
                return "File"
            elif section == 1:
                return "Size"

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None
        if role == Qt.DecorationRole and index.column() == 0:
            file: FileInfo = index.internalPointer()
            return file.icon
        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None
        file = index.internalPointer()
        if index.column() == 0:
            if file is self.file.parent:
                return '..'
            return self.filter.displayed_name(file)
        else:
            if file is self.file.parent:
                return ''
            return self.filter.size(file)

    def setData(self, index: [QModelIndex, QPersistentModelIndex], value, role: int = ...) -> bool:
        if role != Qt.EditRole:
            return super().setData(index, value, role)
        file: FileInfo = index.internalPointer()
        dir_path = os.path.dirname(file.path)
        new_path = os.path.join(dir_path, value)
        was_changed = self.filter.rename(file, new_path)
        if was_changed:  # We need to refresh view, because on renaming we might want to change order of items.
            self.layoutAboutToBeChanged.emit()
            self.layoutChanged.emit()
        return was_changed

    def hasChildren(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> bool:
        if not parent.isValid():
            return True
        file = parent.internalPointer()
        return bool(file.children)

    def mimeData(self, indexes: List[QModelIndex]) -> QMimeData:
        mime = super().mimeData(indexes)
        urls = [self.filter.displayed_path(i.internalPointer()) for i in indexes if i.isValid()]
        mime.setUrls(urls)
        return mime

    def canDropMimeData(self, data: QMimeData, action: Qt.DropAction, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        if not parent.isValid():
            return False
        destination: FileInfo = parent.internalPointer().directory
        # Any of moved files actually changes directory.
        return any(os.path.dirname(path.path()) != destination.path for path in data.urls())

    auto_name_regex = re.compile(r".*\((\d+)\)")

    def autoname(self, org_destination: str):
        result = org_destination
        directory, name = os.path.split(result)
        ext = ''
        parts = name.split('.')
        if len(parts) > 1:
            name = '.'.join(parts[:-1])
            ext = parts[-1]
        while self.filter.file_exists(result):
            reg = self.auto_name_regex.match(name)
            if reg:
                num = int(reg[2]) + 1
                name = f'{reg[1]}_{num}'
            else:
                name = name + '_0'
            if ext:
                result = os.path.join(directory, name + '.' + ext)
            else:
                result = os.path.join(directory, name)
        return result

    def dropMimeData(self, data: QMimeData, action: Qt.DropAction, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        if not parent.isValid():
            return False
        destination: FileInfo = parent.internalPointer().directory
        any_changed = False
        for url in data.urls():
            if os.path.dirname(url.path()) != destination.path:
                moved_name = os.path.basename(url.path())
                dst_str = os.path.join(destination.path, moved_name)
                if self.filter.file_exists(dst_str):
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Question)
                    msg_box.setText("Unable to move file.")
                    msg_box.setInformativeText(f"File named {moved_name} already exists under given path.")
                    msg_box.addButton("Automatic rename.", QMessageBox.AcceptRole)
                    msg_box.addButton("Manual rename.", QMessageBox.AcceptRole)
                    msg_box.addButton("Skip.", QMessageBox.RejectRole)
                    ret = msg_box.exec()
                    if ret == 0:
                        dst_str = self.autoname(dst_str)
                    elif ret == 1:
                        dialog = ManualRenameDialog(dst_str, self.widget)
                        result = dialog.exec()
                        if result:
                            dst_str = os.path.join(destination.path, dialog.ui.name_edit.text())
                        else:
                            continue
                    else:
                        continue
                was_changed = self.filter.rename(self.get_file_info(url.path()), dst_str)
                if was_changed:  # We need to refresh view, because on renaming we might want to change order of items.
                    any_changed = True
                    self.layoutAboutToBeChanged.emit()
                    self.layoutChanged.emit()
                    view: QTreeView = self.widget.ui.file_view
                    view.selectionModel().clearSelection()
        return any_changed


class ManualRenameDialog(QDialog):
    def __init__(self, old_path: str, parent: QWidget):
        super().__init__(parent=parent)
        self.old_path: str = old_path
        self.directory, self.old_name = os.path.split(self.old_path)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label.setText(self.ui.label.text().format(old_name=self.old_name))
        self.ui.file_exists_warning.setVisible(False)

        for button in self.ui.buttonBox.buttons():
            if self.ui.buttonBox.standardButton(button) == QDialogButtonBox.Ok:
                self.ok_button = button

        self.ui.name_edit.textChanged.connect(self.check_if_exists)
        self.ui.name_edit.setText(self.old_name)

    def check_if_exists(self, new_text: str):
        self.ok_button.setEnabled(bool(new_text))
        if not new_text:
            self.ui.file_exists_warning.setVisible(False)
            return
        exists = os.path.exists(os.path.join(self.directory, new_text))
        self.ui.file_exists_warning.setVisible(exists)
        self.ok_button.setEnabled(not exists)
