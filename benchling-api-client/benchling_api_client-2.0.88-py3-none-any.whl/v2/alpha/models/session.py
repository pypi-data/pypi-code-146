import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.session_message import SessionMessage
from ..models.session_status import SessionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Session")


@attr.s(auto_attribs=True, repr=False)
class Session:
    """  """

    _app_id: Union[Unset, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _id: Union[Unset, str] = UNSET
    _label: Union[Unset, str] = UNSET
    _messages: Union[Unset, None, List[SessionMessage]] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _status: Union[Unset, SessionStatus] = UNSET
    _timeout_seconds: Union[Unset, int] = UNSET

    def __repr__(self):
        fields = []
        fields.append("app_id={}".format(repr(self._app_id)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("messages={}".format(repr(self._messages)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("timeout_seconds={}".format(repr(self._timeout_seconds)))
        return "Session({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_id = self._app_id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        id = self._id
        label = self._label
        messages: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._messages, Unset):
            if self._messages is None:
                messages = None
            else:
                messages = []
                for messages_item_data in self._messages:
                    messages_item = messages_item_data.to_dict()

                    messages.append(messages_item)

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        timeout_seconds = self._timeout_seconds

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_id is not UNSET:
            field_dict["appId"] = app_id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if label is not UNSET:
            field_dict["label"] = label
        if messages is not UNSET:
            field_dict["messages"] = messages
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if status is not UNSET:
            field_dict["status"] = status
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_id() -> Union[Unset, str]:
            app_id = d.pop("appId")
            return app_id

        try:
            app_id = get_app_id()
        except KeyError:
            if strict:
                raise
            app_id = cast(Union[Unset, str], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_label() -> Union[Unset, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, str], UNSET)

        def get_messages() -> Union[Unset, None, List[SessionMessage]]:
            messages = []
            _messages = d.pop("messages")
            for messages_item_data in _messages or []:
                messages_item = SessionMessage.from_dict(messages_item_data, strict=False)

                messages.append(messages_item)

            return messages

        try:
            messages = get_messages()
        except KeyError:
            if strict:
                raise
            messages = cast(Union[Unset, None, List[SessionMessage]], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_status() -> Union[Unset, SessionStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = SessionStatus(_status)
                except ValueError:
                    status = SessionStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, SessionStatus], UNSET)

        def get_timeout_seconds() -> Union[Unset, int]:
            timeout_seconds = d.pop("timeoutSeconds")
            return timeout_seconds

        try:
            timeout_seconds = get_timeout_seconds()
        except KeyError:
            if strict:
                raise
            timeout_seconds = cast(Union[Unset, int], UNSET)

        session = cls(
            app_id=app_id,
            created_at=created_at,
            id=id,
            label=label,
            messages=messages,
            modified_at=modified_at,
            status=status,
            timeout_seconds=timeout_seconds,
        )

        return session

    @property
    def app_id(self) -> str:
        if isinstance(self._app_id, Unset):
            raise NotPresentError(self, "app_id")
        return self._app_id

    @app_id.setter
    def app_id(self, value: str) -> None:
        self._app_id = value

    @app_id.deleter
    def app_id(self) -> None:
        self._app_id = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def label(self) -> str:
        """A brief description of the app's actions for users. Length must be between 3-100 chars. Label must be set to a string if it's currently null. It becomes immutable once a value is set."""
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @label.deleter
    def label(self) -> None:
        self._label = UNSET

    @property
    def messages(self) -> Optional[List[SessionMessage]]:
        """An array of `SessionMessage` describing the current session state."""
        if isinstance(self._messages, Unset):
            raise NotPresentError(self, "messages")
        return self._messages

    @messages.setter
    def messages(self, value: Optional[List[SessionMessage]]) -> None:
        self._messages = value

    @messages.deleter
    def messages(self) -> None:
        self._messages = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def status(self) -> SessionStatus:
        """All possible values of a Session's status, including system-updated and user-updated values."""
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: SessionStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET

    @property
    def timeout_seconds(self) -> int:
        """Timeout in seconds, a value between 1 second and 30 days. Once set, it can only be increased, not decreased."""
        if isinstance(self._timeout_seconds, Unset):
            raise NotPresentError(self, "timeout_seconds")
        return self._timeout_seconds

    @timeout_seconds.setter
    def timeout_seconds(self, value: int) -> None:
        self._timeout_seconds = value

    @timeout_seconds.deleter
    def timeout_seconds(self) -> None:
        self._timeout_seconds = UNSET
