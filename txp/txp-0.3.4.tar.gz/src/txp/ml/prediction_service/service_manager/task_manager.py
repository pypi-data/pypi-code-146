from txp.common.utils.model_registry_utils import get_pubsub_ml_event_log
from txp.ml.prediction_service.service_manager.factories import TaskFactory, StateManagerFactory
from txp.ml.prediction_service.service_manager.actors_synchronizer import stateful_function, ActorsStack, \
    stateful_method
import ray
import logging


@ray.remote
@stateful_function
def predict_and_save_event(task, state_manager, segregator, sampling_window, message, task_id, asset_id,
                           actors_stack=None, log_level=logging.INFO):
    """After TaskManager decided which ml task and state manager to use this ray remote function sends the current
    prediction to selected state manager.

    Args:
        task: corresponding task for incoming edge message.
        state_manager: corresponding state manager for asset in message.
        segregator: signals segregator object.
        sampling_window: All PubSub messages collected for given task.
        message: last PubSub message arrived.
        task_id: ml task_id.
        actors_stack: actors stack object.
        asset_id: asset or machine id
        log_level: log level for module
    """
    logging.basicConfig(level=log_level)
    sampling_window_rows = segregator.get_sampling_window_rows_from_bigquery(sampling_window,
                                                                             message["observation_timestamp"],
                                                                             message["tenant_id"])
    predicted_event = task.predict(sampling_window_rows)
    logging.info(f'Prediction completed for. {get_pubsub_ml_event_log(message)}, prediction: {predicted_event}')
    event = {
        "event": predicted_event,
        "explainability": "{}",
        "task_id": task_id,
        "asset_id": asset_id,
        "observation_timestamp": message["observation_timestamp"],
        "event_id": f'{asset_id}-{task_id}-{message["observation_timestamp"]}',
        "tenant_id": message["tenant_id"],
        "partition_timestamp": message["partition_timestamp"]
    }

    logging.info(f"Processing event within state_manager: {get_pubsub_ml_event_log(message)}")
    state_manager.process_event.remote(event, message["gateway_task_id"], message["sampling_window_index"],
                                       message["number_of_sampling_windows"], actors_stack=actors_stack)
    logging.info(f"Event processed {get_pubsub_ml_event_log(message)}")


class TaskManager:
    """This class manages all ml tasks and state managers, basically this class decides which ml task and state
    manager to use by processing each PubSub message.

    Args:
        backup_collection_name: Firestore collection name where all backups are going to be stored.
        tenants_config: tenants configuration taken from firestore.
        events_and_states_dataset: Bigquery dataset where events and states are going to be stored.
        notifications_topic: PubSub topic id where notifications are going to be sent.
        _credentials_str: GCS credentials string.

    """

    def __init__(self, tenants_config, _credentials_str, backup_collection_name, events_and_states_dataset,
                 notifications_topic, reports_topic):
        self.actors_stack = ActorsStack.remote()
        self.tenants_config = tenants_config
        self.tasks = {}
        self.backup_collection_name = backup_collection_name
        self.events_and_states_dataset = events_and_states_dataset
        self.notifications_topic = notifications_topic
        self.reports_topic = reports_topic
        self.state_managers = {}
        for tenant_id in self.tenants_config:
            self.state_managers = {**self.state_managers,
                                   **StateManagerFactory.create_state_managers(
                                       self.tenants_config[tenant_id], _credentials_str, self.backup_collection_name,
                                       self.events_and_states_dataset, self.notifications_topic, self.reports_topic)}
            self.tasks = {**self.tasks, **TaskFactory.create_tasks(self.tenants_config[tenant_id], self.state_managers,
                                                                   _credentials_str)}

    def backup(self):
        logging.info("Backing up task manager, all state managers present at the service will be backed up")
        for sm_id in self.state_managers:
            ray.get(self.state_managers[sm_id].backup.remote())

    @stateful_method
    def process_messages(self, messages, signals_segregator):
        current_task = None
        current_state_manager = None

        for message in messages:

            logging.info(f"Event PubSub received. {get_pubsub_ml_event_log(message)}")

            task_id = None
            asset_id = None
            for tenant_id in self.tenants_config:
                for asset in self.tenants_config[tenant_id]:
                    for task in self.tenants_config[tenant_id][asset]['tasks'].values():
                        for edge in task['edges']:
                            if edge == message["edge_logical_id"]:
                                if self.tenants_config[tenant_id][asset]["state_manager"] not in self.state_managers \
                                        or task['task_id'] not in self.tasks:
                                    continue
                                asset_id = asset
                                task_id = task["task_id"]
                                current_task = self.tasks[task['task_id']]
                                current_state_manager = self.state_managers[
                                    self.tenants_config[tenant_id][asset_id]["state_manager"]]
            if current_task is None or current_state_manager is None:
                logging.info(
                    f"Current configuration is wrong not state manager or current task found for PubSub event. "
                    f"{get_pubsub_ml_event_log(message)}")
                continue
            schema = current_task.get_schema()
            completed = signals_segregator.process_message(message, schema, task_id)

            if completed:
                logging.info(f"All necessary PubSub event were received when {get_pubsub_ml_event_log(message)} "
                             f"was found, generating prediction.")

                sampling_window = signals_segregator.get_sampling_window(message["observation_timestamp"], task_id)
                signals_segregator.delete_sampling_window(message["observation_timestamp"], task_id)
                predict_and_save_event.remote(current_task, current_state_manager,
                                              signals_segregator.bigquery_segregator, sampling_window,
                                              message, task_id, asset_id, actors_stack=self.actors_stack)
