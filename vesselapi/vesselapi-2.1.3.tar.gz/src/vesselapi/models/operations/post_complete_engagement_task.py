import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engtaskcomplete as shared_engtaskcomplete


@dataclass_json
@dataclasses.dataclass
class PostCompleteEngagementTaskRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    fields: shared_engtaskcomplete.EngTaskComplete = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('fields') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclass_json
@dataclasses.dataclass
class PostCompleteEngagementTaskResponseBody:
    id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PostCompleteEngagementTaskRequest:
    request: Optional[PostCompleteEngagementTaskRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class PostCompleteEngagementTaskResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostCompleteEngagementTaskResponseBody] = dataclasses.field(default=None)
    
