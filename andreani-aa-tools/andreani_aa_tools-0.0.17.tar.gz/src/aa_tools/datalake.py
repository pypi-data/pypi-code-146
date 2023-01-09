
from azure.storage.filedatalake import DataLakeServiceClient
import pandas as pd
from io import BytesIO
import pickle
import json

class datalake():

    def __init__(self, credentials, file_system = "datalake"):
        with open(credentials, "rb") as file:
            storage_account_name, storage_account_key = pickle.load(file)

        # Defino la conexión al datalake
        service_client = DataLakeServiceClient(
                account_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name),
                credential=storage_account_key)
        self._client = service_client.get_file_system_client(file_system=file_system)

        self._import_settings = {
            "parquet" : pd.read_parquet,
            "csv" : pd.read_csv,
            "json" : json.loads
        }


    def import_file(self, path, filename, read_format, separator = ',', decimal = '.'):
        directory_client = self._client.get_directory_client(path)
        file_client = directory_client.get_file_client(filename)
        # descargo los datos
        download = file_client.download_file()
        downloaded_bytes = download.readall()

        if read_format == 'csv':
            return pd.read_csv(BytesIO(downloaded_bytes), sep=separator, decimal=decimal, low_memory=False)
        elif read_format == 'json':
            return self._import_settings[read_format](downloaded_bytes)
        else:
            return self._import_settings[read_format](BytesIO(downloaded_bytes))


    def upload_file(self, data, path, filename, write_format):
        directory_client = self._client.get_directory_client(path)

        file_client = directory_client.create_file(filename)
        if write_format == "parquet":
            file_contents = data.to_parquet(index=False).encode()
        elif write_format == "csv":
            file_contents = data.to_csv(index=False).encode()
        elif write_format == "json":
            file_contents = json.dumps(data).encode('utf-8')
        file_client.upload_data(file_contents, overwrite=True)
