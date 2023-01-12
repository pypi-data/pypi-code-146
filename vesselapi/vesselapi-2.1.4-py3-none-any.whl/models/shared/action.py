import dataclasses
from datetime import date, datetime
from marshmallow import fields
import dateutil.parser
from typing import Any,Optional
from enum import Enum
from dataclasses_json import dataclass_json
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class ActionAssociations:
    call_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('callId') }})
    contact_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contactId') }})
    email_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('emailId') }})
    owner_user_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('ownerUserId') }})
    
class ActionStatusEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    TO_DO = "to_do"

class ActionTypeEnum(str, Enum):
    CALL = "call"
    EMAIL = "email"
    OTHER = "other"


@dataclass_json
@dataclasses.dataclass
class Action:
    r"""Action
    An action represents some work that needs to be done in order to progress a sequence to the next step.
    """
    
    associations: ActionAssociations = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('associations') }})
    created_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    modified_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('modifiedTime') }})
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('additional') }})
    due_date: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('dueDate') }})
    status: Optional[ActionStatusEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('status') }})
    type: Optional[ActionTypeEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('type') }})
    
