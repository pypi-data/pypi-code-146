from .singleton import Singleton
from azure.storage.blob import BlobServiceClient

class SingletonBlobServiceClient(metaclass=Singleton):

    """
        Class that creates, maintains and serves singleton BlobServiceClient, primary functionality
        of this is to makes sure that for any <storage_url,account_key> combination has a single client
    """

    def __init__(self, storage_url, account_key):
        self.client = BlobServiceClient(storage_url, credential=account_key)