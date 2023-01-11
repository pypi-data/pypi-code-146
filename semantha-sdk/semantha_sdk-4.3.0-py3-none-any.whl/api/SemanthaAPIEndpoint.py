from abc import ABC, abstractmethod

from semantha_sdk.rest import RestClient


class SemanthaAPIEndpoint(ABC):
    def __init__(self, session: RestClient, parent_endpoint: str):
        self._session = session
        self._parent_endpoint = parent_endpoint

    @property
    @abstractmethod
    def _endpoint(self):
        pass
