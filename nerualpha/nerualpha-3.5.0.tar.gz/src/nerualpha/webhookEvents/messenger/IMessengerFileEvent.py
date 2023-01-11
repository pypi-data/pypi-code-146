from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.webhookEvents.IUrlPayload import IUrlPayload
from nerualpha.webhookEvents.messenger.IMessangerEvent import IMessengerEvent


#interface
class IMessengerFileEvent(IMessengerEvent):
    file:IUrlPayload
