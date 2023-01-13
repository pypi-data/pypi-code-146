from spt_datascience.datascience.models.base_model import BaseModel, ModelConfig


class EstimatorModel(BaseModel):

    def __init__(self, estimator):
        self.estimator = estimator

    def save_model(self, model_id, version) -> ModelConfig:
        raise NotImplemented("Save mlflow model using mlflow API")

    @staticmethod
    def load_model(config: ModelConfig):
        return EstimatorModel(
            estimator=config.bins['estimator']
        )

    def model_name(self) -> str:
        return 'mlflow_sklearn'