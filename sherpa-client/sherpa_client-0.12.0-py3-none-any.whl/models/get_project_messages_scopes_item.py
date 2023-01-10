from enum import Enum


class GetProjectMessagesScopesItem(str, Enum):
    OPEN_CAMPAIGN = "open_campaign"
    OPEN_SESSION = "open_session"
    STOP_CAMPAIGN = "stop_campaign"

    def __str__(self) -> str:
        return str(self.value)
