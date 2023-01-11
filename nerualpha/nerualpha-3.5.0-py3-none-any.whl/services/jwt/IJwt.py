from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IJWT(ABC):
    @abstractmethod
    def getToken(self):
        pass
    @abstractmethod
    def isExpired(self):
        pass
    @abstractmethod
    def mintToken(self,exp):
        pass
