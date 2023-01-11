from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.session import Session
from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class SessionsPaginatedList:
    """  """

    _sessions: Union[Unset, List[Session]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("sessions={}".format(repr(self._sessions)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "SessionsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        sessions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._sessions, Unset):
            sessions = []
            for sessions_item_data in self._sessions:
                sessions_item = sessions_item_data.to_dict()

                sessions.append(sessions_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_sessions() -> Union[Unset, List[Session]]:
            sessions = []
            _sessions = d.pop("sessions")
            for sessions_item_data in _sessions or []:
                sessions_item = Session.from_dict(sessions_item_data, strict=False)

                sessions.append(sessions_item)

            return sessions

        try:
            sessions = get_sessions()
        except KeyError:
            if strict:
                raise
            sessions = cast(Union[Unset, List[Session]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        sessions_paginated_list = cls(
            sessions=sessions,
            next_token=next_token,
        )

        sessions_paginated_list.additional_properties = d
        return sessions_paginated_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def sessions(self) -> List[Session]:
        if isinstance(self._sessions, Unset):
            raise NotPresentError(self, "sessions")
        return self._sessions

    @sessions.setter
    def sessions(self, value: List[Session]) -> None:
        self._sessions = value

    @sessions.deleter
    def sessions(self) -> None:
        self._sessions = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
