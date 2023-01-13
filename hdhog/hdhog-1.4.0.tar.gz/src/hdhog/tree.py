import os
from anytree.search import find_by_attr
from abc import ABC, abstractclassmethod
from pathlib import Path
from typing import List, Optional

from .container import CatalogueContainer, CatalogueItem, FileItem, DirItem
from .logger import logger


class Tree(ABC):
    @abstractclassmethod
    def deleteSubtree(self, node: CatalogueItem):
        pass

    @abstractclassmethod
    def updateAncestors(node: CatalogueItem):
        pass


class FSTree(Tree):
    def __init__(self, root_node: CatalogueItem = None):
        self.root_node = root_node
        self.file_iid = 0  # counter for file iids
        self.dir_iid = 0  # counter for dir iids

    def treeFromFSBottomUp(self, start):
        """Generator that walks the directory tree and builds the tree from the items.

        This wraps os.walk() with topdown=False, so it builds the tree bottom up.
        This is so the sizes of the directories can be calculated directly
        when building the tree.

        Implemented as generator so outside calling functions can keep track
        simultaneously and do stuff with the created items.

        Algorithm:

        1. Iterate over the files and put them in FileItems.

        2. Iterate over the directories.
            If it has no subdirectories create a DirItem for the parent
            directoy with just the files as children and store the
            DirItem as a root. Insert into directory container.
            This is in "leaf directories", so the algorithm starts with
            these as the bottom-most roots.

            Else create a DirItem with the subdirectories, which are now not
            roots anymore and are removed from the roots dict, as children as
            well, make it their parent and store it in the roots dict.
            Insert into directory container.

        The algorithm terminates with setting the topmost directory as the root
        item / node.

        Symlinks are skipped.

        Args:
            start (str, optional): Start of the walk..

        Raises:
            oserror: when os.walk fails

        Yields:
            Tuple[DirItem, List[FileItem]]: A parent DirItem and its file children
        """

        roots = {}

        def _raiseWalkError(oserror: OSError):
            """By default os.walk ignores errors. With this
            function passed as onerror= parameter exceptions are
            raised.

            Args:
                oserror (OSError): instance

            Raises:
                oserror:
            """
            raise oserror

        # do a rstrip, otherwise basename below will be empty
        for parent, dirs, files in os.walk(
            str(start).rstrip("/"),
            topdown=False,
            followlinks=False,
            onerror=_raiseWalkError,
        ):

            # make directories always have a path separator after name for easy distinction
            parent_name = f"{Path(parent).name}{os.path.sep}"
            parent_dirpath = f"{Path(parent).parent}{os.path.sep}"

            file_children = []

            for file in sorted(files):

                file_path = Path(parent, file)

                if file_path.is_symlink():
                    logger.debug(f"Skipping link {file_path}.")
                    continue

                fi = FileItem(f"F{self.file_iid}", f"{parent}{os.path.sep}", file)
                fi.size = Path(file_path).stat().st_size

                file_children.append(fi)
                self.file_iid += 1

            # this is in "leaf directories"; no dir children
            if not dirs:
                d_id = f"D{self.dir_iid}"
                parent_di = DirItem(
                    d_id, parent_dirpath, parent_name, file_children, []
                )
                roots[parent] = parent_di

                yield (parent_di, file_children)

            # in upper directories subdirectories are roots at first
            else:
                dir_children = []
                symlink_dirs = []
                # TODO: refactor vvv
                for d in sorted(dirs):
                    dirpath = Path(parent, d)
                    dirpath_str = str(dirpath)

                    if dirpath.is_symlink():
                        symlink_dirs.append(dirpath_str)
                        logger.debug(f"Skipping link {dirpath}.")
                        continue

                    dir_children.append(roots[dirpath_str])

                # the former roots have a parent now, so remove from them from roots
                for d in dirs:
                    dirpath = f"{Path(parent, d)}"
                    dirpath_str = str(dirpath)
                    if dirpath not in symlink_dirs:
                        del roots[dirpath_str]

                d_iid = f"D{self.dir_iid}"
                parent_di = DirItem(
                    d_iid,
                    parent_dirpath,
                    parent_name,
                    file_children,
                    dir_children,
                )

                roots[parent] = parent_di

                yield (parent_di, file_children)

            self.dir_iid += 1

        self.root_node = list(roots.items())[0][1]

    def deleteSubtree(
        self,
        node: CatalogueItem,
        file_list: CatalogueContainer,
        dir_list: CatalogueContainer,
        repeat_trees: List[Tree],
    ):
        """Recursively delete a tree with a given root <node> and remove the
        root from the global file or directory list.

        Repeat the operation on additional trees in list. Currently only used
        for GUI tree element.

        Args:
            node (CatalogueItem): a given node
            file_list (CatalogueContainer): global file list of Catalogue object
            dir_list (CatalogueContainer): global directory list of Catalogue object
            repeat_trees (List[Tree]): trees on which the operation is repeated
        """
        if node.children:
            logger.debug(f"Detaching all children of {node}")
            for file_item in node.files:
                file_item.parent = None

                logger.debug(f"Removing {file_item} from file list.")
                try:
                    file_list.removeItemByValue(file_item)
                except ValueError as ve:
                    logger.error(f"Error removing item from file container: {ve}")

            for dir_item in node.dirs:
                self.deleteSubtree(dir_item, file_list, dir_list, repeat_trees)

                dir_item.parent = None

                logger.debug(f"Removing {dir_item} from dir list.")
                try:
                    dir_list.removeItemByValue(dir_item)
                except ValueError as ve:
                    logger.error(f"Error removing item from dir container: {ve}")

        if isinstance(node, FileItem):
            file_list.removeItemByValue(node)
        if isinstance(node, DirItem):
            dir_list.removeItemByValue(node)

        self.rmNodeFromParent(node)
        self.updateAncestors(node, dir_list)

        for tree in repeat_trees:
            tree.updateAncestors(node)
            tree.deleteSubtree(node)

        node.parent = None

    def rmNodeFromParent(self, node: CatalogueItem):
        """Remove a node from all of its parent's structures

        Args:
            node (CatalogueItem): To-be-remove-node
        """
        if node.parent:
            logger.debug(f"Remove node {node} from parent structures.")
            p_children = [ch for ch in node.parent.children if ch != node]
            node.parent.children = tuple(p_children)

            node.parent.dirs_files.removeItemByValue(node)

            if isinstance(node, FileItem):
                node.parent.files.removeItemByValue(node)
            if isinstance(node, DirItem):
                node.parent.dirs.removeItemByValue(node)

    def updateAncestors(
        self,
        node: CatalogueItem,
        dir_list: CatalogueContainer,
    ):
        """Update sizes of all ancestors of a node that has already been removed
        from parent's structures. Update ancestors in global directory list.

        Since in the underlying sorted list in the container objects references are kept,
        updating an item takes removing it, then updating the
        item and then inserting it againg. Updating it when the object
        is still in the list leads to the reference in the list not
        representing the new object, so new object cannot be found
        in the list.

        Args:
            node (CatalogueItem): removed node
            dir_list (CatalogueContainer): global directory list
        """
        logger.debug(f"Update ancestors of {node}")
        parent = node.parent
        while parent:
            logger.debug(
                f"Updating size of ancestor {parent}. Current size {parent.size}"
            )

            try:
                dir_list.removeItemByValue(parent)
            except ValueError as ve:
                logger.error(f"Error removing item from dir container: {ve}")

            grand_parent = parent.parent

            if grand_parent:

                grand_parent.dirs_files.removeItemByValue(parent)
                grand_parent.dirs.removeItemByValue(parent)

                parent.calcSetDirSize()

                grand_parent.dirs.addItem(parent)
                grand_parent.dirs_files.addItem(parent)

            else:
                parent.calcSetDirSize()
                logger.debug(f"No grand parent for {node}")

            dir_list.addItem(parent)

            node = parent
            parent = parent.parent

    def findByID(self, iid: str) -> Optional[CatalogueItem]:
        """Find node by its iid string and return it.

        Args:
            iid (str): iid

        Returns:
            Optional[CatalogueItem]: item or None
        """
        item = find_by_attr(self.root_node, iid, name="iid")
        if item:
            return item
        else:
            return None
