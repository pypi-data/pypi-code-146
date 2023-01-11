from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.numbers.contracts.IBaseNumberOptions import IBaseNumberOptions


#interface
class IUpdateNumberOptions(IBaseNumberOptions):
    country:str
    msisdn:str
    app_id:str
    moHttpUrl:str
    moSmppSysType:str
    voiceCallbackType:str
    voiceCallbackValue:str
    voiceStatusCallback:str
