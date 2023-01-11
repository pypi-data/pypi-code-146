import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engaccountcreate as shared_engaccountcreate


@dataclass_json
@dataclasses.dataclass
class PostEngagementAccountRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    account: shared_engaccountcreate.EngAccountCreate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('account') }})
    

@dataclass_json
@dataclasses.dataclass
class PostEngagementAccountResponseBody:
    id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PostEngagementAccountRequest:
    request: Optional[PostEngagementAccountRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class PostEngagementAccountResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostEngagementAccountResponseBody] = dataclasses.field(default=None)
    
