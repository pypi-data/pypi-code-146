import ray
import json
import dataclasses


@ray.remote
class EventGeneratorActor:

    def __init__(
            self,
            logical_id: str,
            event: str,
            sw_timestamp: int
    ):
        import txp.cloud.controllers.big_query_events_states_sim as bq_simulator
        self._next_event: str = event
        self._logical_id = logical_id
        self._spot = bq_simulator.EDGE_TO_SPOT_ID[self._logical_id]
        self._asset = bq_simulator.ASSET_ID
        self._window_timestamp = sw_timestamp
        self._event_id = bq_simulator.AssetEvent.get_id(
            self._logical_id, self._asset, self._spot, self._window_timestamp
        )

    def generate_new_event(self) -> None:
        import txp.cloud.controllers.big_query_events_states_sim as bq_simulator

        row = bq_simulator.AssetEvent(
            self._event_id,
            self._next_event,
            "{}",
            self._asset,
            self._spot,
            self._logical_id,
            self._window_timestamp
        )

        row = json.loads(json.dumps(dataclasses.asdict(row)))

        bq_simulator.write_row_to_bigquery_table(row, bq_simulator.EVENTS_DATASET, bq_simulator.EVENTS_TABLE)
        print(f"New Event received to generate {self._event_id}")
