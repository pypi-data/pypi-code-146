from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailNotifications")


@attr.s(auto_attribs=True)
class EmailNotifications:
    """
    Attributes:
        enabled (bool):
        notified_users (Union[Unset, List[str]]):
    """

    enabled: bool
    notified_users: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        notified_users: Union[Unset, List[str]] = UNSET
        if not isinstance(self.notified_users, Unset):
            notified_users = self.notified_users

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "enabled": enabled,
            }
        )
        if notified_users is not UNSET:
            field_dict["notifiedUsers"] = notified_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled")

        notified_users = cast(List[str], d.pop("notifiedUsers", UNSET))

        email_notifications = cls(
            enabled=enabled,
            notified_users=notified_users,
        )

        return email_notifications
