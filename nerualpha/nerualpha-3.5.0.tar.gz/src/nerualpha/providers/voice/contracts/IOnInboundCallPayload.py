from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback
from nerualpha.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint


#interface
class IOnInboundCallPayload(IPayloadWithCallback):
    to:IChannelPhoneEndpoint
    from_:IChannelPhoneEndpoint
