from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.scheduler.contracts.IIntervalParams import IIntervalParams

T = TypeVar("T")


#interface
class IStartAtParams(ABC,Generic[T]):
    startAt:str
    callback:str
    id:str
    interval:IIntervalParams
    payload:T
