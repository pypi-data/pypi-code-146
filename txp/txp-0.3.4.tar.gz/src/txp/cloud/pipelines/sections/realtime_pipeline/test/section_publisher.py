from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json

CREDENTIALS_PATH = "../../../../../common/credentials/pub_sub_to_bigquery_credentials.json"
TOPIC_ID = "txp-reports"


class PubSubPublisher:

    def __init__(self, credentials_path, topic_id):
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.project_id = credentials.project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def publish(self, command):
        future = self.publisher.publish(self.topic_path, data=json.dumps(command).encode('utf-8'))
        return future.result()


def main():
    publisher = PubSubPublisher(CREDENTIALS_PATH, TOPIC_ID)
    publisher.publish({
        "tenant_id": "labshowroom-001",
        "type": "MockDoubleLine",
        "start_datetime": "2022-07-21 18:00:00.0+00:00",
        "end_datetime": "2022-07-21 19:00:00.0+00:00",
        "parameters": {
            "edge_logical_ids": [
                "icomox_1"
            ]
        },
        "section_id": "section_1"
    })


if __name__ == "__main__":
    main()
