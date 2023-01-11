from abc import ABC, abstractmethod
from txp.ml.prediction_service.state_managers.state_manager_output import RayStateManagerOutput
from txp.ml.prediction_service.state_managers.state_manager_reporter import RayStateManagerReporter
import json
from google.oauth2 import service_account
from txp.ml.prediction_service.state_managers.state_controller import StateController
import google.cloud.firestore as firestore
from txp.common.config import settings
from txp.ml.prediction_service.service_manager.actors_synchronizer import stateful_method
from txp.common.utils.model_registry_utils import get_ml_event_log
from txp.common.ml.tasks import AssetState
import logging


class StateManager(ABC):
    """ An asset has multiple tasks all these tasks generate events, those events generates an state.
    This class in in charge of waiting for all the events to arrived and once all the events has arrived,
    this class creates an state.
    There is one state manager per each asset for a given tenant, this state manager classes are ad-hoc.
    It means someone has to code a new class for each new asset.

    Args:
        asset_id: machine id or asset id.
        events_and_states_dataset: BQ dataset name where events and state are going to be stored.
        backup_collection_name: Firestore collection name where backup is going to be stored.
        notifications_topic: PubSub topic id where notifications are going to be sent.
        credentials_str: GCP credentials string.
    """

    def __init__(self, asset_id, events_and_states_dataset, backup_collection_name, notifications_topic, reports_topic,
                 credentials_str):
        self.asset_id = asset_id
        json_dict_service_account = json.loads(credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        self.backup_collection_name = backup_collection_name
        self.firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
        self.tasks = None
        self.events_cache = {}
        self.state_controller = StateController()
        self.load_backup()
        self.state_manager_output = RayStateManagerOutput.remote(events_and_states_dataset, notifications_topic,
                                                                 credentials_str)
        self.state_manager_reporter = RayStateManagerReporter.remote(reports_topic, credentials_str)

    def backup(self):
        logging.info(f"Backing up state manager for {self.asset_id}")
        backup_collection = self.firestore_db.collection(self.backup_collection_name)
        state_controller_db_ref = backup_collection.document(settings.firestore.ray_state_controller_db_doc_name)
        state_controller_history_ref = backup_collection.document(
            settings.firestore.ray_state_controller_history_doc_name)
        state_manager_ref = backup_collection.document(settings.firestore.ray_state_manager_doc_name)
        if self.state_controller.states_db:
            logging.info(f"Backing up states db for {self.asset_id}")
            state_controller_db_ref.update({self.asset_id: self.state_controller.states_db})
        if self.state_controller.states_history:
            logging.info(f"Backing up states history for {self.asset_id}")
            state_controller_history_ref.update({self.asset_id: self.state_controller.states_history})
        if self.events_cache:
            logging.info(f"Backing up events cache for {self.asset_id}")
            state_manager_ref.update({self.asset_id: self.events_cache})
        logging.info(f"State manager backed up fo {self.asset_id}")

    def load_backup(self):
        logging.info(f"loading back up for {self.asset_id}")
        backup_collection = self.firestore_db.collection(self.backup_collection_name)
        state_controller_db_ref = backup_collection.document(settings.firestore.ray_state_controller_db_doc_name)
        state_controller_history_ref = backup_collection.document(
            settings.firestore.ray_state_controller_history_doc_name)
        state_manager_ref = backup_collection.document(settings.firestore.ray_state_manager_doc_name)

        state_controller_db = state_controller_db_ref.get({self.asset_id}).to_dict()
        if state_controller_db:
            self.state_controller.states_db = state_controller_db[self.asset_id]
            state_controller_db_ref.update({self.asset_id: firestore.DELETE_FIELD})
            logging.info(f"State controller db loaded for {self.asset_id}")
        else:
            logging.info(f"There is no previous state controller db entries for {self.asset_id}")

        state_controller_history = state_controller_history_ref.get({self.asset_id}).to_dict()
        if state_controller_history:
            self.state_controller.states_history = state_controller_history[self.asset_id]
            state_controller_history_ref.update({self.asset_id: firestore.DELETE_FIELD})
            logging.info(f"State controller history loaded for {self.asset_id}")
        else:
            logging.info(f"There is no previous state controller history entries for {self.asset_id}")

        state_manager = state_manager_ref.get({self.asset_id}).to_dict()
        if state_manager:
            self.events_cache = state_manager[self.asset_id]
            state_manager_ref.update({self.asset_id: firestore.DELETE_FIELD})
            logging.info(f"events cache loaded for {self.asset_id}")
        else:
            logging.info(f"There is no previous events cache for {self.asset_id}")
        logging.info(f"Backup loaded for {self.asset_id}")

    @abstractmethod
    def get_state(self, events) -> AssetState:
        pass

    def process_new_state(self, state, gateway_task_id):
        self.insert_state_to_bigquery(state)
        self.notify_new_state(state)

    def insert_events_to_bigquery(self, events):
        self.state_manager_output.insert_events_to_bigquery.remote(events)

    def insert_state_to_bigquery(self, state):
        self.state_manager_output.insert_state_to_bigquery.remote(state)

    def notify_new_state(self, state):
        self.state_manager_output.publish_to_pubsub.remote(state)

    def check_events_completeness(self, events):
        events_tasks = [event["task_id"] for event in events]
        for task in self.tasks:
            if task not in events_tasks:
                logging.info(f"There is no event for task_id: {task}, event is not completed")
                return False
        return True

    def store_event(self, event):
        observation_timestamp = str(event["observation_timestamp"])
        if observation_timestamp in self.events_cache:
            self.events_cache[observation_timestamp].append(event)
        else:
            self.events_cache[observation_timestamp] = [event]
        logging.info(f"Event {get_ml_event_log(event)}, stored at state manager cache")

    def delete_events_from_cache(self, observation_timestamps):
        events = []
        for observation_timestamp_ in observation_timestamps:
            observation_timestamp = str(observation_timestamp_)
            logging.info(f"Deleting events at state manager cache for {observation_timestamp}")
            events += self.events_cache[observation_timestamp]
            self.events_cache.pop(observation_timestamp)
        if events:
            self.insert_events_to_bigquery(events)

    @stateful_method
    def process_event(self, event, gateway_task_id, sampling_window_index, number_of_sampling_windows):
        logging.info(f"Trying to generate state for {get_ml_event_log(event)}")
        self.store_event(event)
        new_state = None
        observation_timestamp = str(event["observation_timestamp"])
        events = self.events_cache[observation_timestamp]
        logging.info(f"Checking event completeness for {get_ml_event_log(event)}")
        logging.info(f"{events}, were found")
        if self.check_events_completeness(events):
            logging.info(f"All necessary events were found when {get_ml_event_log(event)}, "
                         f"arrived generating a new state")
            generated_state = json.loads(self.get_state(events).json())
            logging.info(f"new state generated {generated_state}")

            self.state_controller.save_state(generated_state, gateway_task_id, sampling_window_index,
                                             number_of_sampling_windows)
            new_state = self.state_controller.get_state(gateway_task_id)
            processed_states = []
            while new_state is not None:
                logging.info(f"Processing new state {new_state}")
                self.process_new_state(new_state, gateway_task_id)
                self.state_manager_reporter.generate_report.remote(new_state["tenant_id"])
                logging.info(f"State processed {new_state}")
                self.state_controller.enqueue_state(new_state, gateway_task_id)
                logging.info(f"State enqueued at states history {new_state}")
                processed_states.append(new_state["observation_timestamp"])
                self.state_controller.clear_history(gateway_task_id)
                new_state = self.state_controller.get_state(gateway_task_id)
            self.delete_events_from_cache(processed_states)
        else:
            logging.info(f"There are still missing events {get_ml_event_log(event)}")
        return new_state

    def get_last_states(self, number_of_states, gateway_task_id):
        return self.state_controller.get_states_history(gateway_task_id, number_of_states)
