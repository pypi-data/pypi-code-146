from enum import Enum
from typing import Optional

from pydantic import BaseModel

from telescope_sdk import SequenceStep
from telescope_sdk.common import UserFacingDataType


class ProspectSequenceStepEventType(Enum):
    EMAIL_SENT = 'EMAIL_SENT'


class ProspectSequenceStepEvent(BaseModel):
    id: str
    created_at: str
    sequence_step: SequenceStep
    type: ProspectSequenceStepEventType
    # According to "Managing Threads" from the GMail API (https://developers.google.com/gmail/api/guides/threads):
    # - The request threadId bust be specified on the Message (thread_id)
    # - The headers "In-Reply-To" and "References" must be set in compliance with RFC2922 (message_id)
    thread_id: Optional[str] = None
    message_id: Optional[str] = None


class Prospect(UserFacingDataType):
    campaign_id: str
    person_id: str
    first_name: str
    last_name: str
    company_name: str
    sequence_step_history: list[ProspectSequenceStepEvent]
    job_title: Optional[str] = None
    email: Optional[str] = None
    average_sentiment: Optional[float] = None
