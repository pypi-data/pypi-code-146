from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.campaign_session import CampaignSession
    from ..models.campaign_session_mode import CampaignSessionMode
    from ..models.campaign_user_group import CampaignUserGroup
    from ..models.campaign_user_session import CampaignUserSession
    from ..models.email_notifications import EmailNotifications
    from ..models.message import Message
    from ..models.message_id import MessageId
    from ..models.new_campaign_session import NewCampaignSession
    from ..models.new_campaign_session_mode import NewCampaignSessionMode
    from ..models.new_campaign_user_session import NewCampaignUserSession
    from ..models.new_message import NewMessage


T = TypeVar("T", bound="CampaignPatch")


@attr.s(auto_attribs=True)
class CampaignPatch:
    """
    Attributes:
        email_notifications (Union[Unset, EmailNotifications]):
        label (Union[Unset, str]):
        overview_messages (Union[Unset, List[Union['Message', 'MessageId', 'NewMessage']]]):
        session_modes (Union[Unset, List[Union['CampaignSessionMode', 'NewCampaignSessionMode']]]):
        sessions (Union[Unset, List[Union['CampaignSession', 'NewCampaignSession']]]):
        stop_messages (Union[Unset, List[Union['Message', 'MessageId', 'NewMessage']]]):
        user_groups (Union[Unset, List['CampaignUserGroup']]):
        user_sessions (Union[Unset, List[Union['CampaignUserSession', 'NewCampaignUserSession']]]):
        welcome_messages (Union[Unset, List[Union['Message', 'MessageId', 'NewMessage']]]):
    """

    email_notifications: Union[Unset, "EmailNotifications"] = UNSET
    label: Union[Unset, str] = UNSET
    overview_messages: Union[Unset, List[Union["Message", "MessageId", "NewMessage"]]] = UNSET
    session_modes: Union[Unset, List[Union["CampaignSessionMode", "NewCampaignSessionMode"]]] = UNSET
    sessions: Union[Unset, List[Union["CampaignSession", "NewCampaignSession"]]] = UNSET
    stop_messages: Union[Unset, List[Union["Message", "MessageId", "NewMessage"]]] = UNSET
    user_groups: Union[Unset, List["CampaignUserGroup"]] = UNSET
    user_sessions: Union[Unset, List[Union["CampaignUserSession", "NewCampaignUserSession"]]] = UNSET
    welcome_messages: Union[Unset, List[Union["Message", "MessageId", "NewMessage"]]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.campaign_session import CampaignSession
        from ..models.campaign_session_mode import CampaignSessionMode
        from ..models.campaign_user_session import CampaignUserSession
        from ..models.message import Message
        from ..models.message_id import MessageId

        email_notifications: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.email_notifications, Unset):
            email_notifications = self.email_notifications.to_dict()

        label = self.label
        overview_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.overview_messages, Unset):
            overview_messages = []
            for overview_messages_item_data in self.overview_messages:
                overview_messages_item: Dict[str, Any]

                if isinstance(overview_messages_item_data, MessageId):
                    overview_messages_item = overview_messages_item_data.to_dict()

                elif isinstance(overview_messages_item_data, Message):
                    overview_messages_item = overview_messages_item_data.to_dict()

                else:
                    overview_messages_item = overview_messages_item_data.to_dict()

                overview_messages.append(overview_messages_item)

        session_modes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.session_modes, Unset):
            session_modes = []
            for session_modes_item_data in self.session_modes:
                session_modes_item: Dict[str, Any]

                if isinstance(session_modes_item_data, CampaignSessionMode):
                    session_modes_item = session_modes_item_data.to_dict()

                else:
                    session_modes_item = session_modes_item_data.to_dict()

                session_modes.append(session_modes_item)

        sessions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sessions, Unset):
            sessions = []
            for sessions_item_data in self.sessions:
                sessions_item: Dict[str, Any]

                if isinstance(sessions_item_data, CampaignSession):
                    sessions_item = sessions_item_data.to_dict()

                else:
                    sessions_item = sessions_item_data.to_dict()

                sessions.append(sessions_item)

        stop_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.stop_messages, Unset):
            stop_messages = []
            for stop_messages_item_data in self.stop_messages:
                stop_messages_item: Dict[str, Any]

                if isinstance(stop_messages_item_data, MessageId):
                    stop_messages_item = stop_messages_item_data.to_dict()

                elif isinstance(stop_messages_item_data, Message):
                    stop_messages_item = stop_messages_item_data.to_dict()

                else:
                    stop_messages_item = stop_messages_item_data.to_dict()

                stop_messages.append(stop_messages_item)

        user_groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.user_groups, Unset):
            user_groups = []
            for user_groups_item_data in self.user_groups:
                user_groups_item = user_groups_item_data.to_dict()

                user_groups.append(user_groups_item)

        user_sessions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.user_sessions, Unset):
            user_sessions = []
            for user_sessions_item_data in self.user_sessions:
                user_sessions_item: Dict[str, Any]

                if isinstance(user_sessions_item_data, CampaignUserSession):
                    user_sessions_item = user_sessions_item_data.to_dict()

                else:
                    user_sessions_item = user_sessions_item_data.to_dict()

                user_sessions.append(user_sessions_item)

        welcome_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.welcome_messages, Unset):
            welcome_messages = []
            for welcome_messages_item_data in self.welcome_messages:
                welcome_messages_item: Dict[str, Any]

                if isinstance(welcome_messages_item_data, MessageId):
                    welcome_messages_item = welcome_messages_item_data.to_dict()

                elif isinstance(welcome_messages_item_data, Message):
                    welcome_messages_item = welcome_messages_item_data.to_dict()

                else:
                    welcome_messages_item = welcome_messages_item_data.to_dict()

                welcome_messages.append(welcome_messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if email_notifications is not UNSET:
            field_dict["emailNotifications"] = email_notifications
        if label is not UNSET:
            field_dict["label"] = label
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
        if user_sessions is not UNSET:
            field_dict["userSessions"] = user_sessions
        if welcome_messages is not UNSET:
            field_dict["welcomeMessages"] = welcome_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.campaign_session import CampaignSession
        from ..models.campaign_session_mode import CampaignSessionMode
        from ..models.campaign_user_group import CampaignUserGroup
        from ..models.campaign_user_session import CampaignUserSession
        from ..models.email_notifications import EmailNotifications
        from ..models.message import Message
        from ..models.message_id import MessageId
        from ..models.new_campaign_session import NewCampaignSession
        from ..models.new_campaign_session_mode import NewCampaignSessionMode
        from ..models.new_campaign_user_session import NewCampaignUserSession
        from ..models.new_message import NewMessage

        d = src_dict.copy()
        _email_notifications = d.pop("emailNotifications", UNSET)
        email_notifications: Union[Unset, EmailNotifications]
        if isinstance(_email_notifications, Unset):
            email_notifications = UNSET
        else:
            email_notifications = EmailNotifications.from_dict(_email_notifications)

        label = d.pop("label", UNSET)

        overview_messages = []
        _overview_messages = d.pop("overviewMessages", UNSET)
        for overview_messages_item_data in _overview_messages or []:

            def _parse_overview_messages_item(data: object) -> Union["Message", "MessageId", "NewMessage"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    overview_messages_item_type_0 = MessageId.from_dict(data)

                    return overview_messages_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    overview_messages_item_type_1 = Message.from_dict(data)

                    return overview_messages_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                overview_messages_item_type_2 = NewMessage.from_dict(data)

                return overview_messages_item_type_2

            overview_messages_item = _parse_overview_messages_item(overview_messages_item_data)

            overview_messages.append(overview_messages_item)

        session_modes = []
        _session_modes = d.pop("sessionModes", UNSET)
        for session_modes_item_data in _session_modes or []:

            def _parse_session_modes_item(data: object) -> Union["CampaignSessionMode", "NewCampaignSessionMode"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    session_modes_item_type_0 = CampaignSessionMode.from_dict(data)

                    return session_modes_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                session_modes_item_type_1 = NewCampaignSessionMode.from_dict(data)

                return session_modes_item_type_1

            session_modes_item = _parse_session_modes_item(session_modes_item_data)

            session_modes.append(session_modes_item)

        sessions = []
        _sessions = d.pop("sessions", UNSET)
        for sessions_item_data in _sessions or []:

            def _parse_sessions_item(data: object) -> Union["CampaignSession", "NewCampaignSession"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    sessions_item_type_0 = CampaignSession.from_dict(data)

                    return sessions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                sessions_item_type_1 = NewCampaignSession.from_dict(data)

                return sessions_item_type_1

            sessions_item = _parse_sessions_item(sessions_item_data)

            sessions.append(sessions_item)

        stop_messages = []
        _stop_messages = d.pop("stopMessages", UNSET)
        for stop_messages_item_data in _stop_messages or []:

            def _parse_stop_messages_item(data: object) -> Union["Message", "MessageId", "NewMessage"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    stop_messages_item_type_0 = MessageId.from_dict(data)

                    return stop_messages_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    stop_messages_item_type_1 = Message.from_dict(data)

                    return stop_messages_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                stop_messages_item_type_2 = NewMessage.from_dict(data)

                return stop_messages_item_type_2

            stop_messages_item = _parse_stop_messages_item(stop_messages_item_data)

            stop_messages.append(stop_messages_item)

        user_groups = []
        _user_groups = d.pop("userGroups", UNSET)
        for user_groups_item_data in _user_groups or []:
            user_groups_item = CampaignUserGroup.from_dict(user_groups_item_data)

            user_groups.append(user_groups_item)

        user_sessions = []
        _user_sessions = d.pop("userSessions", UNSET)
        for user_sessions_item_data in _user_sessions or []:

            def _parse_user_sessions_item(data: object) -> Union["CampaignUserSession", "NewCampaignUserSession"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    user_sessions_item_type_0 = CampaignUserSession.from_dict(data)

                    return user_sessions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                user_sessions_item_type_1 = NewCampaignUserSession.from_dict(data)

                return user_sessions_item_type_1

            user_sessions_item = _parse_user_sessions_item(user_sessions_item_data)

            user_sessions.append(user_sessions_item)

        welcome_messages = []
        _welcome_messages = d.pop("welcomeMessages", UNSET)
        for welcome_messages_item_data in _welcome_messages or []:

            def _parse_welcome_messages_item(data: object) -> Union["Message", "MessageId", "NewMessage"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    welcome_messages_item_type_0 = MessageId.from_dict(data)

                    return welcome_messages_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    welcome_messages_item_type_1 = Message.from_dict(data)

                    return welcome_messages_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                welcome_messages_item_type_2 = NewMessage.from_dict(data)

                return welcome_messages_item_type_2

            welcome_messages_item = _parse_welcome_messages_item(welcome_messages_item_data)

            welcome_messages.append(welcome_messages_item)

        campaign_patch = cls(
            email_notifications=email_notifications,
            label=label,
            overview_messages=overview_messages,
            session_modes=session_modes,
            sessions=sessions,
            stop_messages=stop_messages,
            user_groups=user_groups,
            user_sessions=user_sessions,
            welcome_messages=welcome_messages,
        )

        return campaign_patch
