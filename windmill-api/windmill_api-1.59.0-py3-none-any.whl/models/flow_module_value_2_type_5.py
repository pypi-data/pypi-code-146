from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_5_branches_item import FlowModuleValue2Type5BranchesItem
from ..models.flow_module_value_2_type_5_type import FlowModuleValue2Type5Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type5")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type5:
    """
    Attributes:
        branches (List[FlowModuleValue2Type5BranchesItem]):
        type (FlowModuleValue2Type5Type):
        parallel (Union[Unset, bool]):
    """

    branches: List[FlowModuleValue2Type5BranchesItem]
    type: FlowModuleValue2Type5Type
    parallel: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        branches = []
        for branches_item_data in self.branches:
            branches_item = branches_item_data.to_dict()

            branches.append(branches_item)

        type = self.type.value

        parallel = self.parallel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "branches": branches,
                "type": type,
            }
        )
        if parallel is not UNSET:
            field_dict["parallel"] = parallel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        branches = []
        _branches = d.pop("branches")
        for branches_item_data in _branches:
            branches_item = FlowModuleValue2Type5BranchesItem.from_dict(branches_item_data)

            branches.append(branches_item)

        type = FlowModuleValue2Type5Type(d.pop("type"))

        parallel = d.pop("parallel", UNSET)

        flow_module_value_2_type_5 = cls(
            branches=branches,
            type=type,
            parallel=parallel,
        )

        flow_module_value_2_type_5.additional_properties = d
        return flow_module_value_2_type_5

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
