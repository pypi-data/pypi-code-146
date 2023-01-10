from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPermissionsUpdate")


@attr.s(auto_attribs=True)
class UserPermissionsUpdate:
    """
    Attributes:
        disabled (Union[Unset, bool]):
        permissions (Union[Unset, List[str]]):
        roles (Union[Unset, List[str]]):
    """

    disabled: Union[Unset, bool] = UNSET
    permissions: Union[Unset, List[str]] = UNSET
    roles: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        disabled = self.disabled
        permissions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        disabled = d.pop("disabled", UNSET)

        permissions = cast(List[str], d.pop("permissions", UNSET))

        roles = cast(List[str], d.pop("roles", UNSET))

        user_permissions_update = cls(
            disabled=disabled,
            permissions=permissions,
            roles=roles,
        )

        return user_permissions_update
