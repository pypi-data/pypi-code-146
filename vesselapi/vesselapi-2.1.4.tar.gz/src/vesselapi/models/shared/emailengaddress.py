import dataclasses
from typing import Optional
from enum import Enum
from dataclasses_json import dataclass_json
from vesselapi import utils

class EmailEngAddressTypeEnum(str, Enum):
    WORK = "work"
    PERSONAL = "personal"


@dataclass_json
@dataclasses.dataclass
class EmailEngAddress:
    address: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('address') }})
    is_primary: Optional[bool] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('isPrimary') }})
    type: Optional[EmailEngAddressTypeEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('type') }})
    
