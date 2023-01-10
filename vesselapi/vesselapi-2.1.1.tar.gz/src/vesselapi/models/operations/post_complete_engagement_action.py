import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import actioncomplete as shared_actioncomplete


@dataclass_json
@dataclasses.dataclass
class PostCompleteEngagementActionRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    fields: shared_actioncomplete.ActionComplete = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('fields') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclass_json
@dataclasses.dataclass
class PostCompleteEngagementActionResponseBody:
    id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PostCompleteEngagementActionRequest:
    request: Optional[PostCompleteEngagementActionRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class PostCompleteEngagementActionResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostCompleteEngagementActionResponseBody] = dataclasses.field(default=None)
    
