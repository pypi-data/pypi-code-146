import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engcontact as shared_engcontact


@dataclasses.dataclass
class GetOneEngagementContactQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    id: str = dataclasses.field(metadata={'query_param': { 'field_name': 'id', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    

@dataclass_json
@dataclasses.dataclass
class GetOneEngagementContactResponseBody:
    contact: Optional[shared_engcontact.EngContact] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('contact') }})
    

@dataclasses.dataclass
class GetOneEngagementContactRequest:
    query_params: GetOneEngagementContactQueryParams = dataclasses.field()
    

@dataclasses.dataclass
class GetOneEngagementContactResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetOneEngagementContactResponseBody] = dataclasses.field(default=None)
    
