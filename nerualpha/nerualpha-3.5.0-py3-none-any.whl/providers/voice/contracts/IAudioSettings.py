from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IAudioSettings(ABC):
    enabled:bool
    earmuffed:bool
    muted:bool
