import dataclasses
from datetime import date, datetime
from marshmallow import fields
import dateutil.parser
from typing import Any,Optional
from enum import Enum
from dataclasses_json import dataclass_json
from vesselapi import utils

class EngTaskCreateTypeEnum(str, Enum):
    CALL = "call"
    EMAIL = "email"
    OTHER = "other"


@dataclass_json
@dataclasses.dataclass
class EngTaskCreate:
    r"""EngTaskCreate
    Properties that a task can be created with
    """
    
    contact_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contactId') }})
    due_date: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('dueDate') }})
    owner_user_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('ownerUserId') }})
    type: EngTaskCreateTypeEnum = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('type') }})
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('additional') }})
    body: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('body') }})
    
