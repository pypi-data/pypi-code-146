from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_4_branches_item_modules_item import FlowModuleValue2Type4BranchesItemModulesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type4BranchesItem")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type4BranchesItem:
    """
    Attributes:
        expr (str):
        modules (List[FlowModuleValue2Type4BranchesItemModulesItem]):
        summary (Union[Unset, str]):
    """

    expr: str
    modules: List[FlowModuleValue2Type4BranchesItemModulesItem]
    summary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expr = self.expr
        modules = []
        for modules_item_data in self.modules:
            modules_item = modules_item_data.to_dict()

            modules.append(modules_item)

        summary = self.summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expr": expr,
                "modules": modules,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expr = d.pop("expr")

        modules = []
        _modules = d.pop("modules")
        for modules_item_data in _modules:
            modules_item = FlowModuleValue2Type4BranchesItemModulesItem.from_dict(modules_item_data)

            modules.append(modules_item)

        summary = d.pop("summary", UNSET)

        flow_module_value_2_type_4_branches_item = cls(
            expr=expr,
            modules=modules,
            summary=summary,
        )

        flow_module_value_2_type_4_branches_item.additional_properties = d
        return flow_module_value_2_type_4_branches_item

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
