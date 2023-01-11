import logging

import txp.common.utils.model_registry_utils
from txp.ml.training_service.dataset_fetchers.bigquery_dataset_fetcher import (
    BigqueryDatasetFetcher,
)
import ray
from txp.ml.training_service.model_trainers.basic_model_trainer import BasicModelTrainer
from txp.common.ml import models
from txp.ml.training_service import training_exceptions as te


class VibrationModelTrainer(BasicModelTrainer):
    def __init__(
            self,
            credentials_str,
            models_bucket_name,
            data_warehouse_bucket_name,
            prediction_service_topic,
            models_registry_collection_name,
            log_level: logging.INFO,
    ):
        super().__init__(
            credentials_str, models_bucket_name, prediction_service_topic, models_registry_collection_name, log_level
        )
        self.fetcher = BigqueryDatasetFetcher(
            credentials_str, data_warehouse_bucket_name, log_level
        )

    def _train_task(
            self,
            task,
            task_definition,
            dataset_name,
            dataset_versions,
            tenant_id,
            machine_id,
            task_id,
    ):
        logging.basicConfig(level=self.log_level)
        logging.info(
            f"Starting to Download data for {tenant_id}, {machine_id}, {task_id}, {dataset_name}"
        )
        gcs_task_path = txp.common.utils.model_registry_utils.get_gcs_task_bucket_path(tenant_id, machine_id, task_id)
        time_df = self.fetcher.get_time_dataframe_from_gcs(
            dataset_name, dataset_versions, gcs_task_path
        )

        time_df["label"].loc[:, "label"] = time_df["label"].apply(lambda x: self.get_label_value(task_definition, x))

        dataframes = {
            "time_df": time_df,
            "fft_df": self.fetcher.get_fft_dataframe_from_gcs(
                dataset_name, dataset_versions, gcs_task_path
            ),
            "psd_df": self.fetcher.get_psd_dataframe_from_gcs(
                dataset_name, dataset_versions, gcs_task_path
            ),
            "time_metrics_df": self.fetcher.get_time_metrics_dataframe_from_gcs(
                dataset_name, dataset_versions, gcs_task_path
            ),
            "fft_metrics_df": self.fetcher.get_fft_metrics_dataframe_from_gcs(
                dataset_name, dataset_versions, gcs_task_path
            ),
            "psd_metrics_df": self.fetcher.get_psd_metrics_dataframe_from_gcs(
                dataset_name, dataset_versions, gcs_task_path
            ),
        }
        logging.info(
            f"Data Downloaded for {tenant_id}, {machine_id}, {task_id}, {dataset_name}"
        )
        logging.info(
            f"Training model for {tenant_id}, {machine_id}, {task_id}, {dataset_name}"
        )
        try:
            dataset = task.encoder.build_training_dataset("label", {'tables': dataframes})
            task.policy.train(dataset, "label")
            storage_task = task.save()
        except:
            raise te.ErrorWhileTrainingModel()

        return storage_task

    def get_model_registry(self, task, tenant_id, machine_id, task_id, file_path, parameters=None) -> models.ModelRegistry:
        state = models.ModelState(
            value=models.ModelStateValue.TRAINING,
            creation_date=txp.common.utils.model_registry_utils.get_current_utc_datetime_str(),
            publishment_date="",
            deprecation_date=""
        )
        metadata = models.ModelMetadata(
            feedback=models.DefaultModelFeedback(),
            tenant_id=tenant_id,
            machine_id=machine_id,
            task_id=task_id
        )
        registry = models.ModelRegistry(
            metadata=metadata,
            file_path=file_path,
            state=state
        )
        return registry

    def get_model_feedback(self, task, task_definition) -> models.ModelFeedback:
        failed_predictions = [{
            "observation_timestamp": x["observation_timestamp"],
            "predicted_label": task_definition.label_def.int_to_label[x["predicted_label"]],
            "real_label":task_definition.label_def.int_to_label[x["real_label"]]
        } for x in task.policy.failed_predictions]
        return models.SuccessModelFeedback(metrics={"accuracy": task.policy.accuracy},
                                           failed_predictions=failed_predictions)


@ray.remote
class RayVibrationModelTrainer(VibrationModelTrainer):
    def __init__(
            self,
            credentials_str,
            models_bucket_name,
            data_warehouse_bucket_name,
            prediction_service_topic,
            models_registry_collection_name,
            log_level=logging.INFO,
    ):
        super().__init__(
            credentials_str,
            models_bucket_name,
            data_warehouse_bucket_name,
            prediction_service_topic,
            models_registry_collection_name,
            log_level,
        )
