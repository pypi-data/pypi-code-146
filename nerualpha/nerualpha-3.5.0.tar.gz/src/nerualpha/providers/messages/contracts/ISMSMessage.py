from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.messages.contracts.IBaseMessage import IBaseMessage


#interface
class ISMSMessage(IBaseMessage):
    text:str
