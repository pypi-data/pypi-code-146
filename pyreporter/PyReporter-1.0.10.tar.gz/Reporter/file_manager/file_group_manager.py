from .file_manager import FileManager
from ..exceptions.file_except import NonExistentFileError
from typing import List


# FileGroupManager: Manages a group of files
class FileGroupManager():
    """
    A class to manage a group of files

    Attributes
    ----------
    file_managers: List[:class:`Reporter.file_manager.file_manager.FileManager`]
        list of file managers to handle file management for each file
    """
    def __init__(self, file_managers: List[FileManager]):
        self._file_managers = file_managers


    # copy(): Copies a group of files from '_src' to '_dest'
    def copy(self):
        """
        Copies a group of files from their source location to their desired destinations
        """
        for f in self._file_managers:
            try:
                f.copy()
            except NonExistentFileError as e:
                pass
