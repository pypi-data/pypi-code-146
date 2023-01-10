import os
# from azure.storage.blob import BlobServiceClient
# def compress_json(json_data):
#     return zlib.compress(bytearray(json.dumps(json_data), 'utf-8'))

# def decompress_json(str):
#     return zlib.decompress(json.loads(str))

# from dotenv import load_dotenv
# load_dotenv("env/.env-dev")

# def _get_service_client():
#     connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
#     if connect_str is None:
#         raise Exception("Connection string not found in env AZURE_STORAGE_CONNECTION_STRING")
#     return BlobServiceClient.from_connection_string(connect_str)

def get_mlmd_store():
    from ml_metadata import metadata_store
    from ml_metadata.proto import metadata_store_pb2
    from  mlmd import gservice_dao
    mlmd_config = gservice_dao.get_secret("MLMD_CONFIG")
    connection_config = metadata_store_pb2.ConnectionConfig()
    connection_config.mysql.host = mlmd_config["MLMD_HOST"]
    connection_config.mysql.port = int(mlmd_config["MLMD_PORT"])
    connection_config.mysql.database = mlmd_config["MLMD_DB"]
    connection_config.mysql.user = mlmd_config["MLMD_USER"]
    connection_config.mysql.password = mlmd_config["MLMD_PASSWORD"]
    return metadata_store.MetadataStore(connection_config)
