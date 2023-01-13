import os
from sortedcontainers import SortedKeyList
from anytree import NodeMixin
from abc import ABC, abstractclassmethod
from pathlib import Path
from typing import List

from .logger import logger


class CatalogueContainer:
    """Holds CatalogueItems (actual objects) and provides sorting thereof."""

    def __init__(self):
        self.container = SortedKeyList(
            key=lambda item: (
                -item.size,
                item.dirpath,
                item.name,
            )
        )

    def __len__(self):
        return len(self.container)

    def __bool__(self):
        if self.container:
            return True
        else:
            return False

    def __contains__(self, obj):
        for item in self.container:
            if item == obj:
                return True
        return False

    def __iter__(self):
        return iter(self.container)

    def __getitem__(self, ix):
        return self.container[ix]

    def addItem(self, item: "CatalogueItem"):
        self.container.add(item)

    def removeItemByValue(self, item: "CatalogueItem"):
        self.container.remove(item)


class CatalogueItem(NodeMixin, ABC):
    """This is the AB class for an item held in the catalogue
    container. It's an anytree node as well.

    size = size in bytes
    """

    __slots__ = ["size", "dirpath", "name"]

    def __init__(self, iid: str, dirpath: str, name: str):
        super().__init__()
        self.iid = iid
        self.dirpath = f"{Path(dirpath)}{os.path.sep}"
        self.name = name

    def __str__(self):
        return self.getFullPath()

    def __repr__(self):
        return self.getFullPath()

    @abstractclassmethod
    def getSize():
        pass

    @abstractclassmethod
    def getFullPath(self) -> str:
        pass


class FileItem(CatalogueItem):
    __slots__ = ["type", "hash"]

    def __init__(self, iid: str, dirpath: str, name: str, hash_files: bool = False):
        super().__init__(iid, dirpath, name)
        self.setFileType(dirpath, name)

    def setFileType(self, dirpath: str, name: str):
        self.type = Path(self.name).suffix

    def getSize(self):
        return self.size

    def getFullPath(self) -> str:
        return str(Path(self.dirpath, self.name))


class DirItem(CatalogueItem):
    """Holds children as well.
    It has three CatalogueContainers, two for holding and sorting files and
    directories separately, and one for holding and sorting both together.

    The size is calculated on creation from all direct children.
    With no subdirectories in it the size of a directory for now
    is only the sum of the size of it's files. The additional
    4K, or whatever the filesystem says, of any directory are not added.
    """

    __slots__ = ["files", "dirs", "dirs_files", "children"]

    def __init__(
        self,
        iid: str,
        dirpath: str,
        name: str,
        file_children: List[FileItem] = [],
        dir_children: List["DirItem"] = [],
    ):
        super().__init__(iid, dirpath, name)
        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()
        self.dirs_files = CatalogueContainer()
        self.children = tuple(file_children + dir_children)
        self.size = 0

        if file_children or dir_children:
            logger.debug(f"Setting children of {self} on __init__ .")
            self.setChildren(file_children, dir_children)

    def setChildren(
        self, file_children: List[FileItem] = [], dir_children: List["DirItem"] = []
    ):
        for file_child in file_children:
            file_child.parent = self
            self.files.addItem(file_child)
            self.dirs_files.addItem(file_child)

        for dir_child in dir_children:
            dir_child.parent = self
            self.dirs.addItem(dir_child)
            self.dirs_files.addItem(dir_child)

        self.children = tuple(file_children + dir_children)

        logger.debug(f"File children of {self} are {file_children}.")
        logger.debug(f"Dir children of {self} are {dir_children}.")

        self.calcSetDirSize()

    def getSize(self):
        sum_size = 0
        sum_size += sum([child.size for child in self.children])
        return sum_size

    def getFullPath(self) -> str:
        return f"{Path(self.dirpath, self.name)}{os.path.sep}"

    def calcSetDirSize(self):
        """Calculate size from all direct children and set it."""
        sum_size = 0
        sum_size += sum([child.size for child in self.children])
        self.size = sum_size
