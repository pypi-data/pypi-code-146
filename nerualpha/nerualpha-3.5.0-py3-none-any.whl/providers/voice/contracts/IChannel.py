from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IChannelEndpoint import IChannelEndpoint


#interface
class IChannel(ABC):
    id:str
    type_:str
    to:IChannelEndpoint
    from_:IChannelEndpoint
    headers:Dict[str,str]
    cpa:bool
    preanswer:bool
    ring_timeout:int
    can_hear:List[str]
    can_speak:List[str]
    cpa_time:int
    max_length:int
    knocking_id:str
    content_hyphen_type:str
