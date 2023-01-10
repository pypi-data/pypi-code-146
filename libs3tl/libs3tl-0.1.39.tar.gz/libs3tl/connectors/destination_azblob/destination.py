from azure.storage.blob import BlobServiceClient
import json

class DestinationAzBlob:
    def __init__(self, jsonData:str, file_name: str, connecting_string: str, container_name: str):
        self._jsonData = jsonData
        self._file_name = file_name
        self._connecting_string = connecting_string
        self._container_name = container_name


    def write(self):
        blob_service_client = BlobServiceClient.from_connection_string(self._connecting_string)
        blob_client = blob_service_client.get_blob_client(container=self._container_name, blob=self._file_name)
        blob_client.upload_blob(self._jsonData)


