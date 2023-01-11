from txp.ml.training_service.dataset_committer import (
    DatasetCommitter,
    DatasetCommitPayload,
)
import ray
import logging
import json
from google.oauth2 import service_account
from google.cloud import firestore, bigquery
from txp.common.utils import firestore_utils, signals_utils, bigquery_utils
from txp.common.ml.annotation import AnnotationLabel
from txp.ml.prediction_service.service_manager.prediction_manager import TaskFactory
from txp.common.utils import model_registry_utils


@ray.remote
class PreAnnotationManager:
    def __init__(self, credentials_str: str, models_registry_collection_name, log_level=logging.INFO):
        self.dataset_committer = DatasetCommitter(credentials_str, None, log_level)
        json_dict_service_account = json.loads(credentials_str, strict=False)
        self.credentials = service_account.Credentials.from_service_account_info(
            json_dict_service_account
        )
        self.credentials_str = credentials_str
        self.models_registry_collection_name = models_registry_collection_name
        logging.info(f"{self.__class__.__name__} Successfully created")

    def build_in_memory_dataset(self, datasets, task_definition):
        logging.info(f"building in memory dataset for {task_definition.task_id}, at pre annotation manager")
        groups = {
            "time": datasets["time"].groupby(
                ["observation_timestamp", "edge_logical_id", "perception_name"]
            ),
            "fft": datasets["fft"].groupby(
                ["observation_timestamp", "edge_logical_id", "perception_name"]
            ),
            "psd": datasets["psd"].groupby(
                ["observation_timestamp", "edge_logical_id", "perception_name"]
            ),
            "time_metrics": datasets["time_metrics"].groupby(
                ["observation_timestamp", "edge_logical_id", "perception_name"]
            ),
            "fft_metrics": datasets["fft_metrics"].groupby(
                ["observation_timestamp", "edge_logical_id", "perception_name"]
            ),
            "psd_metrics": datasets["psd_metrics"].groupby(
                ["observation_timestamp", "edge_logical_id", "perception_name"]
            ),
        }
        sampling_windows_row = {}
        for grouped_tuple, group in groups["time"]:
            observation_timestamp = grouped_tuple[0]
            sampling_windows_row[observation_timestamp] = {}
            for edge_logical_id in task_definition.schema_:
                sampling_windows_row[observation_timestamp][edge_logical_id] = {}
                for perception_name in task_definition.schema_[edge_logical_id]:
                    sampling_windows_row[observation_timestamp][edge_logical_id][
                        perception_name
                    ] = {}
                    for table_id in task_definition.schema_[edge_logical_id][
                        perception_name
                    ]:
                        try:
                            df = groups[table_id].get_group(
                                (observation_timestamp, edge_logical_id, perception_name)
                            )
                        except:
                            logging.warning(f"The observation timestamp {observation_timestamp} does not"
                                            f" have data for table {table_id}")
                            continue

                        rows = df.to_dict("records")
                        if table_id == "time":
                            signal = signals_utils.merge_signal_chunks(rows)
                            signal["data"] = [
                                dimension["values"] for dimension in signal["data"]
                            ]
                            sampling_windows_row[observation_timestamp][
                                edge_logical_id
                            ][perception_name][table_id] = [signal]
                        else:
                            sampling_windows_row[observation_timestamp][
                                edge_logical_id
                            ][perception_name][table_id] = rows
        logging.info(f"dataset built for {task_definition.task_id}, at pre annotation manager, "
                     f"with {len(sampling_windows_row)} observation timestamps")
        return sampling_windows_row

    def pre_annotate_dataset(self, commit: DatasetCommitPayload):

        logging.info(f"New commit arrived, {commit} is going to be pre annotated")
        firestore_db = firestore.Client(
            credentials=self.credentials, project=self.credentials.project_id
        )
        bigquery_db = bigquery.Client(
            credentials=self.credentials, project=self.credentials.project_id
        )

        model_registry_utils.set_is_pre_annotating_ml_model(firestore_db, commit.tenant_id, commit.machine_id,
                                                            commit.task_id, True, self.models_registry_collection_name)

        (
            time_dataset,
            fft_dataset,
            psd_dataset,
            time_metrics_dataset,
            fft_metrics_dataset,
            psd_metrics_dataset,
        ) = self.dataset_committer.get_datasets(commit)

        task_definition = firestore_utils.get_task_from_firestore(
            firestore_db,
            commit.tenant_id,
            commit.machine_id,
            commit.task_id,
        )
        if task_definition is None:
            logging.error(f"No Task JSON found for {commit.task_id}")
            model_registry_utils.set_is_pre_annotating_ml_model(firestore_db, commit.tenant_id, commit.machine_id,
                                                                commit.task_id, False,
                                                                self.models_registry_collection_name)
            return False

        dataset = self.build_in_memory_dataset(
            {
                "time": time_dataset,
                "fft": fft_dataset,
                "psd": psd_dataset,
                "time_metrics": time_metrics_dataset,
                "fft_metrics": fft_metrics_dataset,
                "psd_metrics": psd_metrics_dataset,
            },
            task_definition,
        )

        task = TaskFactory.create_task(task_definition, self.credentials_str)

        logging.info(f"Updating dataset at bigquery in pre annotation manager for {commit}")

        for observation_timestamp in dataset:
            pred = task.predict(dataset[observation_timestamp])

            if pred is None:
                logging.warning(f"Empty prediction for {observation_timestamp} timestamp")
                continue

            label_value = list(pred)
            label = AnnotationLabel(
                label_value=label_value,
                parameters={},
                label_type="ClassificationLabelDefinition"
            )

            for edge_logical_id in dataset[observation_timestamp]:
                logging.info(f"PreAnnotating timestamp {observation_timestamp} for {edge_logical_id}")
                bigquery_utils.annotate_signal(
                    commit.tenant_id,
                    f"{commit.bigquery_dataset}.time",
                    edge_logical_id,
                    observation_timestamp,
                    label.json(),
                    commit.dataset_versions,
                    bigquery_db,
                )
        model_registry_utils.set_is_pre_annotating_ml_model(firestore_db, commit.tenant_id, commit.machine_id,
                                                            commit.task_id, False,
                                                            self.models_registry_collection_name)
        logging.info(f"End of pre annotation process for {commit}")
