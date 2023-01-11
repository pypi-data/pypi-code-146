from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IWrappedCallback import IWrappedCallback


#interface
class IPayloadWithCallback(ABC):
    callback:IWrappedCallback
