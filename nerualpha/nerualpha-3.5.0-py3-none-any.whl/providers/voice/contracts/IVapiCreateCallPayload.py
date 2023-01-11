from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint


#interface
class IVapiCreateCallPayload(ABC):
    from_:IChannelPhoneEndpoint
    to:List[IChannelPhoneEndpoint]
    ncco:List[Dict[str,object]]
