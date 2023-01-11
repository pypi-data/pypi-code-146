import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engcontactcreate as shared_engcontactcreate


@dataclass_json
@dataclasses.dataclass
class PostEngagementContactRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    contact: shared_engcontactcreate.EngContactCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contact') }})
    

@dataclass_json
@dataclasses.dataclass
class PostEngagementContactResponseBody:
    id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PostEngagementContactRequest:
    request: Optional[PostEngagementContactRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class PostEngagementContactResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostEngagementContactResponseBody] = dataclasses.field(default=None)
    
