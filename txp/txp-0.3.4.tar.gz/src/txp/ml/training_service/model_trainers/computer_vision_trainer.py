import logging

import txp.common.utils.bigquery_utils
import txp.common.utils.model_registry_utils
import txp.common.utils.signals_utils
from txp.ml.training_service.dataset_fetchers.bigquery_dataset_fetcher import (
    BigqueryDatasetFetcher,
)
import ray
from txp.ml.training_service.model_trainers.basic_model_trainer import BasicModelTrainer
from txp.common.ml import models
from txp.ml.training_service import training_exceptions as te
from txp.common.ml.tasks import AssetTask


class ComputerVisionSlicClassificationTrainer(BasicModelTrainer):
    """This trainer will take care of training any of the
    basic SLIC models.
    """

    def __init__(
        self,
        credentials_str,
        models_bucket_name,
        data_warehouse_bucket_name,
        prediction_service_topic,
        models_registry_collection_name,
        log_level=logging.INFO,
    ):
        logging.basicConfig(level=log_level)
        super(ComputerVisionSlicClassificationTrainer, self).__init__(
            credentials_str,
            models_bucket_name,
            prediction_service_topic,
            models_registry_collection_name,
            log_level,
        )
        self._data_fetcher: BigqueryDatasetFetcher = BigqueryDatasetFetcher(
            credentials_str, data_warehouse_bucket_name, log_level
        )

        self.fetcher = BigqueryDatasetFetcher(
            credentials_str, data_warehouse_bucket_name, log_level
        )

    def _train_task(
        self,
        task,
        task_definition: AssetTask,
        dataset_name,
        dataset_versions,
        tenant_id,
        machine_id,
        task_id,
    ):
        """Trains the received Task Actor Handle which refers to a concrete
        Slic Computer vision recognition implementation.

        If hyper parameters are present in task_definition, they will be passed
        across the common interface for SLIC classes. If not, then defaults
        are used by each implementation.

        Note:  This implementation currently supports only datasets produced directly
            from BigQuery time records. Eventually we can supports CV datasets from
            another sources like HuggingFace or Segments.ai.

        Args:
            task (ActorHandle): object reference to the ray actor process.

            task_definition (Dict): A key value map with possible hyper parameters
                declared for the task.

            dataset_name: The dataset name in the models repository.

            dataset_versions: The list of labeling version that composes
                the dataset.

            tenant_id: The tenant ID to which this training belongs.

            machine_id: The asset to which this trained task belongs.

            task_id: The task identifier (task class name).
        """
        logging.info(
            f"{self.__class__.__name__} starts training for task/tenant: {task_id}/{tenant_id}"
        )
        logging.info(
            f"SLIC task parameters description: {task.task_definition.parameters}"
        )
        logging.info(f"Task labels table: {task_definition.label_def.label_to_int}")
        gcs_task_path = txp.common.utils.model_registry_utils.get_gcs_task_bucket_path(
            tenant_id, machine_id, task_id
        )
        time_df = self.fetcher.get_time_dataframe_from_gcs(
            dataset_name, dataset_versions, gcs_task_path
        )
        encoder_args = {"df": time_df}
        logging.info("Successfully images loaded dataframe")
        logging.info("Successfully applied label value to images dataframe")

        try:
            train_dataset = task.encoder.build_training_dataset("label", **encoder_args)
            task.policy.train(train_dataset, test_size=0.05)
            storage_task = task.save()
            logging.info(
                f"Task successfully trained with result: {task.policy.accuracy}"
            )
        except:
            raise te.ErrorWhileTrainingModel
        return storage_task

    def get_model_registry(
        self, task, tenant_id, machine_id, task_id, file_path, parameters=None
    ) -> models.ModelRegistry:
        state = models.ModelState(
            value=models.ModelStateValue.TRAINING,
            creation_date=txp.common.utils.model_registry_utils.get_current_utc_datetime_str(),
            publishment_date="",
            deprecation_date="",
        )
        metadata = models.ModelMetadata(
            feedback=models.DefaultModelFeedback(),
            tenant_id=tenant_id,
            machine_id=machine_id,
            task_id=task_id,
        )
        registry = models.ModelRegistry(
            metadata=metadata, file_path=file_path, state=state, parameters=parameters
        )
        return registry

    def get_model_feedback(self, task, task_definition) -> models.ModelFeedback:
        failed_predictions = [
            {
                "observation_timestamp": x["observation_timestamp"],
                "predicted_label": task_definition.label_def.int_to_label[
                    x["predicted_label"]
                ],
                "real_label": task_definition.label_def.int_to_label[x["real_label"]],
            }
            for x in task.policy.failed_predictions
        ]
        return models.SuccessModelFeedback(
            metrics={"accuracy": task.policy.accuracy},
            failed_predictions=failed_predictions,
        )


@ray.remote
class RayComputerVisionSlicClassificationTrainer(
    ComputerVisionSlicClassificationTrainer
):
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
