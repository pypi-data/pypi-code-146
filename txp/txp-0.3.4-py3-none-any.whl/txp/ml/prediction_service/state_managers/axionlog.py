from typing import Dict, List

from txp.ml.prediction_service.state_managers import state_manager as sm
from txp.common.ml.tasks import AssetTask
import logging
import datetime
import ray
from txp.common.ml.tasks import AssetState, AssetStateCondition


class BasicAxionlogGateAsset(sm.StateManager):
    """A Basic State Manager to detect the Open/Closed Door.


    This State Manager will only work for a single spot for a demonstration
    purpose.
    """

    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name, asset_tasks: List[AssetTask],
                 notifications_topic, reports_topic, credentials_str, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        super().__init__(asset_id, events_and_states_dataset, backup_collection_name, notifications_topic,
                         reports_topic, credentials_str)
        self.tasks = tasks
        self._last_open_door_datetime: datetime.datetime = None
        self._tasks_definitions: Dict[str, AssetTask] = {}
        for t in asset_tasks:
            self._tasks_definitions[t.task_id] = t

    def _get_state(self, ids: List, events: List, state_value: AssetStateCondition) -> AssetState:
        state = AssetState(
            events=ids,
            asset_id=self.asset_id,
            condition=state_value,
            observation_timestamp=events[0]["observation_timestamp"],
            tenant_id=events[0]["tenant_id"],
            partition_timestamp=events[0]["partition_timestamp"]
        )

        logging.info(
            f"{self.__class__.__name__} computed new state for asset {state.asset_id}. "
            f"New state value: {state.condition.value} "
        )
        return state

    def get_state(self, events):
        logging.info(
            f"[{self.__class__.__name__}] Received new events for "
            f"asset {events[0].get('asset_id', None)}"
        )

        event = events[0]
        int_label = self._tasks_definitions[event["task_id"]].label_def.label_to_int[event["event"]]
        if int_label == 1:
            # Detected a new OPTIMAL, last critical returns to None
            new_state = self._get_state([event["event_id"]], [events[0]], AssetStateCondition.OPTIMAL)
            self._last_open_door_datetime = None
            logging.info("[{self.__class__.__name__}] detected OPTIMAL. Open door timestamp goes back to None.")

        else:
            # Detected the Door opened. Compute the total open door time.
            if self._last_open_door_datetime is None:
                logging.info("[{self.__class__.__name__}] detected new Critical. "
                             "Open door timestamp will be remembered.")
                new_state = self._get_state([event["event_id"]], [events[0]], AssetStateCondition.GOOD)

                self._last_open_door_datetime = datetime.datetime.utcfromtimestamp(
                    event['observation_timestamp'] / 1e9
                )

            else:
                current_open_datetime = datetime.datetime.utcfromtimestamp(
                    event['observation_timestamp'] / 1e9
                )
                total_open_time = abs((current_open_datetime - self._last_open_door_datetime).total_seconds())

                if total_open_time <= 60:  # 1 minute is Good:
                    new_state = self._get_state([event["event_id"]], [events[0]], AssetStateCondition.GOOD)
                elif total_open_time <= 300:  # 5 minutes is Operative
                    new_state = self._get_state([event["event_id"]], [events[0]],
                                                AssetStateCondition.OPERATIONAL)
                else:  # more than 5 minutes is critical
                    new_state = self._get_state([event["event_id"]], [events[0]], AssetStateCondition.CRITICAL)

        return new_state


@ray.remote
class RayBasicAxionlogGateAsset(BasicAxionlogGateAsset):
    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name,
                 asset_tasks: List[AssetTask], notifications_topic, reports_topic, credentials_str,
                 log_level=logging.INFO):
        super().__init__(asset_id, tasks, events_and_states_dataset, backup_collection_name, asset_tasks,
                         notifications_topic, reports_topic, credentials_str, log_level)
