from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.webhookEvents.IBaseEvent import IBaseEvent
from nerualpha.webhookEvents.sms.ISMSMetadata import ISMSMetadata
from nerualpha.webhookEvents.sms.ISMSUsage import ISMSUsage


#interface
class ISMSEvent(IBaseEvent):
    channel:str
    usage:ISMSUsage
    sms:ISMSMetadata
