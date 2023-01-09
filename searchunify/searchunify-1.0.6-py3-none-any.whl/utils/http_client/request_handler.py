import requests
from requests.exceptions import HTTPError
import json


class RequestManager:
    def http_request(method, url, **args):
        try:
            result = requests.request(method, url, **args)
            response = json.loads(result.text)
            return response
        except HTTPError as httpError:
            raise Exception(httpError)
        except Exception as error:
            raise Exception(error)
