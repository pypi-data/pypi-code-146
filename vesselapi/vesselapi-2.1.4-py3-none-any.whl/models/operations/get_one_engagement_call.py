import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import call as shared_call


@dataclasses.dataclass
class GetOneEngagementCallQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    id: str = dataclasses.field(metadata={'query_param': { 'field_name': 'id', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    

@dataclass_json
@dataclasses.dataclass
class GetOneEngagementCallResponseBody:
    call: Optional[shared_call.Call] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('call') }})
    

@dataclasses.dataclass
class GetOneEngagementCallRequest:
    query_params: GetOneEngagementCallQueryParams = dataclasses.field()
    

@dataclasses.dataclass
class GetOneEngagementCallResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetOneEngagementCallResponseBody] = dataclasses.field(default=None)
    
