from __future__ import annotations

import abc
from typing import final

from kfp import Client


@final
class KfpClient():

    __metaclass__ = abc.ABCMeta
    __client: Client

    def set_endpoint(self, endpoint: str, *args, **kwargs) -> KfpClient:
        self.__client = Client(
            host=endpoint,
            **kwargs,
        )
        return self

    @property
    def api_client(self) -> Client:
        return self.__client
