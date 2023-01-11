from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IUser(ABC):
    id:str
    name:str
    display_name:str
    image_url:str
    custom_data:object
