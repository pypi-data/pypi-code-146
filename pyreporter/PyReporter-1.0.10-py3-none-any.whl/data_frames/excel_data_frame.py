import pandas as pd
import copy
from ..tools import DataFrameTools as DfTools
from .abs_source_data_frame import AbsSourceDf


# ExcelDf: Class to store dataframe sources for an excel
class ExcelDf(AbsSourceDf):
    """
    This Class inherits from :class:`~Reporter.data_frames.abs_source_data_frame.AbsSourceDf`

    A class to store the dataframe and any associated metadata for a table to be
        written to an Excel file

    Attributes
    ----------
    startrow: :class:`int`
        The row index for the top-left corner of the table

        **Default**: 0

    startcol: :class:`int`
        The column index for the top-left corner of the table

        **Default**: 0

    with_header: :class:`bool`
        Whether we want to display the table column names on the excel sheet

        **Default**: ``True``

    src_to_celled: :class:`bool`
        Whether we want to contain each cell in the source data table to be a :class:`~Reporter.data_frames.cell.Cell`

        **Default**: ``True``

    display_df: `DataFrame`_
        The source table to display in the output
    """
    def __init__(self, df: pd.DataFrame, startrow: int = 0, startcol: int = 0, with_headers: bool = True, src_to_celled: bool = True):
        super().__init__(df)

        # if we need to convert each datacell in the source data frame to a Cell object
        if (src_to_celled):
            self.df = DfTools.df_to_celled_df(self.df)

        self.display_df = copy.deepcopy(self.df)
        self.display_df = DfTools.celled_df_to_display_df(self.display_df)

        # left hand corner position of the dataframe
        self.startrow = startrow
        self.startcol = startcol

        # flags for including the header of the dataframe
        self.with_headers = with_headers
