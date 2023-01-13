from ..file_source import FileSource
import pandas as pd
from ..sharepoint import SharePoint
from pathlib import Path
import io
from ..df_processor import DFProcessor
from typing import Optional, Union, Dict


# ExcelSource: Imports a table from excel
class ExcelSource(FileSource):
    """
    This Class inherits from :class:`~Reporter.data_sources.file_source.FileSource`


    Data source that imports raw data from an Excel sheets and files

    Attributes
    ----------
    post_processor: Optional[Union[Dict[str, :class:`~Reporter.data_sources.df_processor.DFProcessor`], :class:`~Reporter.data_sources.df_processor.DFProcessor`]]
        the processors used to transform the raw imported table

        **Default**: ``None``

    _engine: :class:`str`
        The name of the Excel engine used to manipulate Excel files

        **Default**: "openpyxl"
    """
    def __init__(self, path: str, sheet: Optional[str] = None, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None):
        super().__init__(path, post_processor)
        self._sheet = sheet

        # default to get first sheet if the sheet is not specified
        if (self._sheet is None):
            self._sheet = 0

        self._engine = "openpyxl"


    # sheet(): Getter for '_sheet'
    @property
    def sheet(self):
        """
            the sheet where the target table to load is located.

            When this parameter is set to ``None``, then the first sheet of the Excel
            file will be used

            **Default**: ``None``

            **Type:** Optional[:class:`str`]
        """
        return self._sheet


    # sheet(): Setter for '_sheet'
    @sheet.setter
    def sheet(self, new_sheet):
        self._sheet = new_sheet


    # import_data(): Imports the table from excel
    async def import_data(self) -> pd.DataFrame:
        """
        The method used to import the required table from the Excel file

        Returns
        -------
        `DataFrame`_
            The resultant imported Excel table
        """
        # open from local file path
        df = pd.read_excel(self._path, sheet_name = self._sheet, parse_dates = True)

        return df
