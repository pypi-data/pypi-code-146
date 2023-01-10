from typing import Any, Dict, Type, TypeVar

import attr

from ..models.campaign_user_session_state import CampaignUserSessionState

T = TypeVar("T", bound="CampaignUserSession")


@attr.s(auto_attribs=True)
class CampaignUserSession:
    """
    Attributes:
        id (str):
        session_id (str):
        session_mode_id (str):
        state (CampaignUserSessionState):
        username (str):
    """

    id: str
    session_id: str
    session_mode_id: str
    state: CampaignUserSessionState
    username: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        session_id = self.session_id
        session_mode_id = self.session_mode_id
        state = self.state.value

        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "sessionId": session_id,
                "sessionModeId": session_mode_id,
                "state": state,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        session_id = d.pop("sessionId")

        session_mode_id = d.pop("sessionModeId")

        state = CampaignUserSessionState(d.pop("state"))

        username = d.pop("username")

        campaign_user_session = cls(
            id=id,
            session_id=session_id,
            session_mode_id=session_mode_id,
            state=state,
            username=username,
        )

        return campaign_user_session
