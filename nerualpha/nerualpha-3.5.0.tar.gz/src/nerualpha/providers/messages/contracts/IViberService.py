from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IViberService(ABC):
    category:str
    ttl:int
    type_:str
