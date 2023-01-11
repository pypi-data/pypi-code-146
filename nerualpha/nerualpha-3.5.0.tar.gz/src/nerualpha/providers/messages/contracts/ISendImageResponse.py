from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.messages.contracts.ISendResponse import ISendResponse


#interface
class ISendImageResponse(ISendResponse):
    pass
