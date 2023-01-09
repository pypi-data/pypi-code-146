from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.get_suspended_job_flow_response_200_approvers_item import GetSuspendedJobFlowResponse200ApproversItem
from ..models.get_suspended_job_flow_response_200_job import GetSuspendedJobFlowResponse200Job

T = TypeVar("T", bound="GetSuspendedJobFlowResponse200")


@attr.s(auto_attribs=True)
class GetSuspendedJobFlowResponse200:
    """
    Attributes:
        job (GetSuspendedJobFlowResponse200Job):
        approvers (List[GetSuspendedJobFlowResponse200ApproversItem]):
    """

    job: GetSuspendedJobFlowResponse200Job
    approvers: List[GetSuspendedJobFlowResponse200ApproversItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job = self.job.to_dict()

        approvers = []
        for approvers_item_data in self.approvers:
            approvers_item = approvers_item_data.to_dict()

            approvers.append(approvers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job": job,
                "approvers": approvers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job = GetSuspendedJobFlowResponse200Job.from_dict(d.pop("job"))

        approvers = []
        _approvers = d.pop("approvers")
        for approvers_item_data in _approvers:
            approvers_item = GetSuspendedJobFlowResponse200ApproversItem.from_dict(approvers_item_data)

            approvers.append(approvers_item)

        get_suspended_job_flow_response_200 = cls(
            job=job,
            approvers=approvers,
        )

        get_suspended_job_flow_response_200.additional_properties = d
        return get_suspended_job_flow_response_200

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
