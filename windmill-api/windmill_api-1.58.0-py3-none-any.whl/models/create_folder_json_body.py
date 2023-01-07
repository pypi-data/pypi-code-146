from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateFolderJsonBody")


@attr.s(auto_attribs=True)
class CreateFolderJsonBody:
    """
    Attributes:
        name (str):
        owners (Union[Unset, List[str]]):
        extra_perms (Union[Unset, Any]):
    """

    name: str
    owners: Union[Unset, List[str]] = UNSET
    extra_perms: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        owners: Union[Unset, List[str]] = UNSET
        if not isinstance(self.owners, Unset):
            owners = self.owners

        extra_perms = self.extra_perms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if owners is not UNSET:
            field_dict["owners"] = owners
        if extra_perms is not UNSET:
            field_dict["extra_perms"] = extra_perms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        owners = cast(List[str], d.pop("owners", UNSET))

        extra_perms = d.pop("extra_perms", UNSET)

        create_folder_json_body = cls(
            name=name,
            owners=owners,
            extra_perms=extra_perms,
        )

        create_folder_json_body.additional_properties = d
        return create_folder_json_body

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
