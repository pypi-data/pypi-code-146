from .singleton_blob_service_client import SingletonBlobServiceClient
from pydantic import validate_arguments

class BlobServiceConnection():
    
    """
        An utility class to perform cosmos operations using the SingletonCosmosClient instance
    """
    def __init__(self, storage_url: str, account_key: str):
        self.blob_service_client = SingletonBlobServiceClient(storage_url=storage_url, account_key=account_key).client

    def get_blob_service_client(self):
        return self.blob_service_client

    @validate_arguments
    def set_blob_client(self, container: str, blob: str):
        self.blob_client = self.blob_service_client.get_blob_client(container=container, blob=blob)

    @validate_arguments
    def get_blob_client(self):
        return self.blob_client

    @validate_arguments
    def upload(self, data):
        self.blob_client.upload_blob(data)