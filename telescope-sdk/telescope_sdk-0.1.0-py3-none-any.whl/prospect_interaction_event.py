from enum import Enum
from typing import Optional

from telescope_sdk.common import UserFacingDataType


class ProspectInteractionEventType(Enum):
    PROSPECT_REPLIED_POSITIVE = 'PROSPECT_REPLIED_POSITIVE'
    PROSPECT_REPLIED_NEGATIVE = 'PROSPECT_REPLIED_NEGATIVE'
    PROSPECT_REPLIED_UNKNOWN_SENTIMENT = 'PROSPECT_REPLIED_UNKNOWN_SENTIMENT'


class ProspectInteractionEvent(UserFacingDataType):
    campaign_id: str
    prospect_id: str
    type: ProspectInteractionEventType
    text_reply: Optional[str] = None
