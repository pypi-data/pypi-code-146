import io
import os.path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class BotGoogleDrivePlugin:
    def __init__(self, credentials_file_path: str):
        """
        BotGoogleDrivePlugin.

        Args:
            credentials_file_path: The path of the credentials json file
                obtained at Google Cloud Platform.
        """
        # Credentials
        self.creds = None
        self.drive_service = None
        self.scopes = ['https://www.googleapis.com/auth/drive']

        # The file token_drive.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        credentials_dir = os.path.abspath(os.path.dirname(credentials_file_path))

        if os.path.exists(os.path.join(credentials_dir, 'token_drive.json')):
            self.creds = Credentials.from_authorized_user_file(
                os.path.join(credentials_dir, 'token_drive.json'), self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.abspath(credentials_file_path), self.scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(credentials_dir, 'token_drive.json'), 'w') as token:
                token.write(self.creds.to_json())

        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def search_file_by_name(self, filename: str) -> str:
        """
        Searches for a file on google drive by the file name.

        Args:
            filename: The exact name of the file to be fetched.

        Returns:
            The id of the file found.
        """
        page_token = None
        while True:
            response = self.drive_service.files().list(q=f"name='{filename}' and mimeType !=\
                                                          'application/vnd.google-apps.folder'",
                                                       spaces='drive',
                                                       fields='nextPageToken, files(id, name)',
                                                       pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                return file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return None

    def download_file(self, file_id: str, file_path: str) -> None:
        """
        Download a file stored on Google Drive.

        Args:
            file_id: Id of the file to be downloaded.
            file_path: Path where the file will be saved.
        """
        request = self.drive_service.files().get_media(fileId=file_id)
        with io.FileIO(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                done = downloader.next_chunk()

    def export_file(self, file_id: str, file_path: str, mime_type: str) -> None:
        """
        Download a Google Workspace Document stored on Google Drive.

        Args:
            file_id: Id of the file to be downloaded.
            file_path: Path where the file will be saved.
            mime_type: MIME type corresponding to the Google Workspace document to be downloaded.
        """
        # Exports and saves the document in the format defined by the mime type
        request = self.drive_service.files().export_media(fileId=file_id, mimeType=mime_type)
        with io.FileIO(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                done = downloader.next_chunk()

    def delete_file(self, file_id: str) -> None:
        """
        Delete a file stored on Google Drive.

        Args:
            file_id: Id of the file to be deleted.
        """
        self.drive_service.files().delete(fileId=file_id).execute()

    def create_folder(self, folder_name: str) -> str:
        """
        Create a folder on Google Drive.

        Args:
            folder_name: Name of the folder to be created.

        Returns:
            The id of the created folder.
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().create(body=file_metadata,
                                                 fields='id').execute()
        return file.get('id')

    def upload_file(self, file_path: str, file_name: str,
                    parent_folder_id: Optional[str] = None, mime_type: Optional[str] = None):
        """
        Upload a file on Google Drive.

        Args:
            file_path: Path to the file to be used.
            file_name: Name of the file that will be displayed on the drive.
            parent_folder_id: Id of the folder that will receive the file,
                              otherwise it will be uploaded to the main folder.
            mime_type: The MIME type corresponding to the file if necessary.
        """
        file_metadata = {'name': file_name}

        # Checking folder_id parameter
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        # Checking mime_type parameter
        if mime_type:
            media = MediaFileUpload(file_path, mimetype=mime_type)
        else:
            media = MediaFileUpload(file_path)

        response = self.drive_service.files().create(body=file_metadata,
                                                     media_body=media,
                                                     fields='id').execute()
        if response:
            return response.get("id", None)
        return None

    def search_folder_by_name(self, folder_name: str) -> str:
        """
        Searches for a folder on google drive by the folder name.

        Args:
            folder_name: The exact name of the folder to be fetched.

        Returns:
            The id of the folder found.
        """
        page_token = None
        while True:
            response = self.drive_service.files().list(q=f"name='{folder_name}' and\
                                                           mimeType = 'application/vnd.google-apps.folder'",
                                                       spaces='drive',
                                                       fields='nextPageToken, files(id, name)',
                                                       pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                return (file.get('id'))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return None

    def get_files_from_parent_folder(self, parent_folder_id: str) -> List:
        """
        Searches for every file and folder inside a parent folder.

        Args:
            parent_folder_id: The id of the folder containing the files to be returned.

        Returns:
            The list of found ids.
        """
        subfiles_id = []
        page_token = None
        while True:
            response = self.drive_service.files().list(q=f"'{parent_folder_id}' in parents",
                                                       spaces='drive',
                                                       fields='nextPageToken, files(id, name)',
                                                       pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                subfiles_id.append(file.get('id'))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return subfiles_id
