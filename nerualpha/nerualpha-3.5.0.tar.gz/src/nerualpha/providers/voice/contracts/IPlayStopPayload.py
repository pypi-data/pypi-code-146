from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IPlayStopBody import IPlayStopBody


#interface
class IPlayStopPayload(ABC):
    type_:str
    body:IPlayStopBody
    to:str
