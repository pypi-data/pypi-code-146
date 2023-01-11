from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.scheduler.contracts.IIntervalParams import IIntervalParams
from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback

T = TypeVar("T")


#interface
class IStartAtPayload(IPayloadWithCallback,Generic[T]):
    startAt:str
    interval:IIntervalParams
    payload:T
    id:str
