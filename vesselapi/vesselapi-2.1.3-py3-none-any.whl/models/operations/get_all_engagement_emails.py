import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engemail as shared_engemail


@dataclasses.dataclass
class GetAllEngagementEmailsQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': { 'field_name': 'accessToken', 'style': 'form', 'explode': True }})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'allFields', 'style': 'form', 'explode': True }})
    cursor: Optional[str] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'cursor', 'style': 'form', 'explode': True }})
    limit: Optional[float] = dataclasses.field(default=None, metadata={'query_param': { 'field_name': 'limit', 'style': 'form', 'explode': True }})
    

@dataclass_json
@dataclasses.dataclass
class GetAllEngagementEmailsResponseBody:
    emails: Optional[list[shared_engemail.EngEmail]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('emails') }})
    next_page_cursor: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nextPageCursor') }})
    

@dataclasses.dataclass
class GetAllEngagementEmailsRequest:
    query_params: GetAllEngagementEmailsQueryParams = dataclasses.field()
    

@dataclasses.dataclass
class GetAllEngagementEmailsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetAllEngagementEmailsResponseBody] = dataclasses.field(default=None)
    
