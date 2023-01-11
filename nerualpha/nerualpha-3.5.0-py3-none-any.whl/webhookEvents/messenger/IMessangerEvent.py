from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.webhookEvents.IBaseEvent import IBaseEvent


#interface
class IMessengerEvent(IBaseEvent):
    message_type:str
