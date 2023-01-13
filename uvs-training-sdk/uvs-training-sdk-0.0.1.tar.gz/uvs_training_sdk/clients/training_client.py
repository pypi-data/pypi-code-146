import requests
from .client import Client
from ..models import Model, ModelResponse


class TrainingClient(Client):
    def __init__(self, resource_type, resource_name: str, multi_service_endpoint, resource_key: str) -> None:
        super().__init__(resource_type, resource_name, multi_service_endpoint, resource_key)
        self._endpoint = f'{self._endpoint}/models/'

    def train_model(self, model: Model):
        r = self._request_wrapper(lambda: requests.put(self._endpoint + model.name, json=model.params, timeout=self.TIMEOUT_SEC, headers=self.headers))
        return ModelResponse.from_response(r.json())

    def query_model(self, name):
        r = self._request_wrapper(lambda: requests.get(self._endpoint + name, timeout=self.TIMEOUT_SEC, headers=self.headers))
        return ModelResponse.from_response(r.json())

    def cancel_model_training(self, name):
        self._request_wrapper(lambda: requests.post(self._endpoint + name + "/:cancel", timeout=self.TIMEOUT_SEC, headers=self.headers))

    def delete_model(self, name):
        self._request_wrapper(lambda: requests.delete(self._endpoint + name, timeout=self.TIMEOUT_SEC, headers=self.headers))
