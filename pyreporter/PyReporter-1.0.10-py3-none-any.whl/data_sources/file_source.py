from .abs_source import AbsSource
from .df_processor import DFProcessor
import glob, enum, os
from typing import Optional


# FileExtensions: Different types of file extensions
class FileExtensions(enum.Enum):
    NewExcel = "xlsx"
    OldExcel = "xls"


# FileSource: Class for a source from a file
class FileSource(AbsSource):
    """
    This Class inherits from :class:`~Reporter.data_sources.abs_source.AbsSource`
    

    A data source for importing raw data from a file location

    Attributes
    ----------
    post_processor: Optional[:class:`~Reporter.data_sources.df_processor.DFProcessor`]
        the procesor used to transform the imported raw table from the source

        **Default**: ``None``
    """
    def __init__(self, path: str, post_processor: Optional[DFProcessor] = None):
        super().__init__(post_processor)
        self._path = path


    # path(): Getter for 'path'
    @property
    def path(self):
        """
            The file path to the data source

                **Type:** :class:`str`
        """
        return self._path


    # path(): Setter to check if 'new_path' exists
    @path.setter
    def path(self, new_path: str):
        """
        setting a new file path to the data source
        """
        glob_result = glob.glob(new_path)

        # get the latest file if we have multiple files that match the globbing result
        if (glob_result):
            latest_file = max(glob_result, key=os.path.getctime)
            self._path = latest_file
