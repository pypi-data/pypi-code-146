from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IJwtPayload(ABC):
    api_application_id:str
    api_account_id:str
    aud:str
    iss:str
    sub:str
    iat:int
    exp:int
