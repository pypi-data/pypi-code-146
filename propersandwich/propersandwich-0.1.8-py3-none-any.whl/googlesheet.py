"""
This module will help to perform CRUD operations with Google spreadsheets
"""

import pygsheets
import logging
import pandas as pd
import os
from dotenv import load_dotenv

# Load Environment variables
load_dotenv()


def create_worksheet(spreadsheet_url, worksheet_title):
    """
    Create a worksheet in an existing spreadsheet


    :param str spreadsheet_url: The Environment variable containing the URL of the spreadsheet
    :param str worksheet_title: The title of the worksheet

    """

    # Create a client
    google_sheet_client = pygsheets.authorize(service_account_env_var='GOOGLE_API')

    # Open the sheet
    spreadsheet = google_sheet_client.open_by_url(os.getenv(spreadsheet_url))

    # Create a new worksheet
    spreadsheet.add_worksheet(worksheet_title)


def read_worksheet(spreadsheet_url, worksheet_title, start='A1') -> pd.DataFrame:
    """
    Read a worksheet and return it's content as a Dataframe


    :param str spreadsheet_url: The Environment variable containing the URL of the spreadsheet
    :param str worksheet_title: The title of the worksheet
    :param str start: op left cell to load into data frame. (default: A1)

    :returns: The content of the tab
    :rtype: dataframe

    """

    # Create a client
    google_sheet_client = pygsheets.authorize(service_account_env_var='GOOGLE_API')

    # Open the sheet
    spreadsheet = google_sheet_client.open_by_url(os.getenv(spreadsheet_url))

    # Select the worksheet
    worksheet = spreadsheet.worksheet_by_title(worksheet_title)

    # Get the content of this worksheet as a pandas data frame.
    data = worksheet.get_as_df(start=start)

    logging.info(f"Retrieved {len(data.index)} rows from [ {worksheet.title} / {spreadsheet.title} ]")

    return data

def update_worksheet(spreadsheet_url, worksheet_title, data, start='A1', copy_head=True, extend=False, fit=False):
    """
    update a worksheet with the values from a dataframe


    :param str spreadsheet_url: The Environment variable containing the URL of the spreadsheet
    :param str worksheet_title: The title of the worksheet
    :param pd.Dataframe data: The data to update the worksheet with
    :param str start: Address of the top left corner where the data should be added.
    :param bool copy_head: Copy header data into first row
    :param bool extend: Add columns and rows to the worksheet if necessary, but won’t delete any rows or columns.
    :param bool fit: Resize the worksheet to fit all data inside if necessary.

    """

    # Create a client
    google_sheet_client = pygsheets.authorize(service_account_env_var='GOOGLE_API')

    # Open the sheet
    spreadsheet = google_sheet_client.open_by_url(os.getenv(spreadsheet_url))

    # Find and Update the worksheet ( create it if it doesn't exist )
    try:
        spreadsheet.worksheet_by_title(worksheet_title)
    except pygsheets.exceptions.WorksheetNotFound as error:
        spreadsheet.add_worksheet(worksheet_title)
        logging.info(f"{worksheet_title} has been created")

    worksheet = spreadsheet.worksheet_by_title(worksheet_title)
    worksheet.set_dataframe(data, start=start, copy_head=copy_head, extend=extend, fit=fit)



def delete_worksheet(spreadsheet_url, worksheet_title):
    """
    Delete a worksheet in an existing spreadsheet


    :param str spreadsheet_url: The Environment variable containing the URL of the spreadsheet
    :param str worksheet_title: The title of the worksheet

    """

    # Create a client
    google_sheet_client = pygsheets.authorize(service_account_env_var='GOOGLE_API')

    # Open the sheet
    spreadsheet = google_sheet_client.open_by_url(os.getenv(spreadsheet_url))

    # Select the worksheet
    worksheet = spreadsheet.worksheet_by_title(worksheet_title)

    # Delete a worksheet by title
    spreadsheet.del_worksheet(worksheet)


