from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.services.config.urlObject import UrlObject


#interface
class ICommandService(ABC):
    @abstractmethod
    def executeCommand(self,url,method,data = None,headers = None):
        pass
