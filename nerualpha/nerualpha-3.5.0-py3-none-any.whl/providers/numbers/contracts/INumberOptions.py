from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.numbers.contracts.IBaseNumberOptions import IBaseNumberOptions


#interface
class INumberOptions(IBaseNumberOptions):
    country:str
    msisdn:str
    target_api_key:str
