from abc import ABC, abstractmethod


class Credentials(ABC):
    __slots__ = 'crede', 'crede_object', 'factory_params', 'custom_params', 'spt_resource_factory'

    def __init__(self, spt_resource_factory, spt_ds_factory, factory_params, custom_params):
        self.spt_resource_factory = spt_resource_factory
        self.spt_ds_factory = spt_ds_factory
        self.factory_params = factory_params
        self.custom_params = custom_params

    def get_credentials(self):
        return self.crede


class ModelManagerCredentials(Credentials):

    def __init__(self, spt_resource_factory, spt_ds_factory, factory_params, custom_params):
        super().__init__(spt_resource_factory, spt_ds_factory, factory_params, custom_params)
        self.crede = dict(spt_resource_factory=spt_resource_factory, spt_ds_factory=spt_ds_factory)


class PipelineManagerCredentials(Credentials):

    def __init__(self, spt_resource_factory, spt_ds_factory, factory_params, custom_params):
        super().__init__(spt_resource_factory, spt_ds_factory, factory_params, custom_params)
        self.crede = dict(spt_resource_factory=spt_resource_factory, spt_ds_factory=spt_ds_factory)


class S3ModelManagerCredentials(Credentials):

    def __init__(self, spt_resource_factory, spt_ds_factory, factory_params, custom_params):
        super().__init__(spt_resource_factory, spt_ds_factory, factory_params, custom_params)
        self.crede = dict(spt_resource_factory=spt_resource_factory, spt_ds_factory=spt_ds_factory)


class MLFlowCredentials(Credentials):

    def __init__(self, spt_resource_factory, spt_ds_factory, factory_params, custom_params):
        super().__init__(spt_resource_factory, spt_ds_factory, factory_params, custom_params)
        with spt_resource_factory.get_mongo() as mongo_client:
            mlflow_crede = mongo_client.spt.credentials.find_one({"type": "mlflow"})
        self.crede = mlflow_crede
