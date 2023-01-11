from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.branch_all_branches_item_modules_item_retry_constant import BranchAllBranchesItemModulesItemRetryConstant
from ..models.branch_all_branches_item_modules_item_retry_exponential import (
    BranchAllBranchesItemModulesItemRetryExponential,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BranchAllBranchesItemModulesItemRetry")


@attr.s(auto_attribs=True)
class BranchAllBranchesItemModulesItemRetry:
    """
    Attributes:
        constant (Union[Unset, BranchAllBranchesItemModulesItemRetryConstant]):
        exponential (Union[Unset, BranchAllBranchesItemModulesItemRetryExponential]):
    """

    constant: Union[Unset, BranchAllBranchesItemModulesItemRetryConstant] = UNSET
    exponential: Union[Unset, BranchAllBranchesItemModulesItemRetryExponential] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        constant: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.constant, Unset):
            constant = self.constant.to_dict()

        exponential: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exponential, Unset):
            exponential = self.exponential.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if constant is not UNSET:
            field_dict["constant"] = constant
        if exponential is not UNSET:
            field_dict["exponential"] = exponential

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _constant = d.pop("constant", UNSET)
        constant: Union[Unset, BranchAllBranchesItemModulesItemRetryConstant]
        if isinstance(_constant, Unset):
            constant = UNSET
        else:
            constant = BranchAllBranchesItemModulesItemRetryConstant.from_dict(_constant)

        _exponential = d.pop("exponential", UNSET)
        exponential: Union[Unset, BranchAllBranchesItemModulesItemRetryExponential]
        if isinstance(_exponential, Unset):
            exponential = UNSET
        else:
            exponential = BranchAllBranchesItemModulesItemRetryExponential.from_dict(_exponential)

        branch_all_branches_item_modules_item_retry = cls(
            constant=constant,
            exponential=exponential,
        )

        branch_all_branches_item_modules_item_retry.additional_properties = d
        return branch_all_branches_item_modules_item_retry

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
