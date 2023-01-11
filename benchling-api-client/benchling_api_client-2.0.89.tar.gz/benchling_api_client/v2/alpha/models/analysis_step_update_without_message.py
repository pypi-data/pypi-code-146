from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.analysis_step_update_without_message_status import AnalysisStepUpdateWithoutMessageStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStepUpdateWithoutMessage")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStepUpdateWithoutMessage:
    """  """

    _status: Union[Unset, AnalysisStepUpdateWithoutMessageStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStepUpdateWithoutMessage({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_status() -> Union[Unset, AnalysisStepUpdateWithoutMessageStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = AnalysisStepUpdateWithoutMessageStatus(_status)
                except ValueError:
                    status = AnalysisStepUpdateWithoutMessageStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, AnalysisStepUpdateWithoutMessageStatus], UNSET)

        analysis_step_update_without_message = cls(
            status=status,
        )

        analysis_step_update_without_message.additional_properties = d
        return analysis_step_update_without_message

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def status(self) -> AnalysisStepUpdateWithoutMessageStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: AnalysisStepUpdateWithoutMessageStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
