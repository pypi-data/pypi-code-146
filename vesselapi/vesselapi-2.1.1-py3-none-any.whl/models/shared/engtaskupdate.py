import dataclasses
from datetime import date, datetime
from marshmallow import fields
import dateutil.parser
from typing import Any,Optional
from dataclasses_json import dataclass_json
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class EngTaskUpdate:
    r"""EngTaskUpdate
    Properties that a task can be updated with
    """
    
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('additional') }})
    body: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('body') }})
    due_date: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('dueDate') }})
    
