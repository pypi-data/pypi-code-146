import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engcontact as shared_engcontact


@dataclasses.dataclass
class GetAllEngagementContactsQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    cursor: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'cursor', 'style': 'form', 'explode': True }})
    limit: Optional[float] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'limit', 'style': 'form', 'explode': True }})
    

@dataclass_json
@dataclasses.dataclass
class GetAllEngagementContactsResponseBody:
    contacts: Optional[list[shared_engcontact.EngContact]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('contacts') }})
    next_page_cursor: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nextPageCursor') }})
    

@dataclasses.dataclass
class GetAllEngagementContactsRequest:
    query_params: GetAllEngagementContactsQueryParams = dataclasses.field()
    

@dataclasses.dataclass
class GetAllEngagementContactsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetAllEngagementContactsResponseBody] = dataclasses.field(default=None)
    
