from .singleton_cosmos_client import SingletonCosmosClient
from pydantic import validate_arguments

class CosmosConnection():
    
    """
        An utility class to perform cosmos operations using the SingletonCosmosClient instance
    """
    def __init__(self, host: str, master_key: str):
        self.host_client = SingletonCosmosClient(host=host, master_key=master_key).client

    def get_database_client(self):
        return self.db_client

    def get_container_client(self):
        return self.container_client

    @validate_arguments
    def set_database(self, db_name: str):
        self.db_client = self.host_client.get_database_client(db_name)

    @validate_arguments
    def set_container(self, container_name: str):
        self.container_client = self.db_client.get_container_client(container_name)

    @validate_arguments
    def query(self, query: str):
        items = list(self.container_client.query_items(query=query, enable_cross_partition_query=True, max_item_count=100))
        return items

    @validate_arguments
    def upsert(self, item: dict):
        self.container_client.upsert_item(item)

    @validate_arguments
    def delete(self, document, partitionKey):
        return self.container_client.delete_item(document, partitionKey)