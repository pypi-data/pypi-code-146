from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IBaseMessage(ABC):
    message_type:str
    to:str
    from_:str
    channel:str
