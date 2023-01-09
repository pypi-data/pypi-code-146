from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.branch_all_branches_item import BranchAllBranchesItem
from ..models.branch_all_type import BranchAllType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BranchAll")


@attr.s(auto_attribs=True)
class BranchAll:
    """
    Attributes:
        branches (List[BranchAllBranchesItem]):
        type (BranchAllType):
        parallel (Union[Unset, bool]):
    """

    branches: List[BranchAllBranchesItem]
    type: BranchAllType
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
            branches_item = BranchAllBranchesItem.from_dict(branches_item_data)

            branches.append(branches_item)

        type = BranchAllType(d.pop("type"))

        parallel = d.pop("parallel", UNSET)

        branch_all = cls(
            branches=branches,
            type=type,
            parallel=parallel,
        )

        branch_all.additional_properties = d
        return branch_all

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
