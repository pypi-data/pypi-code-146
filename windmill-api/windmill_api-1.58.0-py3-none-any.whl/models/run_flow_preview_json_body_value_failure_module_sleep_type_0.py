from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.run_flow_preview_json_body_value_failure_module_sleep_type_0_type import (
    RunFlowPreviewJsonBodyValueFailureModuleSleepType0Type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="RunFlowPreviewJsonBodyValueFailureModuleSleepType0")


@attr.s(auto_attribs=True)
class RunFlowPreviewJsonBodyValueFailureModuleSleepType0:
    """
    Attributes:
        type (RunFlowPreviewJsonBodyValueFailureModuleSleepType0Type):
        value (Union[Unset, Any]):
    """

    type: RunFlowPreviewJsonBodyValueFailureModuleSleepType0Type
    value: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = RunFlowPreviewJsonBodyValueFailureModuleSleepType0Type(d.pop("type"))

        value = d.pop("value", UNSET)

        run_flow_preview_json_body_value_failure_module_sleep_type_0 = cls(
            type=type,
            value=value,
        )

        run_flow_preview_json_body_value_failure_module_sleep_type_0.additional_properties = d
        return run_flow_preview_json_body_value_failure_module_sleep_type_0

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
