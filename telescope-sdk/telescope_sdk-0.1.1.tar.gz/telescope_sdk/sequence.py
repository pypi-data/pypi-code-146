from enum import Enum
from typing import Optional

from pydantic import BaseModel

from telescope_sdk.common import UserFacingDataType


class SequenceStepType(Enum):
    EMAIL = 'EMAIL'


class SequenceStep(BaseModel):
    id: str
    type: SequenceStepType
    seconds_from_previous_step: int
    subject: str
    body: str
    signature: Optional[str] = None


class Sequence(UserFacingDataType):
    steps: list[SequenceStep]
