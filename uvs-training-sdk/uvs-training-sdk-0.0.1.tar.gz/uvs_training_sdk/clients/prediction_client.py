import copy
import requests
from .client import Client


class PredictionClient(Client):
    def __init__(self, resource_type, resource_name: str, multi_service_endpoint, resource_key: str) -> None:
        super().__init__(resource_type, resource_name, multi_service_endpoint, resource_key)
        self._endpoint = f'{self._endpoint}/operations/imageanalysis:analyze'
        self._headers['Content-Type'] = 'image/jpeg'
        self._params = {
            'visualFeatures': 'customModel',
            'customModel-modelName': '',
        }

    def predict(self, model_name: str, img: bytes):
        params = copy.deepcopy(self._params)
        params['customModel-modelName'] = model_name
        r = self._request_wrapper(lambda: requests.post(self._endpoint, data=img, timeout=self.TIMEOUT_SEC, headers=self.headers, params=params))
        return r
