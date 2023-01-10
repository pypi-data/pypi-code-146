import dataclasses
from typing import Optional
from enum import Enum
from dataclasses_json import dataclass_json
from vesselapi import utils

class EngTaskCompleteTypeEnum(str, Enum):
    CALL = "call"
    OTHER = "other"


@dataclass_json
@dataclasses.dataclass
class EngTaskComplete:
    r"""EngTaskComplete
    Complete a call or other task.
    """
    
    body: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('body') }})
    disposition_key: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('dispositionKey') }})
    duration_seconds: Optional[float] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('durationSeconds') }})
    phone: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('phone') }})
    type: Optional[EngTaskCompleteTypeEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('type') }})
    
