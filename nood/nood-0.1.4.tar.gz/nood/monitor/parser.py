from abc import ABC, abstractmethod
from typing import List, Union

import requests

from nood import objects


class Parser(ABC):
    @staticmethod
    def _to_list(parsing_response):
        if not isinstance(parsing_response, list):
            parsing_response = [parsing_response]
        return parsing_response

    @abstractmethod
    def parse(self, *, response: requests.Response) -> Union[
        objects.Product, List[objects.Product]]:
        pass
