from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IUser import IUser
from nerualpha.providers.voice.contracts.IChannel import IChannel
from nerualpha.providers.voice.contracts.IMedia import IMedia


#interface
class IAcceptInboundCallPayload(ABC):
    user:IUser
    knocking_id:str
    channel:IChannel
    state:str
    media:IMedia
