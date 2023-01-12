import json
from json import JSONDecodeError
from pathlib import Path

from servicefusion.ServicefusionToken import ServicefusionToken
from servicefusion.storages import BaseStorage


class InMemoryStorage(BaseStorage):
    tokens: dict = {}

    def __init__(self):
        super().__init__()

    def get_token(self, app) -> ServicefusionToken:
        try:
            if app in self.tokens:
                return self.tokens[app]
        except Exception as e:
            pass
        return ServicefusionToken()

    def save_token(self, app: str, token: ServicefusionToken) -> bool:
        try:
            self.tokens[app] = token
            return True
        except Exception as e:
            pass
        return False
