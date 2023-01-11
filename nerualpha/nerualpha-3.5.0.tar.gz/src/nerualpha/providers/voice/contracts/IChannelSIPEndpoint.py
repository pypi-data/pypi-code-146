from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IChannelEndpoint import IChannelEndpoint


#interface
class IChannelSIPEndpoint(IChannelEndpoint):
    uri:str
    headers:Dict[str,str]
    username:str
    password:str
