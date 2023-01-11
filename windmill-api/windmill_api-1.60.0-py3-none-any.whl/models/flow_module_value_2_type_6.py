from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_6_type import FlowModuleValue2Type6Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type6")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type6:
    """
    Attributes:
        type (FlowModuleValue2Type6Type):
        flow (Union[Unset, bool]):
    """

    type: FlowModuleValue2Type6Type
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
        type = FlowModuleValue2Type6Type(d.pop("type"))

        flow = d.pop("flow", UNSET)

        flow_module_value_2_type_6 = cls(
            type=type,
            flow=flow,
        )

        flow_module_value_2_type_6.additional_properties = d
        return flow_module_value_2_type_6

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
