from typing import Dict, List

from txp.ml.prediction_service.state_managers import state_manager as sm
from txp.common.ml.tasks import AssetTask
import logging
import datetime
import ray
from txp.common.ml.tasks import AssetState, AssetStateCondition


class BasicGaoAsset(sm.StateManager):

    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name, asset_tasks: List[AssetTask],
                 notifications_topic, reports_topic, credentials_str, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        super().__init__(asset_id, events_and_states_dataset, backup_collection_name, notifications_topic,
                         reports_topic, credentials_str)
        self.tasks = tasks
        self._last_state_value: AssetStateCondition = AssetStateCondition.UNDEFINED
        self._last_critical_by_operative_flag: bool = False
        self._last_operative_checkpoint = None
        self._operative_max_allowed_secs = 600

        self._tasks_definitions: Dict[str, AssetTask] = {}
        for t in asset_tasks:
            self._tasks_definitions[t.task_id] = t

    def _get_state(self, ids: List, events: List, state_value: AssetStateCondition) -> AssetState:
        state = AssetState(events=ids, asset_id=self.asset_id, condition=state_value,
                           observation_timestamp=events[0]["observation_timestamp"], tenant_id=events[0]["tenant_id"],
                           partition_timestamp=events[0]["partition_timestamp"])
        logging.info(f"{self.__class__.__name__} computed new state for asset {state.asset_id}. "
                     f"New state value: {state.condition.value} ")
        return state

    def get_state(self, events) -> AssetState:
        # TODO: returning mock state
        logging.info(f"{self.__class__.__name__} received new events for asset {events[0]['asset_id']}.")
        rcv_events_labels: Dict[str, int] = {}

        for event in events:
            rcv_events_labels[event['task_id']] = (
                self._tasks_definitions[event['task_id']].label_def.label_to_int[event['event']]
            )

        ids: List[str] = list(map(
            lambda event_obj: event_obj['event_id'],
            events
        ))

        TP_present = (
                rcv_events_labels['TP_01_SD'] + rcv_events_labels['TP_02_MD'] + rcv_events_labels['TP_03_ID']
        )

        SD_present = (
                rcv_events_labels['SD_01_SC'] + rcv_events_labels['SD_02_SC']
        )

        EMP_present = (
                rcv_events_labels['EMP_01_SI'] + rcv_events_labels['EMP_02_MI']
        )

        first_eval = TP_present + SD_present + EMP_present

        if first_eval >= 3 and TP_present and SD_present and EMP_present:
            """First strategy, we evaluate: 

               TP:
                 TP_01_SD, TP_02_MD, TP_02_ID

               SD:
                 SD_01_SC, SD_02_MC

               EMP: 
                EMP_01_SI
                EMP_02_MI

            If at least 1 perception on each of these groups is Present, 
            then the state is optimal.
            """
            logging.info('The new state is OPTIMAL, because there is profile in TP, SD and EMP')
            new_state = self._get_state(ids, events, AssetStateCondition.OPTIMAL)

        elif TP_present:
            """At this point, we'll look for Good state.

            Good state will be truth for any Present value in the group TP. 
            TP:
                 TP_01_SD, TP_02_MD, TP_02_ID
            """
            logging.info('The new state is Good, because there are packages on TP, but not '
                         'enough in EMP and SD.')
            new_state = self._get_state(ids, events, AssetStateCondition.GOOD)

        # let's check for the last operative checkpoint time difference
        elif SD_present or EMP_present:
            """In this case, we'll look for a Operative state. 
            
            It's operative if there are profile in SD or EMP. 
            
            But we'll be careful to look if Operative tolerance has been surpassed.
            """
            logging.info('The new state is Operative, because there are packages on SD or EMP, but not '
                         'enough for a better state.')

            if self._is_valid_operative():
                logging.info('The new state is Operative, because there are packages on SD or EMP')
                self._last_operative_checkpoint = datetime.datetime.now()
                new_state = self._get_state(ids, events, AssetStateCondition.OPERATIONAL)

            else:
                logging.info('The new state is CRITICAL, because Operative was detected but the Operative tolerance '
                             'was surpassed')
                self._last_critical_by_operative_flag = True
                new_state = self._get_state(ids, events, AssetStateCondition.CRITICAL)

        else:
            logging.info('The new state is CRITICAL, because all spots are empty of profiles')
            self._last_critical_by_operative_flag = False
            new_state = self._get_state(ids, events, AssetStateCondition.CRITICAL)

        self._last_state_value = new_state.condition
        return new_state

    def _is_valid_operative(self) -> bool:
        if self._last_state_value.name != 'OPERATIONAL' and self._last_state_value.name != 'CRITICAL':
            return True

        elif self._last_state_value.name == 'CRITICAL':
            return not self._last_critical_by_operative_flag

        else:
            return (datetime.datetime.now() - self._last_operative_checkpoint).total_seconds() < \
                   self._operative_max_allowed_secs


@ray.remote
class RayBasicGaoAsset(BasicGaoAsset):
    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name, asset_tasks: List[AssetTask],
                 notifications_topic, reports_topic, credentials_str, log_level=logging.INFO):
        super().__init__(asset_id, tasks, events_and_states_dataset, backup_collection_name, asset_tasks,
                         notifications_topic, reports_topic, credentials_str, log_level)
