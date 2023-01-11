from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.messages.contracts.IMessageContact import IMessageContact
from nerualpha.providers.messages.contracts.ISendTextMessagePayload import ISendTextMessagePayload


#interface
class ISendTextPayload(ABC):
    from_:IMessageContact
    to:IMessageContact
    message:ISendTextMessagePayload
