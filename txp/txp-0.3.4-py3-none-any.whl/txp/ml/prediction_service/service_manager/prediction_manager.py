from enum import Enum

import txp.common.utils.firestore_utils
from google.oauth2 import service_account
import google.cloud.firestore as firestore
import logging
import threading
import json
import ray
from txp.ml.prediction_service.service_manager.signals_segregator import SignalsSegregator
from txp.ml.prediction_service.service_manager.task_manager import TaskManager
from txp.ml.prediction_service.service_manager.factories import TaskFactory, StateManagerFactory


@ray.remote
class PredictionManager:

    def __init__(self, dataset, subscription_id, backup_collection_name, events_and_states_dataset,
                 notifications_topic, reports_topic, credentials_str, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        self.credentials_str = credentials_str
        self.signals_segregator = SignalsSegregator(credentials_str, dataset, subscription_id, backup_collection_name)
        self.task_manager = TaskManager(self.pull_configuration(), credentials_str,
                                        backup_collection_name,
                                        events_and_states_dataset, notifications_topic, reports_topic)

        self.__pubsub_messages_thread: threading.Thread = threading.Thread(
            daemon=True,
            name="pubsub_messages_thread",
            target=self.__process_pubsub_messages_background,
        )
        self.__pubsub_messages_thread.start()

    def __process_pubsub_messages_background(self):
        logging.info("Starting Pubsub listener.")
        while True:
            pubsub_messages = self.signals_segregator.get_messages()

            if pubsub_messages is None:
                continue

            signals = []
            commands = []
            for pub_sub_message in pubsub_messages:
                message = json.loads(pub_sub_message.message.data.decode('utf-8'))
                if "command" in message:
                    commands.append(message)
                else:
                    signals.append(message)

            logging.info(f"Processing {len(signals)} messages ")
            self.task_manager.process_messages(signals, self.signals_segregator)
            if commands:
                logging.info(f"Processing {len(commands)} commands")
                res = self.process_commands(commands)
                if Command.STOP in res:
                    break

        logging.info("Prediction Service Thread ended it is safe to end the entire service")

    def stop_ray_service(self):
        self.task_manager.backup()
        self.signals_segregator.backup()

    def pull_configuration(self):
        json_dict_service_account = json.loads(self.credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
        tenants = txp.common.utils.firestore_utils.get_all_tenants_from_firestore(firestore_db)
        config = {}
        for tenant in tenants:
            tenant_id = tenant["tenant_id"]
            machines = txp.common.utils.firestore_utils.get_machines_from_firestore(firestore_db, tenant_id)
            config[tenant_id] = {}
            for machine in machines:
                if "tasks" in machine and "state_manager" in machine:
                    config[tenant_id][machine["machine_id"].replace(" ", "_")] = {
                        "tasks": machine["tasks"],
                        "state_manager": machine["state_manager"]
                    }
            if not config[tenant_id]:
                config.pop(tenant_id)
        return config

    def update_task_configuration(self, tenant_id, asset_id, task_id):
        json_dict_service_account = json.loads(self.credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
        task = txp.common.utils.firestore_utils.get_task_from_firestore(firestore_db, tenant_id, asset_id, task_id)
        logging.info(f"Updating service for tenant id: {tenant_id}, asset_id: {asset_id}, task_id: {task_id}")

        if task is None:
            logging.info(
                f"Service cloud not be updated for tenant id: {tenant_id}, asset_id: {asset_id}, task_id: {task_id}, "
                f"task not found.")
            return

        self.task_manager.tasks.pop(task_id, None)
        self.task_manager.state_managers.pop(self.task_manager.tenants_config[tenant_id][asset_id]["state_manager"],
                                             None)
        self.task_manager.tenants_config[tenant_id][asset_id][task_id] = task.dict()

        state_manager_id = self.task_manager.tenants_config[tenant_id][asset_id]["state_manager"]
        state_manager = StateManagerFactory.create_state_manager_for_asset(
            asset_id,
            self.task_manager.tenants_config[tenant_id][asset_id],
            self.credentials_str,
            self.task_manager.backup_collection_name,
            self.task_manager.events_and_states_dataset,
            self.task_manager.notifications_topic,
            self.task_manager.reports_topic
        )
        if state_manager is None:
            logging.info(
                f"Service cloud not be updated for tenant id: {tenant_id}, asset_id: {asset_id}, task_id: {task_id},"
                f"state manager id {state_manager_id} is wrong or has not been configured")
            return
        self.task_manager.state_managers[state_manager_id] = state_manager
        self.task_manager.tasks[task_id] = TaskFactory.create_task(task, self.credentials_str)
        logging.info(f"Service Updated for tenant id: {tenant_id}, asset_id: {asset_id}, task_id: {task_id}")

    def update_asset(self, tenant_id, asset_dict):
        asset_id = asset_dict["machine_id"]
        logging.info(f"Updating service for tenant id: {tenant_id}, asset_id: {asset_id}.")

        if asset_dict is None:
            logging.info(f"Service cloud not be updated for tenant id: {tenant_id}, asset_id: {asset_id}, "
                         f"task not found.")
            return

        self.task_manager.tenants_config[tenant_id][asset_id] = asset_dict

        for task in self.task_manager.tenants_config[tenant_id][asset_id]["tasks"].values():
            self.task_manager.tasks.pop(task["task_id"], None)
        self.task_manager.state_managers.pop(self.task_manager.tenants_config[tenant_id][asset_id]["state_manager"],
                                             None)

        state_manager_id = self.task_manager.tenants_config[tenant_id][asset_id]["state_manager"]
        state_manager = StateManagerFactory.create_state_manager_for_asset(
            asset_id,
            self.task_manager.tenants_config[tenant_id][asset_id],
            self.credentials_str,
            self.task_manager.backup_collection_name,
            self.task_manager.events_and_states_dataset,
            self.task_manager.notifications_topic,
            self.task_manager.reports_topic,
        )
        if state_manager is None:
            logging.info(f"Service cloud not be updated for tenant id: {tenant_id}, asset_id: {asset_id}, "
                         f"state manager id {state_manager_id} is wrong or has not been configured")
            return
        self.task_manager.state_managers[state_manager_id] = state_manager
        self.task_manager.tasks = {**self.task_manager.tasks,
                                   **TaskFactory.create_tasks_for_asset(
                                       asset_id, self.task_manager.tenants_config[tenant_id],
                                       self.credentials_str
                                   )}
        logging.info(f"Service Updated for tenant id: {tenant_id}, asset_id: {asset_id}")

    def update_asset_configuration(self, tenant_id, asset_id):
        json_dict_service_account = json.loads(self.credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
        asset_dict = txp.common.utils.firestore_utils.get_machine_from_firestore(firestore_db, tenant_id, asset_id)
        self.update_asset(tenant_id, asset_dict)

    def update_tenant_configuration(self, tenant_id):
        json_dict_service_account = json.loads(self.credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
        assets = txp.common.utils.firestore_utils.get_machines_from_firestore(firestore_db, tenant_id)
        for asset_dict in assets:
            self.update_asset(tenant_id, asset_dict)

    def process_commands(self, messages):
        res = []
        for message in messages:
            if message["command"] == Command.STOP.value:
                logging.info("Stopping Service waiting until all ray actors stop...")
                running_actors = ray.get(self.task_manager.actors_stack.get_running_actors_count.remote())
                while running_actors > 0:
                    logging.info(f"There is still {running_actors} actors running.")
                    running_actors = ray.get(self.task_manager.actors_stack.get_running_actors_count.remote())
                    continue
                logging.info("There are no more ray actors running, backing up task manager and signals segregator")
                self.stop_ray_service()
                res.append(Command.STOP)
            elif message["command"] == Command.UPDATE_TASK.value:
                logging.info(f"New update command received for tenant_id: {message['parameters']['tenant_id']}, "
                             f"asset_id: {message['parameters']['tenant_id']}, "
                             f"task_id: {message['parameters']['tenant_id']} ")
                self.update_task_configuration(message["parameters"]["tenant_id"],
                                               message["parameters"]["asset_id"],
                                               message["parameters"]["task_id"])
            elif message["command"] == Command.UPDATE_ASSET.value:
                logging.info(f"New update command received for tenant_id: {message['parameters']['tenant_id']}, "
                             f"asset_id: {message['parameters']['tenant_id']}.")
                self.update_asset_configuration(message["parameters"]["tenant_id"],
                                                message["parameters"]["asset_id"])

            elif message["command"] == Command.UPDATE_TENANT.value:
                logging.info(f"New update command received for tenant_id: {message['parameters']['tenant_id']}.")
                self.update_tenant_configuration(message["parameters"]["tenant_id"])

        return res


class Command(Enum):
    STOP = "STOP"
    UPDATE_TASK = "UPDATE_TASK"
    UPDATE_ASSET = "UPDATE_ASSET"
    UPDATE_TENANT = "UPDATE_TENANT"
