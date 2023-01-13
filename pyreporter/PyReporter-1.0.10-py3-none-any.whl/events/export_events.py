import pandas as pd
from .out_event import OutEvent
from ..data_frames import AbsSourceDf, ExcelDf
from ..tools import Excel
from openpyxl.worksheet.worksheet import Worksheet
from typing import List, Dict, Union


# our engine used to write into excel
EXCEL_WRITER_ENGINE = "openpyxl"


# ExcelExportInfo: Class to store information when exporting dataframes to an excel
class ExcelExportInfo():
    """
    A class to store information regarding exporting `DataFrame`_ to Excel

    Attributes
    ----------
    excel_tool: :class:`Reporter.tools.excel.Excel`
        Utilities to help with manipulation of an Excel file

    writer: `ExcelWriter`_
        The excel writer for writing the data table to Excel

    sheets: Dict[:class:`str`, `Worksheet`_]
        The associated sheets for the Excel file

        **Dict Keys**: The name of the worksheet

        **Dict Values**: The associated worksheet
    """
    def __init__(self, excel_tool: Excel, writer: pd.ExcelWriter, sheets: Dict[str, Worksheet]):
        self.excel_tool = excel_tool
        self.writer = writer
        self.sheets = sheets



# ExportEvent: Event for exporting DataFrames to a certain generic output format
class ExportEvent(OutEvent):
    """
    This Class inherits from :class:`~Reporter.event.out_event.OutEvent`

    An event to help with the export of dataframes to another format

    Attributes
    ----------

    src: Union[List[:class:`~Reporter.data_frames.abs_source_data_frame.AbsSourceDf`], Dict[:class:`str`, List[:class:`~Reporter.data_frames.abs_source_data_frame.AbsSourceDf`]]]
        The source tables to export

    loc: :class:`str`
        The location to export the tables
    """
    def __init__(self, src: Union[List[AbsSourceDf], Dict[str, List[AbsSourceDf]]], loc: str):
        self.src = src
        self.loc = loc


# ExcelExportEvent: Event for exporting DataFrames to Excel
class ExcelExportEvent(ExportEvent):
    """
    This Class inherits from :class:`~Reporter.export_events.ExcelExportEvent`

    An event to help exporting dataframes to an Excel file

    Attributes
    ----------
    excel_df_table: Dict[:class:`str`, List[:class:`~Reporter.data_frames.excel_data_frame.ExcelDf`]]
        The source tables to be exported

        **Dict Keys**: The name of the Excel sheet

        **Dict Values**: The source tables that are to be exported to corresponding sheet

    loc: :class:`str`
        The file location of the Excel file
    """
    def __init__(self, excel_df_table: Dict[str, List[ExcelDf]], loc: str):
        super().__init__(excel_df_table, loc)
        self.excel_tool = Excel(loc)


    # export(): exports the list of dataframes to an excel sheet
    def export(self) -> ExcelExportInfo:
        """
        exports the source tables to an Excel file

        Returns
        -------
        :class:`~Reporter.events.export_events.ExcelExportInfo`
            The resultant metadata after writing the tables to the Excel file
        """
        # get the excel writer for editting/writing into the excel file
        writer = pd.ExcelWriter(self.excel_tool.loc, engine=EXCEL_WRITER_ENGINE)
        self.excel_tool.workbook = writer.book

        sheet_dict = {}
        # output the corresponding tables to each of the sheets in the report
        for sheet_name in self.src:
            sheet = self.excel_tool.create_sheet(sheet_name)
            writer.sheets[sheet_name] = sheet
            sheet_dict[sheet_name] = sheet

            current_df_lst = self.src[sheet_name]
            for excel_df in current_df_lst:
                excel_df.display_df.to_excel(writer, sheet_name=sheet_name, startrow=excel_df.startrow , startcol=excel_df.startcol, header = excel_df.with_headers, index = False)

        return ExcelExportInfo(self.excel_tool, writer, sheet_dict)
