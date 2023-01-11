from abc import ABC
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class SemanthaModelEntity(ABC):
    data: Union[dict, list]
