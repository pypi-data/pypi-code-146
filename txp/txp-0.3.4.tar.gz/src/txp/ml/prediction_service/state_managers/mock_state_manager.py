from txp.ml.prediction_service.state_managers import state_manager as sm
import ray
from txp.common.ml.tasks import AssetState, AssetStateCondition
import logging


class MockAsset(sm.StateManager):
    states_map = {
        "Ok": AssetStateCondition.OPTIMAL,
        "Bad": AssetStateCondition.CRITICAL
    }

    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name, notifications_topic,
                 reports_topic, credentials_str, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        super().__init__(asset_id, events_and_states_dataset, backup_collection_name, notifications_topic,
                         reports_topic, credentials_str)
        self.tasks = tasks

    def get_state(self, events) -> AssetState:
        event = events[0]
        ids = [event["event_id"]]
        return AssetState(events=ids,
                          asset_id=self.asset_id,
                          condition=MockAsset.states_map.get(event["event"], AssetStateCondition.UNDEFINED),
                          observation_timestamp=event["observation_timestamp"],
                          tenant_id=event["tenant_id"],
                          partition_timestamp=event["partition_timestamp"])


@ray.remote
class RayMockAsset(MockAsset):
    def __init__(self, asset_id, tasks, events_and_states_dataset, backup_collection_name, notifications_topic,
                 reports_topic, credentials_str, log_level=logging.INFO):
        super().__init__(asset_id, tasks, events_and_states_dataset, backup_collection_name, notifications_topic,
                         reports_topic, credentials_str, log_level)
