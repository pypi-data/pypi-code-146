from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="CampaignRolesChange")


@attr.s(auto_attribs=True)
class CampaignRolesChange:
    """
    Attributes:
        added_roles (List[str]):
        remove_current_funtional_roles (bool):
        removed_roles (List[str]):
        username (str):
    """

    added_roles: List[str]
    remove_current_funtional_roles: bool
    removed_roles: List[str]
    username: str

    def to_dict(self) -> Dict[str, Any]:
        added_roles = self.added_roles

        remove_current_funtional_roles = self.remove_current_funtional_roles
        removed_roles = self.removed_roles

        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "addedRoles": added_roles,
                "removeCurrentFuntionalRoles": remove_current_funtional_roles,
                "removedRoles": removed_roles,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        added_roles = cast(List[str], d.pop("addedRoles"))

        remove_current_funtional_roles = d.pop("removeCurrentFuntionalRoles")

        removed_roles = cast(List[str], d.pop("removedRoles"))

        username = d.pop("username")

        campaign_roles_change = cls(
            added_roles=added_roles,
            remove_current_funtional_roles=remove_current_funtional_roles,
            removed_roles=removed_roles,
            username=username,
        )

        return campaign_roles_change
