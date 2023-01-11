from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.webhookEvents.IBaseEvent import IBaseEvent
from nerualpha.webhookEvents.whatsapp.IProfileName import IProfileName
from nerualpha.webhookEvents.whatsapp.IMessageEventContext import IMessageEventContext


#interface
class IWhatsappEvent(IBaseEvent):
    profile:IProfileName
    context:IMessageEventContext
    provider_message:str
    message_type:str
