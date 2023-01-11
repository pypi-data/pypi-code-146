from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.numbers.contracts.IBaseNumberOptions import IBaseNumberOptions


#interface
class IGetNumbersOptions(IBaseNumberOptions):
    application_id:str
    has_application:bool
    country:str
    pattern:str
    search_pattern:str
    size:str
    index:str
