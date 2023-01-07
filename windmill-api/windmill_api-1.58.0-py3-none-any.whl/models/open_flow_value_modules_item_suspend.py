from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenFlowValueModulesItemSuspend")


@attr.s(auto_attribs=True)
class OpenFlowValueModulesItemSuspend:
    """
    Attributes:
        required_events (Union[Unset, int]):
        timeout (Union[Unset, int]):
    """

    required_events: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        required_events = self.required_events
        timeout = self.timeout

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if required_events is not UNSET:
            field_dict["required_events"] = required_events
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        required_events = d.pop("required_events", UNSET)

        timeout = d.pop("timeout", UNSET)

        open_flow_value_modules_item_suspend = cls(
            required_events=required_events,
            timeout=timeout,
        )

        open_flow_value_modules_item_suspend.additional_properties = d
        return open_flow_value_modules_item_suspend

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
