from __future__ import annotations
import os.path
from typing import Optional, List, Iterable

import magic
from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileIconProvider

from picture_comparator_muri.utils import readable_size


class FileInfo:
    provider = QFileIconProvider()

    def __init__(self, path: str, parent: FileInfo = None, known_children=None):
        self.path = os.path.abspath(path)
        self._parent: Optional[FileInfo] = parent
        self._is_dir: Optional[bool] = None
        self._size: Optional[str] = None
        self._dirs: Optional[List[FileInfo]] = None
        self._files: Optional[List[FileInfo]] = None
        self._mime: Optional[str] = None
        # When creating parent, pass known children, so we don't need to create new FileInfo objects.
        if known_children is None:
            self._known_children = {}
        elif isinstance(known_children, FileInfo):
            self._known_children = {known_children.path: known_children}
        else:
            self._known_children = {file.path: file for file in known_children}

    def __repr__(self):
        return f'{type(self).__name__}({self.path})'

    @property
    def name(self) -> str:
        return os.path.basename(self.path)

    @property
    def icon(self) -> QIcon:
        return self.provider.icon(QFileInfo(self.path))

    @property
    def parent(self) -> Optional[FileInfo]:
        if self._parent is None:
            parent_path = os.path.dirname(self.path)
            if self.path == parent_path:
                return None
            self._parent = FileInfo(parent_path)
        return self._parent

    @property
    def is_dir(self) -> bool:
        if self._is_dir is None:
            self._is_dir = os.path.isdir(self.path)
        return self._is_dir

    @property
    def size(self) -> str:
        if self._size is None:
            if self.is_dir:
                self._size = str(len(self.children))
            else:
                self._size = readable_size(os.path.getsize(self.path))
        return self._size

    @property
    def mime(self) -> str:
        if self._mime is None:
            self._mime = magic.from_file(os.path.realpath(self.path), mime=True)
        return self._mime

    @property
    def type(self) -> str:
        return self.mime.split('/')[0]

    def _get_files(self):
        if not os.path.isdir(self.path):
            self._dirs = []
            self._files = []
        else:
            try:
                _, dir_names, file_names = next(os.walk(self.path))
            except StopIteration:
                dir_names = file_names = tuple()
            self._dirs = []
            self._files = []
            self._fill_children(file_names, self._files)
            self._fill_children(dir_names, self._dirs)
            self._files = sorted(self._files)
            self._dirs = sorted(self._dirs)

    def _fill_children(self, filenames: Iterable[str], dest_list: List):
        for name in filenames:
            path = os.path.join(self.path, name)
            if path in self._known_children:
                file_info = self._known_children[path]
                file_info.parent = self
                dest_list.append(self._known_children[path])
            else:
                dest_list.append(FileInfo(path, self))

    @property
    def dirs(self) -> List[FileInfo]:
        if self._dirs is None:
            self._get_files()
        return self._dirs

    @property
    def files(self) -> List[FileInfo]:
        if self._files is None:
            self._get_files()
        return self._files

    @property
    def children(self) -> List[FileInfo]:
        return self.dirs + self.files

    @property
    def directory(self) -> FileInfo:
        """Returns self if is directory. Return parent otherwise."""
        if self.is_dir:
            return self
        return self.parent

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError
        return self.children[item]

    # Operators used for sorting files in a view, so we don't care about full path and only compare names.

    type_error_message = "'%s' not supported between instances of '%s' and '%s'"

    def __contains__(self, item):
        if isinstance(item, FileInfo):
            return item in self.children
        elif isinstance(item, str):
            return os.path.abspath(item) in (file.path for file in self.children)
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.path == os.path.abspath(other)
        if not isinstance(other, FileInfo):
            raise TypeError(self.type_error_message % ('==', self.__class__.__name__, other.__class__.__name__))
        return self.path == other.path

    def __hash__(self):
        return hash(self.path)

    def __neg__(self, other) -> bool:
        return not self == other

    def __lt__(self, other) -> bool:
        if not isinstance(other, FileInfo):
            raise TypeError(self.type_error_message % ('<', self.__class__.__name__, other.__class__.__name__))
        if self.is_dir != other.is_dir:
            return not self.is_dir
        return self.name < other.name

    def __le__(self, other) -> bool:
        if not isinstance(other, FileInfo):
            raise TypeError(self.type_error_message % ('<=', self.__class__.__name__, other.__class__.__name__))
        if self.is_dir != other.is_dir:
            return not self.is_dir
        return self.name <= other.name

    def __gt__(self, other) -> bool:
        if not isinstance(other, FileInfo):
            raise TypeError(self.type_error_message % ('>', self.__class__.__name__, other.__class__.__name__))
        if self.is_dir != other.is_dir:
            return self.is_dir
        return self.name > other.name

    def __ge__(self, other) -> bool:
        if not isinstance(other, FileInfo):
            raise TypeError(self.type_error_message % ('>=', self.__class__.__name__, other.__class__.__name__))
        if self.is_dir != other.is_dir:
            return self.is_dir
        return self.name >= other.name
