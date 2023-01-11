import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engaccount as shared_engaccount


@dataclasses.dataclass
class GetOneEngagementAccountQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    id: str = dataclasses.field(metadata={'query_param': { 'field_name': 'id', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    

@dataclass_json
@dataclasses.dataclass
class GetOneEngagementAccountResponseBody:
    account: Optional[shared_engaccount.EngAccount] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('account') }})
    

@dataclasses.dataclass
class GetOneEngagementAccountRequest:
    query_params: GetOneEngagementAccountQueryParams = dataclasses.field()
    

@dataclasses.dataclass
class GetOneEngagementAccountResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetOneEngagementAccountResponseBody] = dataclasses.field(default=None)
    
