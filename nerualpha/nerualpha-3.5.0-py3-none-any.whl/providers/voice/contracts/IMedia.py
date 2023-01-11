from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IAudioSettings import IAudioSettings


#interface
class IMedia(ABC):
    audio_settings:IAudioSettings
    audio:bool
