from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IUser import IUser
from nerualpha.providers.voice.contracts.IChannel import IChannel


#interface
class IAcceptInboundCallBody(ABC):
    user:IUser
    channel:IChannel
