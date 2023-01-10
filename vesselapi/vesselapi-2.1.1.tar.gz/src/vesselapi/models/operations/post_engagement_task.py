import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engtaskcreate as shared_engtaskcreate


@dataclass_json
@dataclasses.dataclass
class PostEngagementTaskRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    task: shared_engtaskcreate.EngTaskCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('task') }})
    

@dataclass_json
@dataclasses.dataclass
class PostEngagementTaskResponseBody:
    id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PostEngagementTaskRequest:
    request: Optional[PostEngagementTaskRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class PostEngagementTaskResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostEngagementTaskResponseBody] = dataclasses.field(default=None)
    
