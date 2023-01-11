from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IWrappedCallback import IWrappedCallback

T = TypeVar("T")


#interface
class IActionPayload(ABC,Generic[T]):
    provider:str
    action:str
    payload:T
    successCallback:IWrappedCallback
    errorCallback:IWrappedCallback
    description:str
