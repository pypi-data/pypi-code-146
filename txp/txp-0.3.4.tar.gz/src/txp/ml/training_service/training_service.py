from typing import List

import ray
from fastapi import FastAPI, status
from ray import serve
from ray.actor import ActorHandle
from txp.common.ml.annotation import AnnotationLabelPayload
from txp.ml.training_service.dataset_committer import (
    RayDatasetCommitter,
    DatasetCommitPayload,
)
from txp.ml.training_service.training_manager import TrainingManager
from txp.ml.training_service.common import TrainCommand
from txp.ml.training_service.annotation_manager import AnnotationManager
from txp.ml.training_service.pre_annotation_manager import PreAnnotationManager
import time
import logging
from fastapi.responses import JSONResponse
import argparse

app = FastAPI()
ray.init()


@serve.deployment(route_prefix="/training", num_replicas=1)
@serve.ingress(app)
class TrainingService:
    def __init__(self, _credentials_str, models_bucket_name, data_warehouse_bucket_name,
                 prediction_service_topic, models_registry_collection_name, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        logging.info(
            f"Initialization started for deployment class {self.__class__.__name__}"
        )

        self._training_mgr: ActorHandle = TrainingManager.remote(_credentials_str, models_bucket_name,
                                                                 data_warehouse_bucket_name, prediction_service_topic,
                                                                 models_registry_collection_name, log_level)

        self._credentials_str = _credentials_str
        self._log_level = log_level

        logging.info(
            f"Initialization finished successfully for "
            f"deployment class {self.__class__.__name__}"
        )

    @app.get("/")
    def root(self):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Training service is up and running"},
        )

    @app.post("/train")
    def train(self, acknowledge: TrainCommand):
        logging.info(f"Received /train Request TrainCommand: {acknowledge.dict()}")
        res = ray.get(self._training_mgr.process_acknowledge.remote(acknowledge.dict()))
        if not res:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"Error: Requested Model not found"},
            )

        return JSONResponse(status_code=status.HTTP_200_OK, content={})

    @app.post("/publish")
    def publish(self, publish_command: TrainCommand):
        res = ray.get(self._training_mgr.process_publish.remote(publish_command.dict()))
        if not res:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"Error: Requested Model not found"},
            )

        return JSONResponse(status_code=status.HTTP_200_OK, content={})


@serve.deployment(route_prefix="/annotation", num_replicas=1)
@serve.ingress(app)
class AnnotationService:
    def __init__(self, _credentials_str, data_warehouse_bucket_name, models_registry_collection_name,
                 log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        logging.info(f"Initialization started for deployment {self.__class__.__name__}")

        self.data_warehouse_bucket_name = data_warehouse_bucket_name
        self._credentials_str = _credentials_str
        self._log_level = log_level
        self.models_registry_collection_name = models_registry_collection_name
        self._annotation_mgr: AnnotationManager = AnnotationManager.remote(
            self._credentials_str, self.models_registry_collection_name, self._log_level
        )

        logging.info(
            f"Initialization finished successfully for "
            f"deployment class {self.__class__.__name__}"
        )

    @app.post("/")
    def annotate(self, annotations: List[AnnotationLabelPayload]):
        logging.info(f"Receiving annotations to process in annotation service")
        r = self._annotation_mgr.process_new_annotations.remote(annotations)
        if r:
            logging.info(f"The annotation request was successful")
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={})
        else:
            logging.error("There was an error processing the annotations.")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={}
            )

    @app.post("/commit")
    def commit(self, commit_payload: DatasetCommitPayload):
        # Let's block waiting for the validation. Shouldn't take more than a few msecs.
        valid_commit = ray.get(self._annotation_mgr.validate_commit.remote(commit_payload))

        if not valid_commit:
            logging.error("The dataset commit was not valid. Returning error response")
            return JSONResponse(
                status_code=status.HTTP_412_PRECONDITION_FAILED, content={}
            )

        dataset_committer: ActorHandle = RayDatasetCommitter.remote(
            self._credentials_str, self.data_warehouse_bucket_name, self._log_level
        )
        dataset_committer.commit_dataset.remote(commit_payload)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={})

    @app.post("/pre-annotate")
    def pre_annotate(self, commit_payload: DatasetCommitPayload):
        # Let's block waiting for the validation. Shouldn't take more than a few msecs.
        valid_commit = ray.get(self._annotation_mgr.validate_pre_annotation_commit.remote(commit_payload))

        if not valid_commit:
            logging.error("The dataset commit was not valid. Returning error response")
            return JSONResponse(
                status_code=status.HTTP_412_PRECONDITION_FAILED, content={}
            )

        pre_annotation_manager: ActorHandle = PreAnnotationManager.remote(
            self._credentials_str, self.models_registry_collection_name, self._log_level
        )
        pre_annotation_manager.pre_annotate_dataset.remote(commit_payload)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={})


if __name__ == "__main__":
    serve.start()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--credentials_path",
        help="Google cloud credentials path",
        default="./credentials/pub_sub_to_bigquery_credentials.json",
    )

    parser.add_argument(
        "--models_bucket_name",
        help="GCS bucket name were joblib model files are going to be stored",
        default="txp-model-storage"
    )

    parser.add_argument(
        "--data_warehouse_bucket_name",
        help="GCS bucket name were parquet files for datasets are going to be stored",
        default="txp-data-warehouse"
    )

    parser.add_argument(
        "--prediction_service_topic",
        help="PubSub topic where prediction service is going to receive commands from",
        default="txp-model-serving-signals"
    )

    parser.add_argument(
        "--models_registry_collection_name",
        help="Firestore collection name where all model registries are going to be stored ",
        default="txp_models_registry"
    )

    known_args, _ = parser.parse_known_args()

    with open(known_args.credentials_path, "r") as file:
        credentials_str = file.read().replace("\n", "")
    TrainingService.deploy(credentials_str, known_args.models_bucket_name, known_args.data_warehouse_bucket_name,
                           known_args.prediction_service_topic, known_args.models_registry_collection_name,
                           logging.INFO)
    AnnotationService.deploy(credentials_str, known_args.data_warehouse_bucket_name,
                             known_args.models_registry_collection_name,  logging.INFO)

    while True:
        time.sleep(600)
