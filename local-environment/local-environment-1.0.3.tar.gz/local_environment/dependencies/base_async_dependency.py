from enum import Enum
from typing import Protocol


class ComponentPriority(str, Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2


class BaseAsyncEnvironmentComponent(Protocol):
    PRIORITY = ComponentPriority.MEDIUM

    async def setup(self):
        raise NotImplementedError()

    async def destroy(self):
        raise NotImplementedError()
