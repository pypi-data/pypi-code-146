from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.branch_one_default_item_input_transforms import BranchOneDefaultItemInputTransforms
from ..models.branch_one_default_item_retry import BranchOneDefaultItemRetry
from ..models.branch_one_default_item_sleep_type_0 import BranchOneDefaultItemSleepType0
from ..models.branch_one_default_item_sleep_type_1 import BranchOneDefaultItemSleepType1
from ..models.branch_one_default_item_stop_after_if import BranchOneDefaultItemStopAfterIf
from ..models.branch_one_default_item_suspend import BranchOneDefaultItemSuspend
from ..types import UNSET, Unset

T = TypeVar("T", bound="BranchOneDefaultItem")


@attr.s(auto_attribs=True)
class BranchOneDefaultItem:
    """
    Attributes:
        id (str):
        value (Any):
        input_transforms (Union[Unset, BranchOneDefaultItemInputTransforms]):
        stop_after_if (Union[Unset, BranchOneDefaultItemStopAfterIf]):
        sleep (Union[BranchOneDefaultItemSleepType0, BranchOneDefaultItemSleepType1, Unset]):
        summary (Union[Unset, str]):
        suspend (Union[Unset, BranchOneDefaultItemSuspend]):
        retry (Union[Unset, BranchOneDefaultItemRetry]):
    """

    id: str
    value: Any
    input_transforms: Union[Unset, BranchOneDefaultItemInputTransforms] = UNSET
    stop_after_if: Union[Unset, BranchOneDefaultItemStopAfterIf] = UNSET
    sleep: Union[BranchOneDefaultItemSleepType0, BranchOneDefaultItemSleepType1, Unset] = UNSET
    summary: Union[Unset, str] = UNSET
    suspend: Union[Unset, BranchOneDefaultItemSuspend] = UNSET
    retry: Union[Unset, BranchOneDefaultItemRetry] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        value = self.value
        input_transforms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_transforms, Unset):
            input_transforms = self.input_transforms.to_dict()

        stop_after_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_after_if, Unset):
            stop_after_if = self.stop_after_if.to_dict()

        sleep: Union[Dict[str, Any], Unset]
        if isinstance(self.sleep, Unset):
            sleep = UNSET

        elif isinstance(self.sleep, BranchOneDefaultItemSleepType0):
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        else:
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        summary = self.summary
        suspend: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.suspend, Unset):
            suspend = self.suspend.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if input_transforms is not UNSET:
            field_dict["input_transforms"] = input_transforms
        if stop_after_if is not UNSET:
            field_dict["stop_after_if"] = stop_after_if
        if sleep is not UNSET:
            field_dict["sleep"] = sleep
        if summary is not UNSET:
            field_dict["summary"] = summary
        if suspend is not UNSET:
            field_dict["suspend"] = suspend
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        _input_transforms = d.pop("input_transforms", UNSET)
        input_transforms: Union[Unset, BranchOneDefaultItemInputTransforms]
        if isinstance(_input_transforms, Unset):
            input_transforms = UNSET
        else:
            input_transforms = BranchOneDefaultItemInputTransforms.from_dict(_input_transforms)

        _stop_after_if = d.pop("stop_after_if", UNSET)
        stop_after_if: Union[Unset, BranchOneDefaultItemStopAfterIf]
        if isinstance(_stop_after_if, Unset):
            stop_after_if = UNSET
        else:
            stop_after_if = BranchOneDefaultItemStopAfterIf.from_dict(_stop_after_if)

        def _parse_sleep(data: object) -> Union[BranchOneDefaultItemSleepType0, BranchOneDefaultItemSleepType1, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _sleep_type_0 = data
                sleep_type_0: Union[Unset, BranchOneDefaultItemSleepType0]
                if isinstance(_sleep_type_0, Unset):
                    sleep_type_0 = UNSET
                else:
                    sleep_type_0 = BranchOneDefaultItemSleepType0.from_dict(_sleep_type_0)

                return sleep_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _sleep_type_1 = data
            sleep_type_1: Union[Unset, BranchOneDefaultItemSleepType1]
            if isinstance(_sleep_type_1, Unset):
                sleep_type_1 = UNSET
            else:
                sleep_type_1 = BranchOneDefaultItemSleepType1.from_dict(_sleep_type_1)

            return sleep_type_1

        sleep = _parse_sleep(d.pop("sleep", UNSET))

        summary = d.pop("summary", UNSET)

        _suspend = d.pop("suspend", UNSET)
        suspend: Union[Unset, BranchOneDefaultItemSuspend]
        if isinstance(_suspend, Unset):
            suspend = UNSET
        else:
            suspend = BranchOneDefaultItemSuspend.from_dict(_suspend)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, BranchOneDefaultItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = BranchOneDefaultItemRetry.from_dict(_retry)

        branch_one_default_item = cls(
            id=id,
            value=value,
            input_transforms=input_transforms,
            stop_after_if=stop_after_if,
            sleep=sleep,
            summary=summary,
            suspend=suspend,
            retry=retry,
        )

        branch_one_default_item.additional_properties = d
        return branch_one_default_item

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
