from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.ISayTextBody import ISayTextBody


#interface
class ISayTextPayload(ABC):
    type_:str
    body:ISayTextBody
