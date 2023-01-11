import ray
from fastapi import FastAPI, status
from ray import serve
from txp.ml.prediction_service.service_manager.prediction_manager import PredictionManager
import time
import logging
import argparse
from fastapi.responses import JSONResponse

app = FastAPI()
ray.init()

"""Prediction service.

Args:
    backup_collection_name: Firestore collection name where all backups are going to be stored.

    dataset: Bigquery dataset name where data is going to be read from, this is where telemetry data is stored.

    events_and_states_dataset: Bigquery dataset where events and states are going to be stored.

    subscription_id: PubSub subscription id where signal messages are going to come from, this is the input
    of the service.

    notifications_topic: PubSub topic id where notifications are going to be sent.

    credentials_path: GCS credentials local file path.

"""


@serve.deployment(route_prefix="/prediction", num_replicas=1)
@serve.ingress(app)
class PredictionService:
    def __init__(self, backup_collection_name, dataset, events_and_states_dataset, subscription_id, notifications_topic,
                 reports_topic, _credentials_str, log_level=logging.INFO):

        logging.basicConfig(level=log_level)
        logging.info(f"Initialization started for deployment {self.__class__.__name__}")

        self.__credentials_str = _credentials_str
        self.__log_level = log_level
        self.__prediction_mgr: PredictionManager = \
            PredictionManager.remote(dataset, subscription_id, backup_collection_name, events_and_states_dataset,
                                     notifications_topic, reports_topic, self.__credentials_str, self.__log_level)

        logging.info(f"Initialization finished successfully for deployment class {self.__class__.__name__}")

    @app.get("/")
    def root(self):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Training service is up and running"},
        )


if __name__ == "__main__":
    serve.start()

    parser = argparse.ArgumentParser()
    parser.add_argument("--backup_collection_name", help="Backup collection name",
                        default='ray_service_backup_test')
    parser.add_argument("--dataset", help="Dataset name where data is stored",
                        default="telemetry_test")
    parser.add_argument("--events_and_states_dataset",
                        help="Dataset name where events and state are going to be stored",
                        default="ml_events_and_states_test")
    parser.add_argument("--subscription_id", help="pubsub subscription id where messages are going to come from",
                        default="txp-model-serving-signals-test-sub")
    parser.add_argument("--notifications_topic", help="pubsub topic id where notifications are going to be sent",
                        default="txp-notifications-local-test")
    parser.add_argument("--credentials_path", help="Google cloud credentials path",
                        default="./credentials/pub_sub_to_bigquery_credentials.json")

    parser.add_argument("--reports_topic", help="PubSub topic where section requests are sent",
                        default="txp-reports-test")

    known_args, _ = parser.parse_known_args()

    with open(known_args.credentials_path, 'r') as file:
        credentials_str = file.read().replace('\n', '')

    PredictionService.deploy(known_args.backup_collection_name, known_args.dataset,
                             known_args.events_and_states_dataset, known_args.subscription_id,
                             known_args.notifications_topic, known_args.reports_topic, credentials_str, logging.INFO)

    while True:
        time.sleep(600)
