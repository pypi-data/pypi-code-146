import dataclasses
from typing import Any,Optional
from enum import Enum
from dataclasses_json import dataclass_json
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class CallAssociations:
    action_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('actionId') }})
    contact_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contactId') }})
    owner_user_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('ownerUserId') }})
    task_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('taskId') }})
    
class CallDirectionEnum(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


@dataclass_json
@dataclasses.dataclass
class Call:
    r"""Call
    A phone call between a User and an external Contact
    """
    
    associations: CallAssociations = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('associations') }})
    created_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    modified_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('modifiedTime') }})
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('additional') }})
    direction: Optional[CallDirectionEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('direction') }})
    disposition: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('disposition') }})
    duration_seconds: Optional[float] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('durationSeconds') }})
    note: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('note') }})
    phone: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('phone') }})
    
