from typing import List

from txp.ml.prediction_service.state_managers import state_manager as sm
import ray
import logging
from txp.common.ml.tasks import AssetState, AssetStateCondition
from txp.common.ml.tasks import AssetTask, ClassificationLabelDefinition


class BeerShowroomAsset(sm.StateManager):

    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name, notifications_topic,
                 reports_topic, credentials_str, asset_tasks_dict, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        super().__init__(asset_id, events_and_states_dataset, backup_collection_name, notifications_topic,
                         reports_topic, credentials_str)
        self.tasks = tasks
        self.tasks_dict = asset_tasks_dict
        self.states_count = 3
        self.non_persisted_count = 0
        logging.info(f"BeerShowroomAsset state manager "
                     f"loaded with {len(self.tasks)} tasks configured")
        for t in self.tasks:
            logging.info(f"Task Definition: {t}")

    def get_state(self, events):
        """
        Args:

            events: List of events produced by the tasks associated to this
                Asset.

        Return:
            A state object (typing.Dict)
        """
        recv_events: List[str] = list(map(
            lambda event_obj: event_obj['event'],
            events
        ))

        classification_task_def: ClassificationLabelDefinition = self.tasks_dict['bottle_detection'].label_def

        recv_event = recv_events[0]

        # This State manager expects a list of values
        predicted_lbls = dict(
            list(map(
                lambda lbl: (classification_task_def.label_to_category[lbl], lbl),
                recv_event
            ))
        )

        # BottleBeerPresence
        beer_present = predicted_lbls['ObjectPresence']

        logging.info(f"{self.__class__.__name__} received new events for asset {events[0]['asset_id']}. "
                     f"Received events: {predicted_lbls}")

        ids: List[str] = list(map(
            lambda event_obj: event_obj['event_id'],
            events
        ))

        if beer_present == 'ObjectPresent':
            state_val = AssetStateCondition.OPTIMAL
        else:
            state_val = AssetStateCondition.CRITICAL

        state = AssetState(events=ids, asset_id=self.asset_id,
                           condition=state_val,
                           observation_timestamp=events[0]["observation_timestamp"],
                           tenant_id=events[0]["tenant_id"],
                           partition_timestamp=events[0]["partition_timestamp"])

        logging.info(f"{self.__class__.__name__} computed new state for asset {state.asset_id}. "
                     f"New state value: {state.condition.value} ")
        return state

    def process_new_state(self, state, gateway_task_id):
        logging.info(f"{self.__class__.__name__} Requested to process new state")
        last_states = self.get_last_states(self.states_count, gateway_task_id)
        # number of states needed to decide to write in the table
        if not len(last_states):
            # TODO: Change to log usage when available
            logging.info(f"{self.__class__.__name__} new state for a new Gateway Task ID. "
                         f"Persist into Database...")
            self.insert_state_to_bigquery(state)
            return

        # if new state is different that the immediate previous one, then write
        if state["condition"] != last_states[0]["condition"]:
            logging.info(f"{self.__class__.__name__} new state different than the previous one. "
                         f"Persist into Database...")
            self.insert_state_to_bigquery(state)
            self.notify_new_state(state)
            return

        self.non_persisted_count += 1


@ray.remote
class RayBasicShowroomBeerAsset(BeerShowroomAsset):
    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name, notifications_topic,
                 reports_topic, credentials_str, asset_tasks_dict, log_level=logging.INFO):
        super().__init__(asset_id, tasks, events_and_states_dataset, backup_collection_name, notifications_topic,
                         reports_topic, credentials_str, asset_tasks_dict, log_level)
