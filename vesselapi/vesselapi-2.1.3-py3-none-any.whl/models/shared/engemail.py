import dataclasses
from typing import Any,Optional
from dataclasses_json import dataclass_json
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class EngEmailAssociations:
    action_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('actionId') }})
    contact_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contactId') }})
    owner_user_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('ownerUserId') }})
    task_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('taskId') }})
    

@dataclass_json
@dataclasses.dataclass
class EngEmail:
    r"""EngEmail
    A email between a User and an external Contact
    """
    
    associations: EngEmailAssociations = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('associations') }})
    created_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    modified_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('modifiedTime') }})
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('additional') }})
    bcc: Optional[list[str]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('bcc') }})
    body_html: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('bodyHtml') }})
    body_text: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('bodyText') }})
    cc: Optional[list[str]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('cc') }})
    is_bounced: Optional[bool] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('isBounced') }})
    subject: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('subject') }})
    to: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('to') }})
    
