from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="UserSessionState")


@attr.s(auto_attribs=True)
class UserSessionState:
    """
    Attributes:
        enumname (bool):
    """

    enumname: bool

    def to_dict(self) -> Dict[str, Any]:
        enumname = self.enumname

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "$enum$name": enumname,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enumname = d.pop("$enum$name")

        user_session_state = cls(
            enumname=enumname,
        )

        return user_session_state
