from enum import Enum

from telescope_sdk.common import UserFacingDataType


class CampaignStatus(Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'ERROR'


class Campaign(UserFacingDataType):
    name: str
    status: CampaignStatus
    sequence_id: str
    replenish: bool
