from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="NewCampaignUserSession")


@attr.s(auto_attribs=True)
class NewCampaignUserSession:
    """
    Attributes:
        session_id (str):
        session_mode_id (str):
        username (str):
    """

    session_id: str
    session_mode_id: str
    username: str

    def to_dict(self) -> Dict[str, Any]:
        session_id = self.session_id
        session_mode_id = self.session_mode_id
        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sessionId": session_id,
                "sessionModeId": session_mode_id,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        session_id = d.pop("sessionId")

        session_mode_id = d.pop("sessionModeId")

        username = d.pop("username")

        new_campaign_user_session = cls(
            session_id=session_id,
            session_mode_id=session_mode_id,
            username=username,
        )

        return new_campaign_user_session
