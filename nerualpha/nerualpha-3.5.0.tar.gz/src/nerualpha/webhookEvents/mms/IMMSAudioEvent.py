from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.webhookEvents.IUrlPayload import IUrlPayload
from nerualpha.webhookEvents.mms.IMMSEvent import IMMSEvent


#interface
class IMMSAudioEvent(IMMSEvent):
    audio:IUrlPayload
