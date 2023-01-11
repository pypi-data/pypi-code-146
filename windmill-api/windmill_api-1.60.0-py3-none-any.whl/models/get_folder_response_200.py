from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.get_folder_response_200_extra_perms import GetFolderResponse200ExtraPerms

T = TypeVar("T", bound="GetFolderResponse200")


@attr.s(auto_attribs=True)
class GetFolderResponse200:
    """
    Attributes:
        name (str):
        owners (List[str]):
        extra_perms (GetFolderResponse200ExtraPerms):
    """

    name: str
    owners: List[str]
    extra_perms: GetFolderResponse200ExtraPerms
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        owners = self.owners

        extra_perms = self.extra_perms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "owners": owners,
                "extra_perms": extra_perms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        owners = cast(List[str], d.pop("owners"))

        extra_perms = GetFolderResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        get_folder_response_200 = cls(
            name=name,
            owners=owners,
            extra_perms=extra_perms,
        )

        get_folder_response_200.additional_properties = d
        return get_folder_response_200

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
