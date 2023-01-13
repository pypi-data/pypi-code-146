from abc import ABC, abstractmethod

import mlflow
import os

from spt_datascience.credentials import Credentials
from spt_datascience.datascience.model_manager import SPTModelManager
from spt_datascience.datascience.model_util import MongoModelUtil
from spt_datascience.datascience.models_storage import  S3ModelStorage
from spt_datascience.datascience.pipeline_manager import SPTPipelineManager



class Resource(ABC):

    def __init__(self, c: Credentials):
        self.c = c

    @abstractmethod
    def get_object(self):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass


class ModelManagerResource(Resource):

    def get_object(self):
        credential = self.c.get_credentials()
        return SPTModelManager(
            spt_resource_factory=credential['spt_resource_factory'],
            spt_ds_factory=credential['spt_ds_factory']
        )

    @staticmethod
    def get_name():
        return 'model_manager'


class MLFlowResource(Resource):

    def get_object(self):
        credential = self.c.get_credentials()
        os.environ['MLFLOW_TRACKING_USERNAME'] = credential['user']
        os.environ['MLFLOW_TRACKING_PASSWORD'] = credential['password']
        mlflow.set_tracking_uri(credential['tracking_uri'])
        return mlflow

    @staticmethod
    def get_name():
        return 'mlflow'


class PipelineManagerResource(Resource):

    def get_object(self):
        credential = self.c.get_credentials()
        return SPTPipelineManager(
            spt_resource_factory=credential['spt_resource_factory'],
            model_manager=credential['spt_ds_factory'].get_model_manager()
        )

    @staticmethod
    def get_name():
        return 'pipeline_manager'
