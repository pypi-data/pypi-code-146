import dataclasses
from datetime import date, datetime
from marshmallow import fields
import dateutil.parser
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engcontactupdate as shared_engcontactupdate


@dataclass_json
@dataclasses.dataclass
class PutEngagementContactApplicationJSON:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    contact: shared_engcontactupdate.EngContactUpdate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contact') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutEngagementContactRequests:
    application_xml: bytes = dataclasses.field(metadata={'request': { 'media_type': 'application/xml' }})
    object: Optional[PutEngagementContactApplicationJSON] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json
@dataclasses.dataclass
class PutEngagementContactResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutEngagementContactRequest:
    request: Optional[PutEngagementContactRequests] = dataclasses.field(default=None)
    

@dataclasses.dataclass
class PutEngagementContactResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PutEngagementContactResponseBody] = dataclasses.field(default=None)
    
