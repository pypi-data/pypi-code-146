from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


T = TypeVar("T")
K = TypeVar("K")


#interface
class IRequestInterface(ABC,Generic[T,K]):
    @abstractmethod
    def execute(self):
        pass
