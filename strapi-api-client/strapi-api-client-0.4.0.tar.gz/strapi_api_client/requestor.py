import json
import urllib
from typing import Dict, Union
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
from urllib.parse import urlencode

from strapi_api_client import version
from strapi_api_client.errors import ApiException
from strapi_api_client.utils import JSONEncoder


class Requestor:
    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        self._user_agent = f"strapi_api_client/{version.__version__}"
        self._api_url = api_url
        self._api_key = api_key
        self._timeout = timeout

    def request(
            self, method: str, endpoint_url: str, payload: dict = None, query: dict = None, parse: bool = True
    ) -> Union[str, Dict]:
        if query and isinstance(query, dict):
            params = urlencode(query)
            endpoint_url += f'?{params}'

        request = Request(
            method=method,
            url=endpoint_url,
            headers={
                "User-Agent": self._user_agent,
                "Authorization": self._api_key
            }
        )

        if payload and isinstance(payload, dict):
            request.data = json.dumps(payload, cls=JSONEncoder).encode('utf-8')
            request.headers['Content-Type'] = 'application/json'

        try:
            response = urlopen(request, timeout=self._timeout)
        except HTTPError as error:
            raise ApiException(request, f'{error.status} - {error.reason}')
        except URLError as error:
            raise ApiException(request, error.reason)
        else:
            if parse:
                try:
                    data = json.loads(response.read())
                except json.JSONDecodeError:
                    raise ApiException(request, 'Cannot parse the response data to json format.')
            else:
                data = response.read()

            return data

    def __str__(self) -> str:
        return self._user_agent
