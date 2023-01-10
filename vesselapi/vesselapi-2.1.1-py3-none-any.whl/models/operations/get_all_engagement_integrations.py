import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import engintegration as shared_engintegration


@dataclass_json
@dataclasses.dataclass
class GetAllEngagementIntegrationsResponseBody:
    integrations: Optional[list[shared_engintegration.EngIntegration]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('integrations') }})
    

@dataclasses.dataclass
class GetAllEngagementIntegrationsResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetAllEngagementIntegrationsResponseBody] = dataclasses.field(default=None)
    
