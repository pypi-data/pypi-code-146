import base64
import json
from google.oauth2 import service_account
from google.cloud import bigquery
import ray
from txp.ml.prediction_service.service_manager.actors_synchronizer import stateful_method
from google.cloud import pubsub_v1
import logging
import txp.common.protos.user_notification_pb2 as notifications_proto


class StateManagerOutput:
    """ This class is in charge of managing the output for a given state manager.
    A notification is going to be sent each time a new state is stored in bigquery.
    Args:
        events_and_states_dataset: BQ dataset name where events and state are going to be stored.
        notifications_topic: PubSub topic id where notifications are going to be sent.
        credentials_str: GCP credentials string.
    """

    def __init__(self, events_and_states_dataset, notifications_topic, credentials_str, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        self.events_table_id = "events"
        self.states_table_id = "states"
        self.notifications_topic = notifications_topic
        json_dict_service_account = json.loads(credentials_str, strict=False)
        self.credentials = service_account.Credentials.from_service_account_info(json_dict_service_account)
        self.bigquery_client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
        self.dataset = f"{self.credentials.project_id}.{events_and_states_dataset}"

    def __insert_rows_to_bigquery(self, rows, table_id):
        errors = self.bigquery_client.insert_rows_json(f"{self.dataset}.{table_id}", rows)
        if errors:
            logging.info(f"""Could not store in {table_id}: {rows} """)
            return False
        else:
            return True

    @stateful_method
    def insert_events_to_bigquery(self, events):
        for event in events:
            event["event"] = json.dumps(event["event"])
        res = self.__insert_rows_to_bigquery(events, self.events_table_id)
        if res:
            logging.info(f"{len(events)}, Events were stored in bigquery")

    @stateful_method
    def insert_state_to_bigquery(self, state):
        res = self.__insert_rows_to_bigquery([state], self.states_table_id)
        if res:
            logging.info(f'new state stored to bigquery: {state["observation_timestamp"]}')

    @staticmethod
    def __state_from_dict_to_proto(state):
        notification_proto = notifications_proto.Notification()
        notification_proto.content.asset_id = state["asset_id"]
        notification_proto.content.tenant_id = state["tenant_id"]
        notification_proto.content.predicted_condition = state["condition"]
        notification_proto.type = notifications_proto.Notification.NotificationType.STATE_CHANGE
        return notification_proto

    @stateful_method
    def publish_to_pubsub(self, state):
        proto = self.__state_from_dict_to_proto(state)
        encoded_payload = base64.b64encode(proto.SerializeToString())
        publisher = pubsub_v1.PublisherClient(credentials=self.credentials)
        topic_path = publisher.topic_path(self.credentials.project_id, self.notifications_topic)
        future = publisher.publish(topic_path, data=encoded_payload)
        future.result()
        logging.info(f"New State published to PubSub {state}")


@ray.remote
class RayStateManagerOutput(StateManagerOutput):
    def __init__(self, events_and_states_dataset, notifications_topic, credentials_str):
        super().__init__(events_and_states_dataset, notifications_topic, credentials_str)
