import dataclasses
from typing import Optional
from enum import Enum
from dataclasses_json import dataclass_json
from vesselapi import utils

class EngIntegrationIntegrationIDEnum(str, Enum):
    OUTREACH = "outreach"
    SALESLOFT = "salesloft"


@dataclass_json
@dataclasses.dataclass
class EngIntegration:
    icon_url: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('iconURL') }})
    integration_id: Optional[EngIntegrationIntegrationIDEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('integrationId') }})
    name: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('name') }})
    
