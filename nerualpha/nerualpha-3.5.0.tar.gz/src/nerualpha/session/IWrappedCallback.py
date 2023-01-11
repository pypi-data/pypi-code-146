from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IFilter import IFilter


#interface
class IWrappedCallback(ABC):
    id:str
    filters:List[IFilter]
    instanceServiceName:str
    sessionId:str
    instanceId:str
    path:str
