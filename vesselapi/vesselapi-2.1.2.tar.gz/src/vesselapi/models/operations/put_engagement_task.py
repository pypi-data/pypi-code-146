import dataclasses
from datetime import date, datetime
from marshmallow import fields
import dateutil.parser
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engtaskupdate as shared_engtaskupdate


@dataclass_json
@dataclasses.dataclass
class PutEngagementTaskApplicationJSON:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    task: shared_engtaskupdate.EngTaskUpdate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('task') }})
    

@dataclasses.dataclass
class PutEngagementTaskRequests:
    application_xml: bytes = dataclasses.field(metadata={'request': { 'media_type': 'application/xml' }})
    object: Optional[PutEngagementTaskApplicationJSON] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json
@dataclasses.dataclass
class PutEngagementTaskResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutEngagementTaskRequest:
    request: Optional[PutEngagementTaskRequests] = dataclasses.field(default=None)
    

@dataclasses.dataclass
class PutEngagementTaskResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PutEngagementTaskResponseBody] = dataclasses.field(default=None)
    
