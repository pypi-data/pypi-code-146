from abc import ABC, abstractmethod
from typing import List

import requests

from nood import objects


class Parser(ABC):

    @abstractmethod
    def parse(self, *, response: requests.Response) -> List[objects.Product]:
        pass
