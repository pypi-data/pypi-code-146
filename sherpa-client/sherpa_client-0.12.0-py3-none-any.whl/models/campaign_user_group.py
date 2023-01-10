from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="CampaignUserGroup")


@attr.s(auto_attribs=True)
class CampaignUserGroup:
    """
    Attributes:
        label (str):
        users (List[str]):
    """

    label: str
    users: List[str]

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        users = self.users

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        users = cast(List[str], d.pop("users"))

        campaign_user_group = cls(
            label=label,
            users=users,
        )

        return campaign_user_group
