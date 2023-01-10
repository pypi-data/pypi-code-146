from enum import Enum
from typing import Protocol


class ComponentPriority(str, Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2


class BaseEnvironmentComponent(Protocol):
    PRIORITY = ComponentPriority.MEDIUM

    def setup(self):
        raise NotImplementedError()

    def destroy(self):
        raise NotImplementedError()
