from enum import Enum
from typing import Optional

from telescope_sdk.common import UserFacingDataType


class CampaignLogEventType(Enum):
    CREATED_CAMPAIGN = 'CREATED_CAMPAIGN'
    STARTED_CAMPAIGN = 'STARTED_CAMPAIGN'
    PAUSED_CAMPAIGN = 'PAUSED_CAMPAIGN'
    EMAIL_SENT = 'EMAIL_SENT'
    EMAIL_SEND_FAILURE = 'EMAIL_SEND_FAILURE'
    FUNNEL_REPLENISH_ACTIVATED = 'FUNNEL_REPLENISH_ACTIVATED'
    FUNNEL_REPLENISH_DEACTIVATED = 'FUNNEL_REPLENISH_DEACTIVATED'
    REPLENISHED_FUNNEL = 'REPLENISHED_FUNNEL'
    ADDED_PROSPECTS = 'ADDED_PROSPECTS'
    REMOVED_PROSPECTS = 'REMOVED_PROSPECTS'
    EDITED_EMAIL_STEP = 'EDITED_EMAIL_STEP'
    DELETED_EMAIL_STEP = 'DELETED_EMAIL_STEP'
    ADDED_EMAIL_STEP = 'ADDED_EMAIL_STEP'
    ADDED_DELAY_AFTER = 'ADDED_DELAY_AFTER'
    EDITED_DELAY_AFTER = 'EDITED_DELAY_AFTER'
    ACCEPTED_RECOMMENDATION = 'ACCEPTED_RECOMMENDATION'
    REJECTED_RECOMMENDATION = 'REJECTED_RECOMMENDATION'
    SAVED_RECOMMENDATION = 'SAVED_RECOMMENDATION'


class CampaignLogEvent(UserFacingDataType):
    campaign_id: str
    type: CampaignLogEventType
    description: Optional[str] = None
    prospect_id: Optional[str] = None
    thread_id: Optional[str] = None
    sequence_step_id: Optional[str] = None
    recommendation_id: Optional[str] = None
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
