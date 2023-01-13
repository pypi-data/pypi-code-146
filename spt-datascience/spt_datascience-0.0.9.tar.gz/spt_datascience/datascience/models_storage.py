from abc import abstractmethod

from typing import TypeVar
from spt_factory.factory import Factory as ResourceFactory

from spt_datascience.datascience.singleton import Singleton
from spt_datascience.datascience.models.base_model import ModelConfig

DSFactory = TypeVar('DSFactory')

DEFAULT_MODELS_BUCKET = 'theme-models'


class ModelStorage:

    @abstractmethod
    def upload_model_bins(self, model_config: ModelConfig):
        pass

    @abstractmethod
    def load_model_bins(self, model_config: ModelConfig):
        pass


class S3ModelStorage(ModelStorage, metaclass=Singleton):

    def __init__(self, spt_resource_factory: ResourceFactory):
        self.s3_client = spt_resource_factory.get_s3_manager()
        self.mongo_client = spt_resource_factory.get_mongo()

    def upload_model_bins(self, model_config: ModelConfig):
        for bin_name, bin_obj in model_config.bins.items():
            model_path = f"{model_config.id}/{bin_name}"
            self.s3_client.upload_bin(bucket_name=DEFAULT_MODELS_BUCKET, id=model_path, bin_str=bin_obj)
            model_config.bins[bin_name] = model_path
        return model_config

    def load_model_bins(self, model_config: ModelConfig):
        model_bins = model_config.bins
        model_bucket = DEFAULT_MODELS_BUCKET
        for bin_name, bin_path in model_bins.items():
            model_bins[bin_name] = self.s3_client.download_bin(bucket_name=model_bucket, id=bin_path)
        model_config.bins = model_bins
        return model_config

    def delete_model(self, model_id: str):
        self.mongo_client.spt.models.delete_one({'id': model_id})
        self.s3_client.delete_folder(DEFAULT_MODELS_BUCKET, model_id)


class MLFlowSklearnModelStorage(ModelStorage, metaclass=Singleton):

    def __init__(self, spt_resource_factory: ResourceFactory, ds_factory: DSFactory):
        self.spt_resource_factory = spt_resource_factory
        self.ds_factory = ds_factory
        self.mlflow = ds_factory.get_mlflow()

    def upload_model_bins(self, model_config: ModelConfig):
        raise NotImplemented("Save mlflow model using mlflow API")

    def load_model_bins(self, model_config: ModelConfig):
        model_bins = model_config.bins
        for bin_name, bin_value in model_bins.items():
            model_uri = f"models:/{bin_value['name']}/{bin_value['version']}"
            model_bins[bin_name] = self.mlflow.sklearn.load_model(model_uri)
        return model_config


class RestModelStorage(ModelStorage, metaclass=Singleton):

    def __init__(self, spt_resource_factory: ResourceFactory):
        self.spt_resource_factory = spt_resource_factory

    def upload_model_bins(self, model_config: ModelConfig):
        raise NotImplemented("Save mlflow model using mlflow API")

    def load_model_bins(self, model_config: ModelConfig):
        with self.spt_resource_factory.get_mongo() as mongo_client:
            mlflow_rest_credes = mongo_client.spt.credentials.find_one({"type": "mlflow_rest"})
        model_config.bins['model_url'] = mlflow_rest_credes['model_url_template'].format(model_name=model_config.name)
        model_config.bins['user'] = mlflow_rest_credes['user']
        model_config.bins['password'] = mlflow_rest_credes['password']
        return model_config
