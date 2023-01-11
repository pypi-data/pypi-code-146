import json
from abc import ABC, abstractmethod
from typing import Dict, List

import txp.common.utils.model_registry_utils
from google.cloud import storage, pubsub_v1
from google.oauth2 import service_account
import google.cloud.firestore as firestore
import pathlib

from txp.ml.prediction_service.service_manager.prediction_manager import Command
import logging
from joblib import dump
import os
from ray.actor import ActorHandle
from txp.common.ml.tasks import AssetTask
from txp.common.ml.models import ModelRegistry, ModelFeedback, ErrorModelFeedback
from txp.ml.training_service import training_exceptions as te

from txp.ml.prediction_service.service_manager.factories import TaskFactory

class BasicModelTrainer(ABC):
    """A trainer is a concrete implementation that knows how to
    train (encode) specific Tasks implementations."""
    def __init__(
            self,
            credentials_str,
            models_bucket_name,
            prediction_service_topic,
            models_registry_collection_name,
            data_warehouse_bucket_name,
            log_level=logging.INFO,
    ):
        self.log_level = log_level
        logging.basicConfig(level=self.log_level)
        try:
            json_dict_service_account = json.loads(credentials_str, strict=False)
        except json.JSONDecodeError:
            logging.error("Error deconding JSON credentials value")
            raise ValueError("Error deconding JSON credentials value")

        try:
            self.credentials = service_account.Credentials.from_service_account_info(
                json_dict_service_account
            )
        except ValueError:
            logging.error("Error parsing Credentials, unexpected format.")

        self.models_registry_collection_name = models_registry_collection_name
        self.models_bucket_name = models_bucket_name
        self.prediction_service_topic = prediction_service_topic
        self.fetcher = None
        self.task_factory: TaskFactory = TaskFactory()

    def get_label_value(self, task_definition: AssetTask, json_string):
        label_dict = json.loads(json_string)
        if "label_value" not in label_dict:
            raise te.WrongLabelValue("Empty label dict")
        if not task_definition.label_def.is_valid_label_seq(label_dict["label_value"]):
            raise te.WrongLabelValue(label_dict["label_value"])
        return task_definition.label_def.label_to_int[frozenset(label_dict["label_value"])]

    @abstractmethod
    def _train_task(
            self,
            task: ActorHandle,
            task_definition: AssetTask,
            dataset_name: str,
            dataset_versions: List,
            tenant_id: str,
            machine_id: str,
            task_id: str,
    ):
        """Train the Ray Actor reference that points to some concrete
        implementation of a txp ML Task class.

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
        pass

    @abstractmethod
    def get_model_registry(self, task, tenant_id, machine_id, task_id, file_path, parameters=None) -> ModelRegistry:
        """This method returns model registry dataclass which contains all important information for a trained
        model
        """
        pass

    @abstractmethod
    def get_model_feedback(self, task, task_definition) -> ModelFeedback:
        pass

    def train(
            self,
            task_definition: AssetTask,
            dataset_name,
            dataset_versions,
            tenant_id,
            machine_id,
    ):
        """Trains the Ray Actor Task and then stores the result model in
        GCS models storage.
        """
        task_definition = task_definition
        task = self.task_factory.create_task(task_definition, "")
        task_id = task.task_id
        gcs_task_path = txp.common.utils.model_registry_utils.get_gcs_task_bucket_path(tenant_id, machine_id, task_id)
        gcs_file_path = f"{gcs_task_path}/{dataset_name}"
        file_name = txp.common.utils.model_registry_utils.get_gcs_model_file_name(dataset_name, dataset_versions)
        model_registry_name = txp.common.utils.model_registry_utils.get_gcs_dataset_prefix(dataset_name,
                                                                                           dataset_versions)
        model_registry = self.get_model_registry(task, tenant_id, machine_id, task_definition.task_id,
                                                 f"{gcs_file_path}/{file_name}", task_definition.parameters)
        firestore_db = firestore.Client(credentials=self.credentials, project=self.credentials.project_id)

        logging.info(f"Model created in firestore for tenant_id: {tenant_id}, machine_id: {machine_id}, "
                     f"task_id: {task_id}, dataset_name: {dataset_name}")
        txp.common.utils.model_registry_utils.insert_ml_model(firestore_db, model_registry, model_registry_name,
                                                              self.models_registry_collection_name)

        logging.info(f"Starting training process for task "
                     f"identified with: {gcs_task_path}")

        error_feedback = None
        storage_task = None
        exception = None
        try:
            storage_task = self._train_task(
                task,
                task_definition,
                dataset_name,
                dataset_versions,
                tenant_id,
                machine_id,
                task_id,
            )
        except te.WrongLabelValue as e:
            error_feedback = ErrorModelFeedback(error_message=e.get_message())
            exception = e
        except te.NoParquetFileFound as e:
            error_feedback = ErrorModelFeedback(error_message=e.get_message(gcs_file_path=gcs_file_path))
            exception = e
        except te.ErrorWhileTrainingModel as e:
            error_feedback = ErrorModelFeedback(error_message=e.get_message())
            exception = e

        if error_feedback is not None:
            txp.common.utils.model_registry_utils.set_error_ml_model(firestore_db, tenant_id, machine_id, task_id,
                                                                     model_registry_name,
                                                                     error_feedback,
                                                                     self.models_registry_collection_name)
            firestore_db.close()
            raise exception

        logging.info(f"Model identified with: {gcs_task_path} was successfully trained"
                     f" in memory")

        tmp_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

        file_path = os.path.join(tmp_directory, file_name)
        pathlib.Path(tmp_directory).mkdir(parents=True, exist_ok=True)

        logging.info(f"Trying to store {gcs_task_path} as a local file in: {file_path}")

        dump(storage_task, file_path)

        logging.info(f"Model successfully dumped in local storage: {file_path}")

        storage_client = storage.Client(credentials=self.credentials, project=self.credentials.project_id)
        bucket = storage_client.bucket(self.models_bucket_name, user_project=self.credentials.project_id)
        logging.info(f"Trying to upload model to remote model storage: {gcs_file_path}")
        blob = bucket.blob(f"{gcs_file_path}/{file_name}")
        blob.upload_from_filename(file_path)
        storage_client.close()
        os.remove(file_path)
        feedback = self.get_model_feedback(task, task_definition)
        txp.common.utils.model_registry_utils.acknowledge_ml_model(firestore_db, tenant_id, machine_id, task_id,
                                                                   model_registry_name,
                                                                   feedback, self.models_registry_collection_name)
        logging.info(f"Model registry acknowledged in firestore for tenant_id: {tenant_id}, machine_id: {machine_id}, "
                     f"task_id: {task_id}, dataset_name: {dataset_name}")

        firestore_db.close()
        logging.info(f"Model is already available in GCS at {self.models_bucket_name}/{gcs_file_path}")

    def send_command_to_prediction_service(self, tenant_id, asset_id, task_id):
        logging.basicConfig(level=self.log_level)
        logging.info(
            f"sending command to prediction service for tenant_id: {tenant_id}, asset_id: {asset_id}, "
            f"task_id: {task_id}"
        )
        publisher = pubsub_v1.PublisherClient(credentials=self.credentials)
        topic_path = publisher.topic_path(
            self.credentials.project_id, self.prediction_service_topic
        )
        future = publisher.publish(
            topic_path,
            data=json.dumps(
                {
                    "command": Command.UPDATE_TASK.value,
                    "parameters": {"tenant_id": tenant_id, "asset_id": asset_id, "task_id": task_id},
                }
            ).encode("utf-8"),
        )
        future.result()

    def publish_model(self, tenant_id, machine_id, task_id, dataset_name, dataset_versions,
                     task_params: Dict):
        """Publish a model in response to an explicit /publish request by a client."""

        log_identifier_str = f"tenant_id: {tenant_id}, machine_id: {machine_id}, " \
                             f"task_id: {task_id}, dataset_name: {dataset_name}"
        firestore_db = firestore.Client(credentials=self.credentials, project=self.credentials.project_id)

        logging.info(f"Downgrading model in firestore for {log_identifier_str}")

        deprecation_res = txp.common.utils.model_registry_utils.deprecate_active_ml_model(
            firestore_db, tenant_id, machine_id, task_id, self.models_registry_collection_name)
        if deprecation_res:
            logging.info(f"Last active model was deprecated: {deprecation_res}")
        else:
            logging.info(f"There was not an active model for {log_identifier_str}")

        logging.info(f"Upgrading model in firestore for {log_identifier_str}")

        model_registry_name = txp.common.utils.model_registry_utils.get_gcs_dataset_prefix(dataset_name,
                                                                                           dataset_versions)
        publish_res = txp.common.utils.model_registry_utils.publish_ml_model(firestore_db, tenant_id, machine_id,
                                                                             task_id, model_registry_name,
                                                                             self.models_registry_collection_name)
        if not publish_res:
            logging.info(f"Cannot Upgrade model in firestore for {log_identifier_str}, "
                         f"model does not exists or it is already active")
            firestore_db.close()
            return

        logging.info(f"Model upgraded in firestore for {log_identifier_str}")

        logging.info(f"Stating to publish model for {log_identifier_str}")

        file_name = txp.common.utils.model_registry_utils.get_gcs_model_file_name(dataset_name, dataset_versions)
        gcs_task_path = txp.common.utils.model_registry_utils.get_gcs_task_bucket_path(tenant_id, machine_id, task_id)
        gcs_file_path = f"{gcs_task_path}/{dataset_name}/{file_name}"
        firestore_db = firestore.Client(credentials=self.credentials, project=self.credentials.project_id)
        txp.common.utils.model_registry_utils.update_model_in_task(firestore_db, tenant_id, machine_id, task_id,
                                                                   gcs_file_path, task_params)
        self.send_command_to_prediction_service(tenant_id, machine_id, task_id)
        firestore_db.close()

        logging.info(f"Model was published for {log_identifier_str}. ")
        logging.info(f"Model is already available at {self.models_bucket_name}/{gcs_file_path}")
