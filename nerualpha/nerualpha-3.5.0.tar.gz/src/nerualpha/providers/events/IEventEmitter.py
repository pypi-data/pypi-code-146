from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IEventEmitter(ABC):
    @abstractmethod
    def emitSessionCreatedEvent(self,ttl):
        pass
    @abstractmethod
    def emit(self,e):
        pass
