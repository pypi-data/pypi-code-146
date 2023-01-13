from abc import ABC, abstractmethod


class ModelConfig:

    def __init__(self, id, name, version, extra, model_package, model_class, bins, storage_type='s3'):
        self.id = id
        self.name = name
        self.storage_type = storage_type
        self.extra = extra
        self.version = version
        self.model_package = model_package
        self.model_class = model_class
        self.bins = bins

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'extra': self.extra,
            'model_package': self.model_package,
            'model_class': self.model_class,
            'bins': self.bins,
            'storage_type': self.storage_type
        }

    @staticmethod
    def from_dict(config_dict):

        return ModelConfig(
            id=config_dict['id'],
            name=config_dict['name'],
            version=config_dict['version'],
            extra=config_dict['extra'],
            model_package=config_dict['model_package'],
            model_class=config_dict['model_class'],
            bins=config_dict['bins'],
            storage_type=config_dict.get('storage_type', 's3')
        )

    @staticmethod
    def default_config():
        return ModelConfig(
            id=None,
            name=None,
            version=None,
            extra={},
            model_package=None,
            model_class=None,
            bins={},
            storage_type='s3'
        )

    def __str__(self):
        return self.to_dict()

    def _repr_html_(self):
        return """
        <p><h3>%s</h3></p>
        <div><b>id</b>: %s</div>
        <div><b>version</b>: %s</div>
        <div><b>package</b>: %s</div>
        <div><b>class</b>: %s</div>
        <div><b>extra</b>: %s</div>
        """ % (self.name, self.id, self.version, self.model_package, self.model_class, self.extra)


class BaseModel(ABC):

    @abstractmethod
    def save_model(self, model_id, version) -> ModelConfig:
        """
        Save model files
        :return: config dict
        """
        raise NotImplemented()

    @staticmethod
    @abstractmethod
    def load_model(config: ModelConfig):
        """

        :param config: dict with config
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def model_name(self) -> str:
        """
        :return: model name
        """
        raise NotImplemented()
