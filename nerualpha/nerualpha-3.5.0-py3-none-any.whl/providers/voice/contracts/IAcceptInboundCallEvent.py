from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IAcceptInboundCallBody import IAcceptInboundCallBody


#interface
class IAcceptInboundCallEvent(ABC):
    type_:str
    application_id:str
    timestamp:str
    params:Dict[str,str]
    body:IAcceptInboundCallBody
    from_:str
