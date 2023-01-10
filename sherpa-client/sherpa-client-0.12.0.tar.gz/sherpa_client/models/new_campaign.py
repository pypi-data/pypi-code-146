from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.campaign_user_group import CampaignUserGroup
    from ..models.email_notifications import EmailNotifications
    from ..models.new_campaign_session import NewCampaignSession
    from ..models.new_campaign_session_mode import NewCampaignSessionMode
    from ..models.new_message import NewMessage


T = TypeVar("T", bound="NewCampaign")


@attr.s(auto_attribs=True)
class NewCampaign:
    """
    Attributes:
        label (str):
        email_notifications (Union[Unset, EmailNotifications]):
        overview_messages (Union[Unset, List['NewMessage']]):
        session_modes (Union[Unset, List['NewCampaignSessionMode']]):
        sessions (Union[Unset, List['NewCampaignSession']]):
        stop_messages (Union[Unset, List['NewMessage']]):
        user_groups (Union[Unset, List['CampaignUserGroup']]):
        welcome_messages (Union[Unset, List['NewMessage']]):
    """

    label: str
    email_notifications: Union[Unset, "EmailNotifications"] = UNSET
    overview_messages: Union[Unset, List["NewMessage"]] = UNSET
    session_modes: Union[Unset, List["NewCampaignSessionMode"]] = UNSET
    sessions: Union[Unset, List["NewCampaignSession"]] = UNSET
    stop_messages: Union[Unset, List["NewMessage"]] = UNSET
    user_groups: Union[Unset, List["CampaignUserGroup"]] = UNSET
    welcome_messages: Union[Unset, List["NewMessage"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        email_notifications: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.email_notifications, Unset):
            email_notifications = self.email_notifications.to_dict()

        overview_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.overview_messages, Unset):
            overview_messages = []
            for overview_messages_item_data in self.overview_messages:
                overview_messages_item = overview_messages_item_data.to_dict()

                overview_messages.append(overview_messages_item)

        session_modes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.session_modes, Unset):
            session_modes = []
            for session_modes_item_data in self.session_modes:
                session_modes_item = session_modes_item_data.to_dict()

                session_modes.append(session_modes_item)

        sessions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sessions, Unset):
            sessions = []
            for sessions_item_data in self.sessions:
                sessions_item = sessions_item_data.to_dict()

                sessions.append(sessions_item)

        stop_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.stop_messages, Unset):
            stop_messages = []
            for stop_messages_item_data in self.stop_messages:
                stop_messages_item = stop_messages_item_data.to_dict()

                stop_messages.append(stop_messages_item)

        user_groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.user_groups, Unset):
            user_groups = []
            for user_groups_item_data in self.user_groups:
                user_groups_item = user_groups_item_data.to_dict()

                user_groups.append(user_groups_item)

        welcome_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.welcome_messages, Unset):
            welcome_messages = []
            for welcome_messages_item_data in self.welcome_messages:
                welcome_messages_item = welcome_messages_item_data.to_dict()

                welcome_messages.append(welcome_messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
            }
        )
        if email_notifications is not UNSET:
            field_dict["emailNotifications"] = email_notifications
        if overview_messages is not UNSET:
            field_dict["overviewMessages"] = overview_messages
        if session_modes is not UNSET:
            field_dict["sessionModes"] = session_modes
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if stop_messages is not UNSET:
            field_dict["stopMessages"] = stop_messages
        if user_groups is not UNSET:
            field_dict["userGroups"] = user_groups
        if welcome_messages is not UNSET:
            field_dict["welcomeMessages"] = welcome_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.campaign_user_group import CampaignUserGroup
        from ..models.email_notifications import EmailNotifications
        from ..models.new_campaign_session import NewCampaignSession
        from ..models.new_campaign_session_mode import NewCampaignSessionMode
        from ..models.new_message import NewMessage

        d = src_dict.copy()
        label = d.pop("label")

        _email_notifications = d.pop("emailNotifications", UNSET)
        email_notifications: Union[Unset, EmailNotifications]
        if isinstance(_email_notifications, Unset):
            email_notifications = UNSET
        else:
            email_notifications = EmailNotifications.from_dict(_email_notifications)

        overview_messages = []
        _overview_messages = d.pop("overviewMessages", UNSET)
        for overview_messages_item_data in _overview_messages or []:
            overview_messages_item = NewMessage.from_dict(overview_messages_item_data)

            overview_messages.append(overview_messages_item)

        session_modes = []
        _session_modes = d.pop("sessionModes", UNSET)
        for session_modes_item_data in _session_modes or []:
            session_modes_item = NewCampaignSessionMode.from_dict(session_modes_item_data)

            session_modes.append(session_modes_item)

        sessions = []
        _sessions = d.pop("sessions", UNSET)
        for sessions_item_data in _sessions or []:
            sessions_item = NewCampaignSession.from_dict(sessions_item_data)

            sessions.append(sessions_item)

        stop_messages = []
        _stop_messages = d.pop("stopMessages", UNSET)
        for stop_messages_item_data in _stop_messages or []:
            stop_messages_item = NewMessage.from_dict(stop_messages_item_data)

            stop_messages.append(stop_messages_item)

        user_groups = []
        _user_groups = d.pop("userGroups", UNSET)
        for user_groups_item_data in _user_groups or []:
            user_groups_item = CampaignUserGroup.from_dict(user_groups_item_data)

            user_groups.append(user_groups_item)

        welcome_messages = []
        _welcome_messages = d.pop("welcomeMessages", UNSET)
        for welcome_messages_item_data in _welcome_messages or []:
            welcome_messages_item = NewMessage.from_dict(welcome_messages_item_data)

            welcome_messages.append(welcome_messages_item)

        new_campaign = cls(
            label=label,
            email_notifications=email_notifications,
            overview_messages=overview_messages,
            session_modes=session_modes,
            sessions=sessions,
            stop_messages=stop_messages,
            user_groups=user_groups,
            welcome_messages=welcome_messages,
        )

        return new_campaign
