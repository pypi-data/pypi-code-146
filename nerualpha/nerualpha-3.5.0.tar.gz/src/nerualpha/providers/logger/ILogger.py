from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.logger.ILogContext import ILogContext


#interface
class ILogger(ABC):
    @abstractmethod
    def log(self,level,message,context = None):
        pass
