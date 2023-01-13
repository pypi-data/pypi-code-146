import requests
import json

from requests.auth import HTTPBasicAuth

from spt_datascience.datascience.models.base_model import BaseModel, ModelConfig


class RestModel(BaseModel):

    def __init__(self, model_url, user, password):
        self.model_url = model_url
        self.__base_auth = HTTPBasicAuth(user, password)
        self.__header = {'Content-Type': 'application/json'}

    def save_model(self, model_id, version) -> ModelConfig:
        raise NotImplemented("Save mlflow model using mlflow API")

    @staticmethod
    def load_model(config: ModelConfig):
        return RestModel(
            model_url=config.bins['model_url'],
            user=config.bins['user'],
            password=config.bins['password']
        )

    def predict(self, data):
        json_data = {"inputs": data}
        response = requests.post(
            self.model_url,
            auth=self.__base_auth,
            headers=self.__header,
            json=json_data
        )
        return json.loads(response.content.decode('UTF-8'))

    def model_name(self) -> str:
        return 'mlflow_rest'
