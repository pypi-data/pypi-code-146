from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CampaignSessionMode")


@attr.s(auto_attribs=True)
class CampaignSessionMode:
    """
    Attributes:
        id (str):
        label (str):
        open_functional_roles (Union[Unset, List[str]]):
        started_functional_roles (Union[Unset, List[str]]):
    """

    id: str
    label: str
    open_functional_roles: Union[Unset, List[str]] = UNSET
    started_functional_roles: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        label = self.label
        open_functional_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.open_functional_roles, Unset):
            open_functional_roles = self.open_functional_roles

        started_functional_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.started_functional_roles, Unset):
            started_functional_roles = self.started_functional_roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "label": label,
            }
        )
        if open_functional_roles is not UNSET:
            field_dict["openFunctionalRoles"] = open_functional_roles
        if started_functional_roles is not UNSET:
            field_dict["startedFunctionalRoles"] = started_functional_roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        label = d.pop("label")

        open_functional_roles = cast(List[str], d.pop("openFunctionalRoles", UNSET))

        started_functional_roles = cast(List[str], d.pop("startedFunctionalRoles", UNSET))

        campaign_session_mode = cls(
            id=id,
            label=label,
            open_functional_roles=open_functional_roles,
            started_functional_roles=started_functional_roles,
        )

        return campaign_session_mode
