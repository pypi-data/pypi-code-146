from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.flow_module_value_2_type_2_input_transforms import FlowModuleValue2Type2InputTransforms
from ..models.flow_module_value_2_type_2_type import FlowModuleValue2Type2Type

T = TypeVar("T", bound="FlowModuleValue2Type2")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type2:
    """
    Attributes:
        input_transforms (FlowModuleValue2Type2InputTransforms):
        path (str):
        type (FlowModuleValue2Type2Type):
    """

    input_transforms: FlowModuleValue2Type2InputTransforms
    path: str
    type: FlowModuleValue2Type2Type
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms = self.input_transforms.to_dict()

        path = self.path
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transforms": input_transforms,
                "path": path,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_transforms = FlowModuleValue2Type2InputTransforms.from_dict(d.pop("input_transforms"))

        path = d.pop("path")

        type = FlowModuleValue2Type2Type(d.pop("type"))

        flow_module_value_2_type_2 = cls(
            input_transforms=input_transforms,
            path=path,
            type=type,
        )

        flow_module_value_2_type_2.additional_properties = d
        return flow_module_value_2_type_2

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
