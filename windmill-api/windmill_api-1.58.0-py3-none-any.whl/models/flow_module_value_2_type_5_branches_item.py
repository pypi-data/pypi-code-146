from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_5_branches_item_modules_item import FlowModuleValue2Type5BranchesItemModulesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type5BranchesItem")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type5BranchesItem:
    """
    Attributes:
        modules (List[FlowModuleValue2Type5BranchesItemModulesItem]):
        summary (Union[Unset, str]):
        skip_failure (Union[Unset, bool]):
    """

    modules: List[FlowModuleValue2Type5BranchesItemModulesItem]
    summary: Union[Unset, str] = UNSET
    skip_failure: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        modules = []
        for modules_item_data in self.modules:
            modules_item = modules_item_data.to_dict()

            modules.append(modules_item)

        summary = self.summary
        skip_failure = self.skip_failure

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "modules": modules,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if skip_failure is not UNSET:
            field_dict["skip_failure"] = skip_failure

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        modules = []
        _modules = d.pop("modules")
        for modules_item_data in _modules:
            modules_item = FlowModuleValue2Type5BranchesItemModulesItem.from_dict(modules_item_data)

            modules.append(modules_item)

        summary = d.pop("summary", UNSET)

        skip_failure = d.pop("skip_failure", UNSET)

        flow_module_value_2_type_5_branches_item = cls(
            modules=modules,
            summary=summary,
            skip_failure=skip_failure,
        )

        flow_module_value_2_type_5_branches_item.additional_properties = d
        return flow_module_value_2_type_5_branches_item

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
