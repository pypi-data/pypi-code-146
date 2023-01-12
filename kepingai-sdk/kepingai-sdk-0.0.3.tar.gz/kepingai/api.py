import requests
import json
from requests import Response
from kepingai.exceptions import KepingApiException


class KepingApi:
    def __init__(self,
                 api_key: str,
                 user_id: str,
                 host="apis.kepingai.com",
                 api_version="v0"):
        self._api_url = f"http://{host}/{api_version}"
        self._api_key = api_key
        self._user_id = user_id

    def get(self, params: dict, tag: str):
        params.update({"api_key": self._api_key,
                       "user_id": self._user_id})
        url = f"{self._api_url}/{tag}"
        response = requests.get(url=url, params=params)
        return self._handle_response(response)

    def post(self, data: dict, tag: str):
        url = f"{self._api_url}/{tag}"
        data.update({"api_key": self._api_key,
                     "user_id": self._user_id})
        response = requests.post(url=url, data=json.dumps(data))
        return self._handle_response(response)

    def _handle_response(self, response: Response):
        if response.status_code == 200:
            return response.content.decode()
        else:
            raise KepingApiException(response.content.decode())
