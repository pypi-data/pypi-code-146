from abc import ABC, abstractmethod
from functools import lru_cache
from uuid import uuid4

from spt_datascience.datascience.singleton import Singleton
from spt_datascience.datascience.model_manager import ModelManager
from spt_datascience.datascience.pipelines.base_pipeline import BasePipeline, PipelineConfig
from importlib import import_module


class PipelineManager(metaclass=Singleton):

    @abstractmethod
    def get_pipeline(self, pipeline_id) -> BasePipeline:
        """
        Get pipelines by pipeline_id
        :param pipeline_id:
        :return: pipelines object
        """
        pass

    @abstractmethod
    def save_pipeline(self, pipeline: BasePipeline) -> str:
        """
        Save pipelines info
        :param pipeline: pipelines to save
        :return:
        """
        pass


class SPTPipelineManager(PipelineManager):

    def __init__(self, spt_resource_factory, model_manager):
        self.spt_resource_factory = spt_resource_factory
        self.model_manager = model_manager

    def load_pipeline_object(self, pipeline_package, pipeline_class, config, model_manager):
        module = import_module(pipeline_package)
        return getattr(
            module, pipeline_class
        ).load_pipeline(config, model_manager)

    @lru_cache(maxsize=512)
    def get_pipeline(self, pipeline_id) -> BasePipeline:
        with self.spt_resource_factory.get_mongo() as mongo_client:
            pipeline_config_dict = mongo_client.spt.pipelines.find_one({'pipeline_id': pipeline_id})
        pipeline_config = PipelineConfig.from_dict(pipeline_config_dict)

        pipeline_package = pipeline_config.pipeline_package
        pipeline_class = pipeline_config.pipeline_class

        return self.load_pipeline_object(
            pipeline_package,
            pipeline_class,
            pipeline_config,
            self.model_manager
        )

    def save_pipeline(self, pipeline: BasePipeline) -> str:
        pipeline_id = str(uuid4())
        pipeline_config = pipeline.save_pipeline(pipeline_id).to_dict()
        with self.spt_resource_factory.get_mongo() as mongo_client:
            mongo_client.spt.pipelines.insert_one(pipeline_config)
        return pipeline_id

    def save_pipeline_config(self, pipeline_config: PipelineConfig):
        with self.spt_resource_factory.get_mongo() as mongo_client:
            mongo_client.spt.pipelines.insert_one(pipeline_config.to_dict())

    def delete_pipeline(self, pipeline_id):
        with self.spt_resource_factory.get_mongo() as mongo_client:
            mongo_client.spt.pipelines.delete_one({'id': pipeline_id})


