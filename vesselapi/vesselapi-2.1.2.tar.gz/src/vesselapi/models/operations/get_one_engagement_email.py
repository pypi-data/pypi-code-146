import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engemail as shared_engemail


@dataclasses.dataclass
class GetOneEngagementEmailQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    id: str = dataclasses.field(metadata={'query_param': { 'field_name': 'id', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    

@dataclass_json
@dataclasses.dataclass
class GetOneEngagementEmailResponseBody:
    email: Optional[shared_engemail.EngEmail] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('email') }})
    

@dataclasses.dataclass
class GetOneEngagementEmailRequest:
    query_params: GetOneEngagementEmailQueryParams = dataclasses.field()
    

@dataclasses.dataclass
class GetOneEngagementEmailResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetOneEngagementEmailResponseBody] = dataclasses.field(default=None)
    
