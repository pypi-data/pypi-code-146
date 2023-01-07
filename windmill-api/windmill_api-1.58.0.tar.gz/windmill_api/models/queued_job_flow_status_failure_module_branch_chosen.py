from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.queued_job_flow_status_failure_module_branch_chosen_type import (
    QueuedJobFlowStatusFailureModuleBranchChosenType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueuedJobFlowStatusFailureModuleBranchChosen")


@attr.s(auto_attribs=True)
class QueuedJobFlowStatusFailureModuleBranchChosen:
    """
    Attributes:
        type (QueuedJobFlowStatusFailureModuleBranchChosenType):
        branch (Union[Unset, int]):
    """

    type: QueuedJobFlowStatusFailureModuleBranchChosenType
    branch: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        branch = self.branch

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if branch is not UNSET:
            field_dict["branch"] = branch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = QueuedJobFlowStatusFailureModuleBranchChosenType(d.pop("type"))

        branch = d.pop("branch", UNSET)

        queued_job_flow_status_failure_module_branch_chosen = cls(
            type=type,
            branch=branch,
        )

        queued_job_flow_status_failure_module_branch_chosen.additional_properties = d
        return queued_job_flow_status_failure_module_branch_chosen

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
