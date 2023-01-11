import dataclasses
from datetime import date, datetime
from marshmallow import fields
import dateutil.parser
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engaccountupdate as shared_engaccountupdate


@dataclass_json
@dataclasses.dataclass
class PutEngagementAccountApplicationJSON:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    account: shared_engaccountupdate.EngAccountUpdate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('account') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutEngagementAccountRequests:
    application_xml: bytes = dataclasses.field(metadata={'request': { 'media_type': 'application/xml' }})
    object: Optional[PutEngagementAccountApplicationJSON] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json
@dataclasses.dataclass
class PutEngagementAccountResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutEngagementAccountRequest:
    request: Optional[PutEngagementAccountRequests] = dataclasses.field(default=None)
    

@dataclasses.dataclass
class PutEngagementAccountResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PutEngagementAccountResponseBody] = dataclasses.field(default=None)
    
