import json
from json import JSONDecodeError

from servicefusion import ServicefusionToken


class BaseStorage:
    app: str = None

    def __init__(self):
        pass

    def get_token(self, app) -> ServicefusionToken:
        raise NotImplementedError()

    def save_token(self, app: str, token: ServicefusionToken) -> bool:
        raise NotImplementedError()
