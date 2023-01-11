from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.identity_type import IdentityType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Identity")


@attr.s(auto_attribs=True)
class Identity:
    """
    Attributes:
        type (IdentityType):
        flow (Union[Unset, bool]):
    """

    type: IdentityType
    flow: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        flow = self.flow

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if flow is not UNSET:
            field_dict["flow"] = flow

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = IdentityType(d.pop("type"))

        flow = d.pop("flow", UNSET)

        identity = cls(
            type=type,
            flow=flow,
        )

        identity.additional_properties = d
        return identity

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
