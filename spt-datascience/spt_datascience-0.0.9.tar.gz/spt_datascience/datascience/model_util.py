from abc import abstractmethod

from spt_datascience.datascience.singleton import Singleton
from spt_datascience.datascience.models.base_model import ModelConfig
from datetime import datetime


class ModelUtil(metaclass=Singleton):

    @abstractmethod
    def get_model_version(self, model_name) -> int:
        """
        return last model version
        :param model_name: name of the model
        :return: model version
        """
        pass

    @abstractmethod
    def save_model_config(self, model_config: ModelConfig):
        """
        :param model_config: model info
        """
        pass


class MongoModelUtil(ModelUtil):

    def __init__(self, spt_resource_factory):
        self.spt_resource_factory = spt_resource_factory

    @staticmethod
    def _fix_dict(d: dict):
        return {
            str(key): value if type(value) != dict else MongoModelUtil._fix_dict(value)
            for key, value in d.items()
        }

    def get_model_version(self, model_name) -> int:
        with self.spt_resource_factory.get_mongo() as mongo_client:
            models_info = list(mongo_client.spt.models.find({"name": model_name}).sort("version", -1))
        for model_info in models_info:
            return model_info['version']
        return 0

    def save_model_config(self, model_config):
        model_config_dict = model_config.to_dict()
        model_config_dict['date'] = str(datetime.now())
        with self.spt_resource_factory.get_mongo() as mongo_client:
            mongo_client.spt.models.insert_one(
                MongoModelUtil._fix_dict(model_config_dict)
            )
