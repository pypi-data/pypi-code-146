from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload


#interface
class IVonageAPI(ABC):
    @abstractmethod
    def invoke(self,url,method,body):
        pass
