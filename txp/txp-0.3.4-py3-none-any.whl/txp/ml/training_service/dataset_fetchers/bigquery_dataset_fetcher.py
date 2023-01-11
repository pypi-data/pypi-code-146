import json
import os.path
import pathlib
import shutil
import google.api_core.exceptions
import pandas as pd
import txp.common.utils.model_registry_utils
from google.oauth2 import service_account
from google.cloud import storage
import numpy as np
import logging
from txp.ml.training_service import training_exceptions as te


class BigqueryDatasetFetcher:
    def __init__(self, credentials_str, data_warehouse, log_level=logging.INFO):
        json_dict_service_account = json.loads(credentials_str, strict=False)
        self.credentials = service_account.Credentials.from_service_account_info(
            json_dict_service_account
        )
        self.data_warehouse = data_warehouse
        self.log_level = log_level

    def __get_dataframe_from_gcs(
            self, gcs_task_path, dataset_name, dataset_versions, table_name
    ):
        logging.basicConfig(level=self.log_level)
        storage_client = storage.Client(
            credentials=self.credentials, project=self.credentials.project_id
        )
        bucket = storage_client.bucket(
            self.data_warehouse, user_project=self.credentials.project_id
        )
        file_name = txp.common.utils.model_registry_utils.get_gcs_dataset_file_name(
            gcs_task_path, dataset_name, table_name, dataset_versions
        )
        blob = bucket.blob(file_name)
        tmp_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
        split_file_name = file_name.split("/")
        dataset_name = split_file_name[3]
        table_name = split_file_name[4]
        dataset_directory = os.path.join(tmp_directory, dataset_name)
        logging.info(f"Fetching remote dataset file for GCS path: {gcs_task_path}")
        if not os.path.isdir(dataset_directory):
            pathlib.Path(dataset_directory).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(dataset_directory, table_name)
        try:
            blob.download_to_filename(file_path)
        except google.api_core.exceptions.NotFound:
            logging.error(f"No such file found in GCS {file_name}")
            if os.path.exists(file_path):
                os.remove(file_path)
            return None
        df = pd.read_parquet(file_path)
        storage_client.close()
        shutil.rmtree(dataset_directory)
        return df

    def get_time_dataframe_from_gcs(
            self, dataset_name, dataset_versions, gcs_task_path
    ):
        df = self.__get_dataframe_from_gcs(
            gcs_task_path, dataset_name, dataset_versions, "time"
        )
        if df is None:
            raise te.NoParquetFileFound("time")
        return df

    def get_fft_dataframe_from_gcs(self, dataset_name, dataset_versions, gcs_task_path):
        df = self.__get_dataframe_from_gcs(
            gcs_task_path, dataset_name, dataset_versions, "fft"
        )
        if df is None:
            raise te.NoParquetFileFound("fft")
        df["fft"] = df["fft"].map(
            lambda fft: [
                [
                    np.complex128(complex(z["real"], z["imag"]))
                    for z in dimension["values"]
                ]
                for dimension in fft
            ]
        )
        return df

    def get_psd_dataframe_from_gcs(self, dataset_name, dataset_versions, gcs_task_path):
        df = self.__get_dataframe_from_gcs(
            gcs_task_path, dataset_name, dataset_versions, "psd"
        )
        if df is None:
            raise te.NoParquetFileFound("psd")
        df.rename(columns={"data": "psd"}, inplace=True)
        df["frequency"] = df["psd"].map(
            lambda data: [dimension["frequency"] for dimension in data]
        )
        df["psd"] = df["psd"].map(lambda data: [dimension["psd"] for dimension in data])
        return df

    def get_time_metrics_dataframe_from_gcs(
            self, dataset_name, dataset_versions, gcs_task_path
    ):
        df = self.__get_dataframe_from_gcs(
            gcs_task_path, dataset_name, dataset_versions, "time_metrics"
        )

        if df is None:
            raise te.NoParquetFileFound("time_metrics")
        return df

    def get_fft_metrics_dataframe_from_gcs(
            self, dataset_name, dataset_versions, gcs_task_path
    ):
        df = self.__get_dataframe_from_gcs(
            gcs_task_path, dataset_name, dataset_versions, "fft_metrics"
        )
        if df is None:
            raise te.NoParquetFileFound("fft_metrics")
        return df

    def get_psd_metrics_dataframe_from_gcs(
            self, dataset_name, dataset_versions, gcs_task_path
    ):
        df = self.__get_dataframe_from_gcs(
            gcs_task_path, dataset_name, dataset_versions, "psd_metrics"
        )
        if df is None:
            raise te.NoParquetFileFound("time_metrics")
        return df
