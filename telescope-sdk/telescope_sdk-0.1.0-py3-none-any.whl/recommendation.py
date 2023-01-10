from enum import Enum
from typing import Optional

from telescope_sdk.common import UserFacingDataType


class RecommendationStatus(Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    SAVED = 'SAVED'
    PENDING = 'PENDING'


class RecommendationRejectionReason(Enum):
    NOT_RELEVANT = 'NOT_RELEVANT'
    WRONG_POSITION_RIGHT_COMPANY = 'WRONG_POSITION_RIGHT_COMPANY'
    RIGHT_POSITION_WRONG_COMPANY = 'RIGHT_POSITION_WRONG_COMPANY'
    EXISTING_CUSTOMER = 'EXISTING_CUSTOMER'
    ALREADY_CONTACTED = 'ALREADY_CONTACTED'
    OTHER = 'OTHER'


class Recommendation(UserFacingDataType):
    campaign_id: str
    person_id: str
    status: RecommendationStatus
    relevance: float
    rejection_reason: Optional[RecommendationRejectionReason] = None
    free_text_rejection_reason: Optional[str] = None
