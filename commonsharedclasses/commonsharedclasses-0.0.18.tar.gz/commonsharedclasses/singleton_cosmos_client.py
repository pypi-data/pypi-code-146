from .singleton import Singleton
from azure.cosmos import CosmosClient

class SingletonCosmosClient(metaclass=Singleton):

    """
        Class that creates, maintains and serves singleton CosmosClient, primary functionality
        of this is to makes sure that for any <host,masterkey> combination has a single client
    """

    def __init__(self, host, master_key):
        self.client = CosmosClient(host, credential=master_key,
                            retry_total=10,
                            retry_backoff_max=60, retry_backoff_factor=0.5)