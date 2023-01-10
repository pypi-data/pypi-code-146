import os
from typing import List, Optional

import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting import numberFormat, set_frozen, textFormat
from gspread_formatting.dataframe import (
    BasicFormatter,
    cellFormat,
    format_with_dataframe,
)


def get_authorized_client() -> gspread.client.Client:  # type: ignore
    """
    Get authorized client

    Returns:
        gspread.client.Client: authorized client
    """
    if env_credentials := os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH"):
        return gspread.service_account(filename=env_credentials)
    else:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_PATH not set in environment")


def open_spreadsheet(  # type: ignore [no-any-unimported]
    spreadsheet_key: str,
) -> gspread.spreadsheet.Spreadsheet:
    """Open Google spreadsheet

    Args:
        spreadsheet_key (str): the key of the spreadsheet to open

    Returns:
        gspread.spreadsheet.Spreadsheet: the spreadsheet
    """

    gc = get_authorized_client()
    return gc.open_by_key(spreadsheet_key)


def open_worksheet(  # type: ignore [no-any-unimported]
    spreadsheet_key: str,
    worksheet_number: int = 0,
    worksheet_name: Optional[str] = None,
) -> gspread.worksheet.Worksheet:

    """
    Open Google worksheet

    Args:
        spreadsheet_key (str): Key of the spreadsheet to open.
        worksheet_number (int): _description_. Defaults to 0.
        worksheet_name (str, optional): Defaults to None.

    Returns:
        gspread.spreadsheet.Spreadsheet: the spreadsheet
    """
    gc = get_authorized_client()

    if worksheet_name:
        return gc.open_by_key(spreadsheet_key).worksheet(worksheet_name)

    else:
        return gc.open_by_key(spreadsheet_key).get_worksheet(worksheet_number)


def create_gspreadsheet(  # type: ignore [no-any-unimported]
    title: str, folder_id: str, locale: str = "no_NO"
) -> gspread.spreadsheet.Spreadsheet:
    """Create a new spreadsheet

    Args:
        title (str): Title of the spradsheet
        folder_id (str): the folder to create the spreadsheet in

    Returns:
        gspread.spreadsheet.Spreadsheet: The created spreadsheet
    """

    gc = get_authorized_client()
    sheet = gc.create(title, folder_id)
    sheet.update_locale(locale)
    return sheet


def open_or_create_spreadsheet(  # type: ignore [no-any-unimported]
    title: str, folder_id: str, locale: str = "no_NO"
) -> gspread.spreadsheet.Spreadsheet:
    """Open or create a spreadsheet

    Args:
        title (str): Title of the spradsheet
        folder_id (str): the folder to create the spreadsheet in
        locale (str, optional): Locale of the spreadsheet. Defaults to "no_NO".

    Returns:
        gspread.spreadsheet.Spreadsheet: The created spreadsheet
    """

    gc = get_authorized_client()
    try:
        return gc.open(title, folder_id)
    except gspread.exceptions.SpreadsheetNotFound:
        return create_gspreadsheet(title, folder_id, locale)


def create_worksheet(  # type: ignore [no-any-unimported]
    spreadsheet_key: str, title: str
) -> gspread.worksheet.Worksheet:
    """Create a new worksheet

    Args:
        spreadsheet_key (str): Key of the spreadsheet to open.
        title (str): Title of the worksheet

    Returns:
        gspread.worksheet.Worksheet: The created worksheet
    """

    gc = get_authorized_client()
    return gc.open_by_key(spreadsheet_key).add_worksheet(title)


def open_or_create_worksheet(  # type: ignore [no-any-unimported]
    spreadsheet: gspread.spreadsheet.Spreadsheet, title: str
) -> gspread.worksheet.Worksheet:
    """Open or create a worksheet

    Args:
        spreadsheet_key (str): Key of the spreadsheet to open.
        title (str): Title of the worksheet

    Returns:
        gspread.worksheet.Worksheet: The created worksheet
    """

    try:
        return spreadsheet.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        return spreadsheet.add_worksheet(title)


def save_dataframe_to_worksheet(  # type: ignore [no-any-unimported]
    dataframe: pd.DataFrame,
    spreadsheet_title: str,
    folder_id: str,
    worksheet_title: str,
    locale: str = "no_NO",
    include_index: bool = True,
    include_column_header: bool = True,
    resize: bool = True,
    allow_formulas: bool = True,
    overwrite: bool = True,
) -> gspread.worksheet.Worksheet:
    """Set worksheet with pandas DataFrame

    Args:
        dataframe (pd.DataFrame): the DataFrame to set
        title (str): Title of the spradsheet
        folder_id (str): the folder to create the spreadsheet in
        locale (str, optional): Locale of the spreadsheet. Defaults to "no_NO".
        include_index (bool, optional): include index in DataFrame. Defaults to True.
        include_column_header (bool, optional): include column header in DataFrame.
            Defaults to True.
        resize (bool, optional): resize worksheet to fit DataFrame. Defaults to True.
        allow_formulas (bool, optional): allow formulas in DataFrame. Defaults to True.
        overwrite (bool, optional): overwrite existing data. Defaults to True.
    """

    spreadsheet = open_or_create_spreadsheet(spreadsheet_title, folder_id, locale)
    worksheet = open_or_create_worksheet(spreadsheet, worksheet_title)

    if overwrite:
        worksheet.clear()
    else:
        # don't include column header if we don't overwrite
        include_column_header = False

    set_with_dataframe(
        worksheet,
        dataframe,
        include_index=include_index,
        include_column_header=include_column_header,
        resize=resize,
        allow_formulas=allow_formulas,
    )

    return worksheet


def get_worksheet_as_dataframe(  # type: ignore [no-any-unimported]
    spreadsheet_key: str,
    worksheet_number: int = 0,
    worksheet_name: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch Google spreadsheet as records

    Args:
        spreadsheet_key (str): Google spreadsheet key
        worksheet_number (int): Sheet number
        worksheet_name (str): Sheet name

      Returns:
        pd.DataFrame: DataFrame of the sheet
    """

    worksheet = open_worksheet(spreadsheet_key, worksheet_number, worksheet_name)

    return get_as_dataframe(worksheet)


def format_worksheet(  # type: ignore [no-any-unimported]
    worksheet: gspread.worksheet.Worksheet,
    df: pd.DataFrame,
    text_columns: Optional[List[str]] = None,
    bold_text_columns: Optional[List[str]] = None,
    date_columns: Optional[List[str]] = None,
    date_time_columns: Optional[List[str]] = None,
    int_columns: Optional[List[str]] = None,
    float_columns: Optional[List[str]] = None,
    frozen_columns: int = 0,
) -> None:
    """_summary_

    Args:
        worksheet (gspread.worksheet.Worksheet): the worksheet to format
        df (pd.DataFrame): the dataframe to use
        text_columns (Optional[List[str]], optional): columns containing text.
            Defaults to None.
        bold_text_columns (Optional[List[str]], optional): columns that should be bold.
            Defaults to None.
        date_columns (Optional[List[str]], optional): columns of dates.
            Defaults to None.
        date_time_columns (Optional[List[str]], optional): columns of date times.
            Defaults to None.
        int_columns (Optional[List[str]], optional): columns of ints.
            Defaults to None.
        float_columns (Optional[List[str]], optional): columns of floats.
            Defaults to None.
        frozen_columns (int, optional): _description_. Defaults to 0.
    """

    norwegian_number_format = numberFormat(
        "NUMBER", "[<10000]#####; [>99999] ### ###; ### ###"
    )
    norwegian_number_format_decimal = numberFormat(
        "NUMBER", "[<10000]#####0.00; [>99999] ### ###0.00; ### ###0.00"
    )

    column_formats = (
        {
            column: cellFormat(
                horizontalAlignment="LEFT",
                wrapStrategy="WRAP",
            )
            for column in text_columns or []
        }
        | {
            column: cellFormat(
                horizontalAlignment="LEFT",
                wrapStrategy="WRAP",
                textFormat=textFormat(bold=True),
            )
            for column in bold_text_columns or []
        }
        | {
            column: cellFormat(
                numberFormat=numberFormat("DATE_TIME", "yyyy-mm-dd"),
                horizontalAlignment="LEFT",
            )
            for column in date_columns or []
        }
        | {
            column: cellFormat(
                numberFormat=numberFormat("DATE_TIME", "yyyy-mm-dd hh:mm:ss"),
                horizontalAlignment="LEFT",
            )
            for column in date_time_columns or []
        }
        | {
            column: cellFormat(
                numberFormat=norwegian_number_format,
                horizontalAlignment="RIGHT",
            )
            for column in int_columns or []
        }
        | {
            column: cellFormat(
                numberFormat=norwegian_number_format_decimal,
                horizontalAlignment="RIGHT",
            )
            for column in float_columns or []
        }
    )

    formatter = BasicFormatter.with_defaults(
        freeze_headers=True, column_formats=column_formats
    )

    format_with_dataframe(
        worksheet,
        df,
        formatter=formatter,
        include_index=False,
        include_column_header=True,
    )

    if frozen_columns > 0:
        set_frozen(worksheet, cols=frozen_columns)


# TODO: add conditinonal formatting
