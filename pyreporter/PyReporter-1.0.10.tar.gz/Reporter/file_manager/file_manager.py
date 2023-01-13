import shutil, os
from .file import File
from ..exceptions.file_except import NonExistentFileError

# FileManager(): help manages manipulation of a file
class FileManager():
    """
    A class to help with the management and manipulation of a file

    Attributes
    ----------
    new_source: :class:`str`
        The source path of the file

    new_dest: :class:`str`
        The source destination of the file
    """
    def __init__(self, new_source: str, new_dest: str):
        self._original = File(new_source)
        self._target = File(new_dest)

        self._source = new_source
        self._dest = new_dest


    # exists(): Checks if the original file at 'src' exists
    def exists(self):
        """
        Whether the file exists
        """
        return self._original.exists()


    # source(): Getter for '_source'
    @property
    def source(self):
        """
        **Type**: :class:`str`

            The path to the source file
        """
        return self._source


    # dest(): Getter for '_dest'
    @property
    def dest(self):
        """
        **Type**: :class:`str`

            The path to the file's new destination
        """
        return self._dest


    # source(new_name): Setter for '_source'
    @source.setter
    def source(self, new_name: str):
        self._source = new_name
        self._original.name = new_name


    # dest(new_name): Setter for '_dest'
    @dest.setter
    def dest(self, new_name: str):
        self._dest = new_name
        self._target.name = new_name


    # copy(): Copies the file from '_src' to '_dest'
    # effects: may raise an exception
    def copy(self):
        """
        Copies the file from their source location to their new destination

        Raises
        ------
        :class:`~Reporter.exceptions.file_except.NonExistentFileError`
            If the source file location does not exist
        """
        file = 1

        if (self._target.exists()):
            self._target.remove()

        if (self._original.exists()):
            shutil.copyfile(self._original.name, self._target.name)
        else:
            raise NonExistentFileError(self._source)


    # move(): Moves the file from '_src' to '_dest'
    def move(self):
        """
        Moves the file from its source location to its new destination
        """
        os.replace(self._original.name, self._target.name)
