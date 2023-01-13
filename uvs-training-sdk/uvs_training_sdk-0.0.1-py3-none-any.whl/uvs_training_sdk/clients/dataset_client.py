import requests
from .client import Client
from ..models import Dataset, DatasetResponse


class DatasetClient(Client):
    def __init__(self, resource_type, resource_name: str, multi_service_endpoint, resource_key: str) -> None:
        super().__init__(resource_type, resource_name, multi_service_endpoint, resource_key)
        self._endpoint = f'{self._endpoint}/datasets/'

    def register_dataset(self, dataset: Dataset) -> Dataset:
        r = self._request_wrapper(lambda: requests.put(self._endpoint + dataset.name, json=dataset.params, timeout=self.TIMEOUT_SEC, headers=self.headers))
        return DatasetResponse.from_response(r.json())

    def query_dataset(self, dataset: Dataset) -> Dataset:
        r = self._request_wrapper(lambda: requests.get(self._endpoint + dataset.name, timeout=self.TIMEOUT_SEC, headers=self.headers).json())
        return DatasetResponse.from_response(r.json())
