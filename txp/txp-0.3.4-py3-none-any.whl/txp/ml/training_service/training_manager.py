import ray
import logging
import json

import txp.common.utils.firestore_utils
from google.oauth2 import service_account
import google.cloud.firestore as firestore
from txp.ml.training_service.model_trainers import TrainerFactory


@ray.remote
class TrainingManager:
    """This class is in charge of processing anything that arrives at the
    /training endpoint.

    This class will be called from the main Ray Serve deployment serving
    the HTTP endpoints for training, and it will:
        - create new Actors to perform training related activities
        - interact with in memory actors refs
    """

    def __init__(self, credentials_str, models_bucket_name, data_warehouse_bucket_name,
                 prediction_service_topic, models_registry_collection_name, log_level=logging.INFO):
        self._log_level = log_level
        logging.basicConfig(level=log_level)
        json_dict_service_account = json.loads(credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(
            json_dict_service_account
        )
        self._credentials_str = credentials_str
        self._firestore_db = firestore.Client(
            credentials=credentials, project=credentials.project_id
        )
        self.factory = TrainerFactory(credentials_str,  models_bucket_name, data_warehouse_bucket_name,
                                      prediction_service_topic, models_registry_collection_name, log_level)
        logging.info(f"{self.__class__.__name__} Created successfully.")

    def process_acknowledge(self, acknowledge) -> bool:
        task_definition = txp.common.utils.firestore_utils.get_task_from_firestore(
            self._firestore_db,
            acknowledge["tenant_id"],
            acknowledge["machine_id"],
            acknowledge["task_id"],
        )
        if task_definition is None:
            logging.error(f"No Task JSON found for {acknowledge['task_id']}")
            return False

        if 'task_params' in acknowledge:
            logging.info(f"Received parameters in train request. {acknowledge['task_params']}")
            params_d = json.loads(acknowledge['task_params'])
            if params_d:
                task_definition.parameters = {
                    **task_definition.parameters, **params_d,
                }

        trainer = self.factory.get_trainer(task_definition)

        try:
            trainer.train.remote(
                task_definition,
                acknowledge["dataset_name"],
                acknowledge["dataset_versions"],
                acknowledge["tenant_id"],
                acknowledge["machine_id"],
            )
            logging.info(
                f"Successfully started training in cluster for"
                f"{acknowledge['task_id']}"
            )
        except Exception as e:
            logging.error(f"Unexpected {e}")
            return False
        else:
            return True

    def process_publish(self, publish_command):
        task_definition = txp.common.utils.firestore_utils.get_task_from_firestore(
            self._firestore_db,
            publish_command["tenant_id"],
            publish_command["machine_id"],
            publish_command["task_id"],
        )
        if task_definition is None:
            logging.error(f"No Task JSON found for {publish_command['task_id']}")
            return False

        if 'task_params' in publish_command:
            logging.info(f"Received parameters in train request. {publish_command['task_params']} ")
            params_d = json.loads(publish_command['task_params'])
            task_definition.parameters = {
                **task_definition.parameters, **params_d,
            }

        trainer = self.factory.get_trainer(task_definition)
        trainer.publish_model.remote(
            publish_command["tenant_id"],
            publish_command["machine_id"],
            publish_command["task_id"],
            publish_command["dataset_name"],
            publish_command["dataset_versions"],
            task_definition.parameters
        )
        logging.info(
            f"Successfully started training in cluster for {publish_command['task_id']}"
        )
        return True
