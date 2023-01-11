"""google related api comment"""

from __future__ import print_function
import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
# DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

def google_credential_oauth(oauth_json_def, token_json_def):
    """Create credentials if using OAUTH"""
    SCOPES = ['https://www.googleapis.com/auth/drive'
                , 'https://www.googleapis.com/auth/drive.file'
                , 'https://www.googleapis.com/auth/spreadsheets'
                , 'https://www.googleapis.com/auth/spreadsheets.readonly'
                , 'https://www.googleapis.com/auth/documents'
                , 'https://www.googleapis.com/auth/documents.readonly'
            ]
    # OAUTH_FILE = """/Volumes/GoogleDrive/My Drive/work/code/py/oauth2.json"""
    # TOKEN_FILE = """/Volumes/GoogleDrive/My Drive/work/code/py/token.json"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_json_def):
        creds = Credentials.from_authorized_user_file(token_json_def, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                oauth_json_def, SCOPES)
            creds = flow.run_local_server(port = 0)
        # Save the credentials for the next run
        with open(token_json_def, 'w', encoding = "utf-8") as token:
            token.write(creds.to_json())
    return creds

def google_credential_service(service_json_def):
    """Create credentials if using service account"""
    SCOPES = ['https://www.googleapis.com/auth/drive'
                , 'https://www.googleapis.com/auth/drive.file'
                , 'https://www.googleapis.com/auth/spreadsheets'
                , 'https://www.googleapis.com/auth/spreadsheets.readonly'
                , 'https://www.googleapis.com/auth/documents'
                , 'https://www.googleapis.com/auth/documents.readonly'
            ]
    # SERVICE_ACCOUNT_FILE = """/Volumes/GoogleDrive/My Drive/work/code/py/service_account.json"""
    credentials = service_account.Credentials.from_service_account_file(service_json_def, scopes = SCOPES)
    creds = credentials
    return creds

def google_get_data_gsheet(creds_def, sheet_id_def, range_name_def):
    """get data from google sheet"""
    try:
        service = build('sheets', 'v4', credentials = creds_def) # build the service for google sheets
        # Call the Sheets API
        sheet = service.spreadsheets() # sheets api
        result = sheet.values().get(
                                    spreadsheetId = sheet_id_def
                                    , range = range_name_def
                                ).execute() # execute the get command
        values = result.get('values', []) # get the value
        if not values:
            print('No data found.') # warning if connection error
    except HttpError as err:
        print(err)
    df_def = pd.DataFrame(values) # put values into dataframe
    df_def.columns = df_def.iloc[0,:] # make the first line as column
    df_def = df_def.iloc[1:,:] # make the other line as values
    return df_def

def google_append_data_gsheet(creds_def, sheet_id_def, range_name_def, df_def, include_column_def = False):
    """append data on google sheet"""
    service = build('sheets', 'v4', credentials = creds_def) # build the service for google sheets
    # Call the Sheets API
    sheet = service.spreadsheets() # sheets api
    result = sheet.values().get(
                                spreadsheetId = sheet_id_def
                                ,range=range_name_def
                            ).execute() # execute the get command
    if include_column_def: # if you want to include the column name in the appended sheet
        data = df_def.values.tolist()
        data.insert(0, df_def.columns.values.tolist())
    else: # if you want to append just the content
        data = df_def.values.tolist()
    body = {'values': data} # put the data into body
    result = service.spreadsheets().values().append(
                                                spreadsheetId = sheet_id_def
                                                , body = body
                                                , valueInputOption = 'USER_ENTERED'
                                                , insertDataOption = 'OVERWRITE'
                                                , range = range_name_def
                                            ).execute() # execute the command to append file
    return result # return the response

def google_clear_data_gsheet(creds_def, sheet_id_def, range_name_def):
    """clear data from google sheet"""
    service = build('sheets', 'v4', credentials = creds_def) # build the service for google sheets
    result = service.spreadsheets().values().clear(
                                                spreadsheetId = sheet_id_def
                                                , range = range_name_def
                                            ).execute() # clear the value in google sheet
    return result # return the response

def google_update_data_gsheet(creds_def, sheet_id_def, range_name_def, df_def, include_column_def = False):
    """update data on google sheet"""
    service = build('sheets', 'v4', credentials = creds_def) # build the service for google sheets
    if include_column_def: # if you want to include the column name in the appended sheet
        data = df_def.values.tolist()
        data.insert(0, df_def.columns.values.tolist())
    else: # if you want to append just the content
        data = df_def.values.tolist()
    body = {'values': data} # put the data into body
    result = service.spreadsheets().values().update(
                                                spreadsheetId = sheet_id_def
                                                , body = body
                                                , valueInputOption = 'USER_ENTERED'
                                                , range = range_name_def
                                            ).execute() # execute the command to append file
    return result # return the response
