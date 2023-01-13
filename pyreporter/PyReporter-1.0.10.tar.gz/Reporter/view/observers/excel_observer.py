import openpyxl as pyx
import pandas as pd
from .observer import Observer
from ...tools import Excel, ExcelStyles, ExcelAlignment, ColourList
from ...tools import DataFrameTools as DfTools
from ...data_frames import ExcelDf
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, Alignment, Border, PatternFill, Side
from openpyxl.styles.colors import Color
from openpyxl.cell.cell import Cell
import openpyxl.utils as pyx_tools
from ...events import OutEvent, ExcelExportEvent
from ...events.progress_event import *
from typing import Union, List, Tuple, Optional, Dict, Any


# preset widths for the calendar entries
PAST_CALENDAR_WIDTH = 16
CURRENT_CALENDAR_WIDTH = 13


class ExcelObserver(Observer):
    def __init__(self):
        # =========================INITIALIZATION ==============================
        # excel utility to help us write to the excel file
        self.excel = None
        self._writer = None
        self._sheets = None

        # ====================================================================


    # notify(target): Updates changes to the current excel file based off 'out_event'
    def notify(self, out_event: ExcelExportEvent):
        # write all our dataframes into the excel sheet
        export_info = out_event.export()
        self.excel = export_info.excel_tool
        self._writer = export_info.writer
        self._sheets = export_info.sheets

        self.excel.save_current_file()
