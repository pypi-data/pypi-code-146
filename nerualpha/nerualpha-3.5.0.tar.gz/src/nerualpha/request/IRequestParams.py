from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.services.config.urlObject import UrlObject

T = TypeVar("T")


#interface
class IRequestParams(ABC,Generic[T]):
    method:str
    url:UrlObject
    data:T
    headers:Dict[str,str]
