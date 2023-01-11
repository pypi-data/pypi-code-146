from typing import List

import ray
import logging
import json

import txp.common.utils.bigquery_utils
import txp.common.utils.firestore_utils
import txp.common.utils.model_registry_utils
from pydantic import BaseModel, Field
from google.cloud import firestore
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import storage
import datetime
from txp.common.config import settings


class DatasetCommitPayload(BaseModel):
    """Expected Payload to receive when the client request the
    creation of """
    tenant_id: str
    task_id: str
    start: str
    end: str
    dataset_name: str
    dataset_versions: List[str]
    machine_id: str = Field(alias='asset_id')
    bigquery_dataset: str

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/602#issuecomment-503189368
        allow_population_by_field_name = True


class DatasetCommitter:
    """This actor supports the datasets generation based on labeled data
    in TXP data sources.

    """

    def __init__(self, credentials_str: str, data_warehouse_bucket_name, log_level=logging.INFO):
        logging.basicConfig(level=log_level)

        self.data_warehouse_bucket_name = data_warehouse_bucket_name
        json_dict_service_account = json.loads(credentials_str, strict=False)
        self._credentials = service_account.Credentials.from_service_account_info(
            json_dict_service_account
        )

        logging.info(f"{self.__class__.__name__} Successfully created")

    def _get_dataset(
            self,
            tenant_id,
            table_name,
            edges,
            dataset_versions,
            start_datetime,
            end_datetime,
            bigquery_dataset,
            bigquery_client,
    ):
        return txp.common.utils.bigquery_utils.get_all_signals_for_asset(
            tenant_id,
            f"{bigquery_dataset}.{table_name}",
            edges,
            dataset_versions,
            start_datetime,
            end_datetime,
            bigquery_client,
        )

    def get_datasets(self, commit):
        logging.info(
            f"Requested to get Datasets with the following parameters: "
            f"tenant-id[{commit.tenant_id}]|"
            f"machine-id[{commit.machine_id}]|"
            f"task-id[{commit.task_id}]"
        )
        firestore_db: firestore.Client = firestore.Client(
            credentials=self._credentials, project=self._credentials.project_id
        )
        bigquery_client: bigquery.Client = bigquery.Client(
            credentials=self._credentials, project=self._credentials.project_id
        )
        machine = txp.common.utils.firestore_utils.get_machine_from_firestore(
            firestore_db, commit.tenant_id, commit.machine_id
        )
        if machine is None:
            logging.error(
                f'Tenant:{commit.tenant_id} or Machine:{commit.machine_id} not found'
            )
            return

        if commit.task_id not in machine["tasks"]:
            logging.error(
                f"No task found or task is not unique for {commit.task_id}"
            )
            return

        task = machine["tasks"][commit.task_id]

        logging.info(f'Machine {commit.machine_id} and task {commit.task_id} found '
                     f'successfully')

        edges = task["edges"]
        start_datetime = datetime.datetime.strptime(commit.start, settings.time.datetime_zoned_format)
        end_datetime = datetime.datetime.strptime(commit.end, settings.time.datetime_zoned_format)

        time_dataset = self._get_dataset(
            commit.tenant_id,
            "time",
            edges,
            commit.dataset_versions,
            start_datetime,
            end_datetime,
            commit.bigquery_dataset,
            bigquery_client,
        )
        fft_dataset = self._get_dataset(
            commit.tenant_id,
            "fft",
            edges,
            commit.dataset_versions,
            start_datetime,
            end_datetime,
            commit.bigquery_dataset,
            bigquery_client,
        )
        psd_dataset = self._get_dataset(
            commit.tenant_id,
            "psd",
            edges,
            commit.dataset_versions,
            start_datetime,
            end_datetime,
            commit.bigquery_dataset,
            bigquery_client,
        )
        time_metrics_dataset = self._get_dataset(
            commit.tenant_id,
            "time_metrics",
            edges,
            commit.dataset_versions,
            start_datetime,
            end_datetime,
            commit.bigquery_dataset,
            bigquery_client,
        )
        psd_metrics_dataset = self._get_dataset(
            commit.tenant_id,
            "psd_metrics",
            edges,
            commit.dataset_versions,
            start_datetime,
            end_datetime,
            commit.bigquery_dataset,
            bigquery_client,
        )
        fft_metrics_dataset = self._get_dataset(
            commit.tenant_id,
            "fft_metrics",
            edges,
            commit.dataset_versions,
            start_datetime,
            end_datetime,
            commit.bigquery_dataset,
            bigquery_client,
        )
        firestore_db.close()
        bigquery_client.close()
        return time_dataset, fft_dataset, psd_dataset, time_metrics_dataset, fft_metrics_dataset, psd_metrics_dataset

    def commit_dataset(self, commit: DatasetCommitPayload):
        time_dataset, fft_dataset, psd_dataset, time_metrics_dataset, fft_metrics_dataset, psd_metrics_dataset = \
            self.get_datasets(commit)

        storage_client = storage.Client(credentials=self._credentials,
                                        project=self._credentials.project_id)

        bucket = storage_client.bucket(self.data_warehouse_bucket_name, user_project=self._credentials.project_id)

        task_path = txp.common.utils.model_registry_utils.get_gcs_task_bucket_path(
            commit.tenant_id, commit.machine_id, commit.task_id
        )
        if len(time_dataset):
            blob = bucket.blob(
                txp.common.utils.model_registry_utils.get_gcs_dataset_file_name(
                    task_path,
                    commit.dataset_name,
                    "time",
                    commit.dataset_versions,
                )
            )
            time_dataset.to_parquet("/tmp/time.gzip", compression="gzip")
            blob.upload_from_filename("/tmp/time.gzip")
            logging.info(f"Successfully created time dataset for {commit}")
        else:
            logging.warning(f"Nothing found at time table in commit {commit}")

        if len(fft_dataset):
            blob = bucket.blob(
                txp.common.utils.model_registry_utils.get_gcs_dataset_file_name(
                    task_path, commit.dataset_name, "fft", commit.dataset_versions
                )
            )
            fft_dataset.to_parquet("/tmp/fft.gzip", compression="gzip")
            blob.upload_from_filename("/tmp/fft.gzip")
            logging.info(f"Successfully created fft dataset for {commit}")
        else:
            logging.info(f"Nothing found at fft table in commit {commit}")

        if len(psd_dataset):
            blob = bucket.blob(
                txp.common.utils.model_registry_utils.get_gcs_dataset_file_name(
                    task_path, commit.dataset_name, "psd", commit.dataset_versions
                )
            )
            psd_dataset.to_parquet("/tmp/psd.gzip", compression="gzip")
            blob.upload_from_filename("/tmp/psd.gzip")
            logging.info(f"Successfully created psd dataset for {commit}")
        else:
            logging.info(f"Nothing found at psd table {commit}")

        if len(time_metrics_dataset):
            blob = bucket.blob(
                txp.common.utils.model_registry_utils.get_gcs_dataset_file_name(
                    task_path,
                    commit.dataset_name,
                    "time_metrics",
                    commit.dataset_versions,
                )
            )
            time_metrics_dataset.to_parquet(
                "/tmp/time_metrics.gzip", compression="gzip"
            )
            blob.upload_from_filename("/tmp/time_metrics.gzip")
        else:
            logging.info(f"Nothing found at time_metrics table {commit}")

        if len(fft_metrics_dataset):
            blob = bucket.blob(
                txp.common.utils.model_registry_utils.get_gcs_dataset_file_name(
                    task_path,
                    commit.dataset_name,
                    "fft_metrics",
                    commit.dataset_versions,
                )
            )
            fft_metrics_dataset.to_parquet("/tmp/fft_metrics.gzip", compression="gzip")
            blob.upload_from_filename("/tmp/fft_metrics.gzip")
            logging.info(f"Successfully created fft_metrics dataset for {commit}")
        else:
            logging.info(f"Nothing found at fft_metrics table {commit}")

        if len(psd_metrics_dataset):
            blob = bucket.blob(
                txp.common.utils.model_registry_utils.get_gcs_dataset_file_name(
                    task_path,
                    commit.dataset_name,
                    "psd_metrics",
                    commit.dataset_versions,
                )
            )
            psd_metrics_dataset.to_parquet("/tmp/psd_metrics.gzip", compression="gzip")
            blob.upload_from_filename("/tmp/psd_metrics.gzip")
            logging.info(f"Successfully created psd_metrics dataset for {commit}")
        else:
            logging.info(f"Nothing found at psd_metrics table {commit}")

        storage_client.close()


@ray.remote
class RayDatasetCommitter(DatasetCommitter):
    def __init__(self, credentials_str: str, data_warehouse_bucket_name, log_level=logging.INFO):
        super().__init__(credentials_str, data_warehouse_bucket_name, log_level)
