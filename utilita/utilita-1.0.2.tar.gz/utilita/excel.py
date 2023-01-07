import openpyxl as xl
import pandas as pd
from deprecated import deprecated

def workbook_to_bytes(wb: xl.workbook.workbook.Workbook, lock_worksheets=True):
    if lock_worksheets:
        for x in wb.worksheets:
            x.protection.enable() # always do this before exporting because they automatically become unprotected somehow

    return xl.writer.excel.save_virtual_workbook(wb)

def df_to_worksheet(df: pd.DataFrame, cell: xl.cell.cell.Cell):
    ws = cell.parent

    for r in range(df.shape[0]):
        for c in range(df.shape[1]):
            cell.offset(r+1, c).value = df.iloc[r, c]

@deprecated(version='0.3.0', reason='renamed to df_to_worksheet' )
def df_to_sh(df: pd.DataFrame, cell: xl.cell.cell.Cell):
    df_to_worksheet(df, cell)
