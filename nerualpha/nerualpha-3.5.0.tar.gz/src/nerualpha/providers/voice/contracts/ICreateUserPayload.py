from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class ICreateUserPayload(ABC):
    name:str
    display_name:str
    image_url:str
    channels:object
