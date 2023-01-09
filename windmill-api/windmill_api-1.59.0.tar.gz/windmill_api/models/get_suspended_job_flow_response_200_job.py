from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.get_suspended_job_flow_response_200_job_type import GetSuspendedJobFlowResponse200JobType
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSuspendedJobFlowResponse200Job")


@attr.s(auto_attribs=True)
class GetSuspendedJobFlowResponse200Job:
    """
    Attributes:
        type (Union[Unset, GetSuspendedJobFlowResponse200JobType]):
    """

    type: Union[Unset, GetSuspendedJobFlowResponse200JobType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, GetSuspendedJobFlowResponse200JobType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetSuspendedJobFlowResponse200JobType(_type)

        get_suspended_job_flow_response_200_job = cls(
            type=type,
        )

        get_suspended_job_flow_response_200_job.additional_properties = d
        return get_suspended_job_flow_response_200_job

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
