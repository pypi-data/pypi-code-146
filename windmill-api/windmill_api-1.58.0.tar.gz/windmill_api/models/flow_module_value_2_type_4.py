from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.flow_module_value_2_type_4_branches_item import FlowModuleValue2Type4BranchesItem
from ..models.flow_module_value_2_type_4_default_item import FlowModuleValue2Type4DefaultItem
from ..models.flow_module_value_2_type_4_type import FlowModuleValue2Type4Type

T = TypeVar("T", bound="FlowModuleValue2Type4")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type4:
    """
    Attributes:
        branches (List[FlowModuleValue2Type4BranchesItem]):
        default (List[FlowModuleValue2Type4DefaultItem]):
        type (FlowModuleValue2Type4Type):
    """

    branches: List[FlowModuleValue2Type4BranchesItem]
    default: List[FlowModuleValue2Type4DefaultItem]
    type: FlowModuleValue2Type4Type
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        branches = []
        for branches_item_data in self.branches:
            branches_item = branches_item_data.to_dict()

            branches.append(branches_item)

        default = []
        for default_item_data in self.default:
            default_item = default_item_data.to_dict()

            default.append(default_item)

        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "branches": branches,
                "default": default,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        branches = []
        _branches = d.pop("branches")
        for branches_item_data in _branches:
            branches_item = FlowModuleValue2Type4BranchesItem.from_dict(branches_item_data)

            branches.append(branches_item)

        default = []
        _default = d.pop("default")
        for default_item_data in _default:
            default_item = FlowModuleValue2Type4DefaultItem.from_dict(default_item_data)

            default.append(default_item)

        type = FlowModuleValue2Type4Type(d.pop("type"))

        flow_module_value_2_type_4 = cls(
            branches=branches,
            default=default,
            type=type,
        )

        flow_module_value_2_type_4.additional_properties = d
        return flow_module_value_2_type_4

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
