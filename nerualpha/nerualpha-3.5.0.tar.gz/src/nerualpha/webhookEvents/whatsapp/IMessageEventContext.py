from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IMessageEventContext(ABC):
    message_uuid:str
    message_from:str
