from abc import ABC, abstractmethod

import requests

from nood import objects


class Parser(ABC):

    @abstractmethod
    def parse(self, *, response: requests.Response) -> list[objects.Product]:
        pass
