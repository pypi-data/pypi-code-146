from __future__ import annotations
from bidict import bidict
from abc import abstractmethod, ABC
from typing import Dict, List, Union


def create_types_class(types: Union[Dict[str, str], List[str]]) -> BaseTypes:
    if isinstance(types, dict):
        return DictTypes(types)

    return ListTypes(types)


class BaseTypes(ABC):
    def __init__(self, data: Union[Dict[str, str], List[str]]) -> None:
        self.data = data

    @abstractmethod
    def get(self, key: Union[str, int]) -> str:
        pass


class DictTypes(BaseTypes):
    def __init__(self, data: Dict[str, str]) -> None:
        self.data = bidict({int(k): v for k, v in data.items()})

    def get(self, key: int) -> str:
        return self.data.get(key)

    def get_inverse(self, key: str) -> str:
        return self.data.inverse.get(key)


class ListTypes(BaseTypes):
    def get(self, key: int) -> str:
        return self.data[key]
