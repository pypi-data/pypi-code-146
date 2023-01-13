from abc import ABC, abstractmethod


class PipelineConfig:

    def __init__(self, pipeline_name, pipeline_id, config, pipeline_package, pipeline_class, target_problem):
        self.pipeline_name = pipeline_name
        self.pipeline_id = pipeline_id
        self.config = config
        self.pipeline_package = pipeline_package
        self.pipeline_class = pipeline_class
        self.target_problem = target_problem

    def to_dict(self):
        return {
            'pipeline_name': self.pipeline_name,
            'pipeline_id': self.pipeline_id,
            'config': self.config,
            'pipeline_package': self.pipeline_package,
            'pipeline_class': self.pipeline_class,
            'target_problem': self.target_problem
        }

    @staticmethod
    def from_dict(config_dict: dict):
        return PipelineConfig(
            pipeline_name=config_dict['pipeline_name'],
            pipeline_id=config_dict['pipeline_id'],
            config=config_dict['config'],
            pipeline_package=config_dict['pipeline_package'],
            pipeline_class=config_dict['pipeline_class'],
            target_problem=config_dict['target_problem']
        )

    def __str__(self):
        return self.to_dict()

    def _repr_html_(self):
        return """
        <p><h3>%s</h3></p>
        <div><b>id</b>: %s</div>
        <div><b>target_problem</b>: %s</div>
        <div><b>package</b>: %s</div>
        <div><b>class</b>: %s</div>
        <div><b>config</b>: %s</div>
        """ % (self.pipeline_name, self.pipeline_id, self.target_problem,
               self.pipeline_package, self.pipeline_class, self.config)


class BasePipeline(ABC):

    @abstractmethod
    def save_pipeline(self, pipeline_id) -> PipelineConfig:
        """
        trigger inside models to saving
        :return: config dict
        """
        pass

    @staticmethod
    @abstractmethod
    def load_pipeline(config, model_manager):
        """
        :param pipeline_id:
        :return:
        """
        pass

    @abstractmethod
    def pipeline_name(self) -> str:
        """
        :return: pipelines name
        """
        pass

    @abstractmethod
    def predict(self, features):
        pass

    @abstractmethod
    def predict_proba(self, features):
        pass

    @abstractmethod
    def pipeline_score(self):
        pass