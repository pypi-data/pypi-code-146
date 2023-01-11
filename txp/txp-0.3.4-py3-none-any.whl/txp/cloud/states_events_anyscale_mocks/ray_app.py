import time
import datetime

PRESENT_PROFILE = "HAY PERFIL"
NO_PRESENT_PROFILE = "NO HAY PERFIL"

EDGES = EDGE_TO_SPOT_ID = [
  "TXP-ARMROBOT-001_3e5be60c7a826a1e32eb9913ed11170f",
  "TXP-ARMROBOT-001_c0fcd732d555d7eb1752f65b83b8e6d5",
  "TXP-ARMROBOT-001_d5bdaeb38990169d310caa3e47b7a951",
  "TXP-ARMROBOT-001_e135617e7c30e4fea19c15d764050d13",
  "TXP-ARMROBOT-001_edc659ad2449fd102d70d1317446a437",
  "TXP-ARMROBOT-001_0a333974dfe6f2a6c55e8846ca5d82ff",
  "TXP-ARMROBOT-001_dfd684239c39d781de18751d9c62a72a",
]


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

    def generate_new_event(self):
        import txp.cloud.controllers.big_query_events_states_sim as bq_simulator

        row: bq_simulator.AssetEvent = bq_simulator.AssetEvent(
            self._event_id,
            self._next_event,
            "{}",
            self._asset,
            self._spot,
            self._logical_id,
            self._window_timestamp
        )

        row = json.loads(json.dumps(dataclasses.asdict(row)))

        try:
            bq_simulator.write_row_to_bigquery_table(row, bq_simulator.EVENTS_DATASET, bq_simulator.EVENTS_TABLE)
            return f"""New row added for event {row['event_id']}"""

        except RuntimeError as e:
            return f"""ERROR while creating simulated event {e} """


if __name__ == '__main__':
    runtime_env = {
        'py_modules': ['/home/marco_sandoval/txp-0.1.83-py3-none-any.whl'],
    }
    ray.init(address="auto", runtime_env=runtime_env)

    new_event = PRESENT_PROFILE
    tm = int(datetime.datetime.now().timestamp() * 1e9)

    while True:
        print('Going to generate a new set of events.')

        generators = [EventGeneratorActor.remote(edge, new_event, tm) for edge in EDGES]
        futures = [generator.generate_new_event.remote() for generator in generators]
        print(ray.get(futures))

        new_event = PRESENT_PROFILE if new_event == NO_PRESENT_PROFILE else NO_PRESENT_PROFILE
        time.sleep(600)
