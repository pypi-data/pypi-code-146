from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.session_message_create import SessionMessageCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionCreate")


@attr.s(auto_attribs=True, repr=False)
class SessionCreate:
    """  """

    _app_id: str
    _label: str
    _timeout_seconds: int
    _messages: Union[Unset, List[SessionMessageCreate]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("app_id={}".format(repr(self._app_id)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("timeout_seconds={}".format(repr(self._timeout_seconds)))
        fields.append("messages={}".format(repr(self._messages)))
        return "SessionCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_id = self._app_id
        label = self._label
        timeout_seconds = self._timeout_seconds
        messages: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._messages, Unset):
            messages = []
            for messages_item_data in self._messages:
                messages_item = messages_item_data.to_dict()

                messages.append(messages_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_id is not UNSET:
            field_dict["appId"] = app_id
        if label is not UNSET:
            field_dict["label"] = label
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if messages is not UNSET:
            field_dict["messages"] = messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_id() -> str:
            app_id = d.pop("appId")
            return app_id

        try:
            app_id = get_app_id()
        except KeyError:
            if strict:
                raise
            app_id = cast(str, UNSET)

        def get_label() -> str:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(str, UNSET)

        def get_timeout_seconds() -> int:
            timeout_seconds = d.pop("timeoutSeconds")
            return timeout_seconds

        try:
            timeout_seconds = get_timeout_seconds()
        except KeyError:
            if strict:
                raise
            timeout_seconds = cast(int, UNSET)

        def get_messages() -> Union[Unset, List[SessionMessageCreate]]:
            messages = []
            _messages = d.pop("messages")
            for messages_item_data in _messages or []:
                messages_item = SessionMessageCreate.from_dict(messages_item_data, strict=False)

                messages.append(messages_item)

            return messages

        try:
            messages = get_messages()
        except KeyError:
            if strict:
                raise
            messages = cast(Union[Unset, List[SessionMessageCreate]], UNSET)

        session_create = cls(
            app_id=app_id,
            label=label,
            timeout_seconds=timeout_seconds,
            messages=messages,
        )

        return session_create

    @property
    def app_id(self) -> str:
        if isinstance(self._app_id, Unset):
            raise NotPresentError(self, "app_id")
        return self._app_id

    @app_id.setter
    def app_id(self, value: str) -> None:
        self._app_id = value

    @property
    def label(self) -> str:
        """The name of the session. Length must be between 3-100 chars. Label must be set to a string if it's currently null. It becomes immutable once a value is set."""
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @property
    def timeout_seconds(self) -> int:
        """Timeout in seconds, a value between 1 second and 30 days. Once set, it can only be increased, not decreased."""
        if isinstance(self._timeout_seconds, Unset):
            raise NotPresentError(self, "timeout_seconds")
        return self._timeout_seconds

    @timeout_seconds.setter
    def timeout_seconds(self, value: int) -> None:
        self._timeout_seconds = value

    @property
    def messages(self) -> List[SessionMessageCreate]:
        """An array of `SessionMessage` describing the current session state."""
        if isinstance(self._messages, Unset):
            raise NotPresentError(self, "messages")
        return self._messages

    @messages.setter
    def messages(self, value: List[SessionMessageCreate]) -> None:
        self._messages = value

    @messages.deleter
    def messages(self) -> None:
        self._messages = UNSET
