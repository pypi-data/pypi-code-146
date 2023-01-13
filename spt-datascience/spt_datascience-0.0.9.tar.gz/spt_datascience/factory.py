from abc import ABC, abstractmethod
from spt_datascience.resources import ModelManagerResource, PipelineManagerResource, MLFlowResource
from spt_datascience.credentials import ModelManagerCredentials, PipelineManagerCredentials, MLFlowCredentials
from functools import partial


class Factory(ABC):

    @abstractmethod
    def get_resource_crede_pairs(self):
        pass

    def __init__(self, spt_resource_factory, **factory_params):
        self.factory_params = factory_params
        self.spt_resource_factory = spt_resource_factory
        self.resources = {}
        for resource, credentials in self.get_resource_crede_pairs():

            def get_resource(resource, credentials, **params):
                c = credentials(
                    spt_resource_factory=self.spt_resource_factory,
                    spt_ds_factory=self,
                    factory_params=self.factory_params,
                    custom_params=params
                )
                return resource(c).get_object()

            def get_credentials(credentials, **params):
                return credentials(
                    spt=self,
                    factory_params=self.factory_params,
                    custom_params=params
                ).get_credentials()

            setattr(self, f'get_{resource.get_name()}', partial(get_resource, resource=resource, credentials=credentials))
            setattr(self, f'get_{resource.get_name()}_credentials', partial(get_credentials, credentials=credentials))


class DsFactory(Factory):

    def get_resource_crede_pairs(self):
        return (
            (ModelManagerResource, ModelManagerCredentials),
            (PipelineManagerResource, PipelineManagerCredentials),
            (MLFlowResource, MLFlowCredentials)
        )
