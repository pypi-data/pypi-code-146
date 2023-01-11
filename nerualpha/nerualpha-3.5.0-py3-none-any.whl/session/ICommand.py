from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IActionPayload import IActionPayload

T = TypeVar("T")


#interface
class ICommand(ABC,Generic[T]):
    header:Dict[str,str]
    actions:List[IActionPayload[T]]
