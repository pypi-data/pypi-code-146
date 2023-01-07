from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_1_input_transforms import FlowModuleValue2Type1InputTransforms
from ..models.flow_module_value_2_type_1_type import FlowModuleValue2Type1Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type1")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type1:
    """
    Attributes:
        input_transforms (FlowModuleValue2Type1InputTransforms):
        path (str):
        type (FlowModuleValue2Type1Type):
        hash_ (Union[Unset, str]):
    """

    input_transforms: FlowModuleValue2Type1InputTransforms
    path: str
    type: FlowModuleValue2Type1Type
    hash_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms = self.input_transforms.to_dict()

        path = self.path
        type = self.type.value

        hash_ = self.hash_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transforms": input_transforms,
                "path": path,
                "type": type,
            }
        )
        if hash_ is not UNSET:
            field_dict["hash"] = hash_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_transforms = FlowModuleValue2Type1InputTransforms.from_dict(d.pop("input_transforms"))

        path = d.pop("path")

        type = FlowModuleValue2Type1Type(d.pop("type"))

        hash_ = d.pop("hash", UNSET)

        flow_module_value_2_type_1 = cls(
            input_transforms=input_transforms,
            path=path,
            type=type,
            hash_=hash_,
        )

        flow_module_value_2_type_1.additional_properties = d
        return flow_module_value_2_type_1

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
