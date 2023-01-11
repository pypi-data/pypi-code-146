from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
from txp.ml.prediction_service.service_manager.prediction_manager import Command

CREDENTIALS_PATH = "../../../common/credentials/pub_sub_to_bigquery_credentials.json"
TOPIC_ID = "txp-model-serving-signals"

"""
    This module allows to publish a new command to ray service.
    We are currently supporting 2 kind of commands:
    
    Service update task:
        When a new model is trained we need to update current configuration for a given tenant_id, asset_id, task_id:
        {"command": Command.UPDATE_TASK.value, 
        "parameters": {"tenant_id": <TENANT_ID>, "asset_id": <ASSET_ID>, "task_id": <TASK_ID>}}
        
    Service update asset:
        If you to update a single asset of a tenant:
        {"command": Command.UPDATE_ASSET.value, 
        "parameters": {"tenant_id": <TENANT_ID>, "asset_id": <ASSET_ID>}}
        
    Service update tenant:
        Update or create tenant configuration:
        {"command": Command.UPDATE_ASSET.value, 
        "parameters": {"tenant_id": <TENANT_ID>}}
    
    Stop service:
        If you want to stop ray service safety you must publish:
        {"command": Command.STOP.value, "parameters": {}}
"""


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
    publisher.publish({"command": Command.STOP.value,
                       "parameters": {}})


if __name__ == "__main__":
    main()
