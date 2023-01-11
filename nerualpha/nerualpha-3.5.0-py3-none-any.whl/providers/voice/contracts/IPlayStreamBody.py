from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IPlayStreamBody(ABC):
    level:int
    loop:int
    streamUrl:List[str]
    queue:bool
