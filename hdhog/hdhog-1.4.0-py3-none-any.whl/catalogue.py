from typing import Tuple, List

from .tree import Tree, FSTree
from .container import CatalogueContainer
from .fsaction import FSActionDelete
from .logger import logger


class Catalogue:
    """This represents the walking of the directory tree and holding the resulting
    information, as well as actions taken on catalogue items, i.e. files and directories.
    This class holds three structures / elements:
        1. A CatalogueContainer for files, which is just for file-based sorting
        2. A CatalogueContainer for directories, which is just for
        directory-based sorting
        3. The FSTree. Nodes in the tree are
        FileItems or DirItems which inherit from anytree's NodeMixin.
        Each node in turn holds CatalogueContainers for holding children
        items.
    """

    def __init__(self, hash_files=False):
        # self.filter_checks = []
        # self.files = CatalogueContainer()
        # self.dirs = CatalogueContainer()
        self.tree = FSTree()
        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()
        self.mirror_trees = []
        self.num_files = 0
        self.num_dirs = 0
        self.total_space = 0
        self.hash_files = hash_files

    def registerMirrorTrees(self, trees: List[Tree]):
        self.mirror_trees.extend(trees)

    def createCatalogue(self, start):
        """Have the directory tree built up as structure and put items into containers.

        Args:
            start (str, optional): Top directory.
        """

        self.files = CatalogueContainer()
        self.dirs = CatalogueContainer()
        self.tree = FSTree()
        self.num_files = 0
        self.num_dirs = 0
        self.total_space = 0

        logger.info("Start creating catalogue (bottom up).")

        try:
            for parent_item, file_items in self.tree.treeFromFSBottomUp(start=start):
                self.num_dirs += 1
                self.num_files += len(file_items)

                self.dirs.addItem(parent_item)
                for item in file_items:
                    self.files.addItem(item)
                for tree in self.mirror_trees:
                    tree.insertDirItem(parent_item)

            # minus top dir
            self.num_dirs -= 1

        except Exception as e:
            logger.error(f"Error when walking the directory tree: {e}")

        self.total_space = self.tree.root_node.size

        logger.info("Finished creating catalogue.")

    # def addFilterCheck(self, filter_check: FilterCheck):
    #     """Register a check object.

    #     Args:
    #         filter_check (FilterCheck): Check object
    #     """

    #     # check if a check of that kind was already added
    #     if self.filter_checks:
    #         for ix, registered_check in enumerate(self.filter_checks):
    #             if type(filter_check) == type(registered_check):
    #                 del self.filter_checks[ix]

    #     self.filter_checks.append(filter_check)

    def deleteByIDs(self, selection: Tuple[str]):
        """Executes a files system action on file or directory paths.

        Remove the items representing the paths from the respective
        containers.
        Update the tree:
            Remove the nodes and recalculate the parent's, grand parent's
            etc. sizes up the tree

        Args:
            fs_action (Action): Action object
            paths (List[str]): full paths to files or dirs
        """
        logger.debug(f"Deleting iids {selection} from tree.")
        # reverse sort, so greatest iids, i.e. "oldest ancestors"
        # are deleted first which potentially deletes
        # smaller iids in the list if they are their children
        # and also guaranteeing that ancestors are not updated multiple
        # times by their descendants (e.g. by a file and then by it's parent
        # folder)
        for iid in sorted(selection, reverse=True):
            item = self.tree.findByID(f"{iid}")

            if item:
                self.tree.deleteSubtree(item, self.files, self.dirs, self.mirror_trees)

                # in case an item has been deleted on disk by the user / os
                try:
                    fs_action = FSActionDelete()
                    fs_action.execute(item)
                except FileNotFoundError as fne:
                    logger.error(
                        f"Cannot delete item since it does not seem to exist anymore: {fne}"
                    )

        self.num_files = len(self.files)
        self.num_dirs = len(self.dirs) - 1  # minus top dir
        if self.tree.root_node:
            self.total_space = self.tree.root_node.size
        else:
            self.total_space = 0


# class FilterCheck(ABC):
#     """This is the ABC class for a filter check used
#     when walking the directory tree in the Catalogue.
#     """

#     @abstractclassmethod
#     def check(self, filepath: str):
#         pass


# class FilterCheckFileExt(FilterCheck):
#     def __init__(self, extensions: List[str]):
#         self.extensions = extensions

#     def check(self, filepath: str):
#         fname, ext = os.path.splitext(filepath)

#         if ext.strip(".") in self.extensions:
#             return False
#         else:
#             return True
