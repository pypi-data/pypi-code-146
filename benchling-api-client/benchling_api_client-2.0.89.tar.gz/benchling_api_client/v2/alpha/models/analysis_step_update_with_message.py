from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.analysis_step_update_with_message_status import AnalysisStepUpdateWithMessageStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStepUpdateWithMessage")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStepUpdateWithMessage:
    """  """

    _status: Union[Unset, AnalysisStepUpdateWithMessageStatus] = UNSET
    _status_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("status={}".format(repr(self._status)))
        fields.append("status_message={}".format(repr(self._status_message)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStepUpdateWithMessage({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        status_message = self._status_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_status() -> Union[Unset, AnalysisStepUpdateWithMessageStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = AnalysisStepUpdateWithMessageStatus(_status)
                except ValueError:
                    status = AnalysisStepUpdateWithMessageStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, AnalysisStepUpdateWithMessageStatus], UNSET)

        def get_status_message() -> Union[Unset, str]:
            status_message = d.pop("statusMessage")
            return status_message

        try:
            status_message = get_status_message()
        except KeyError:
            if strict:
                raise
            status_message = cast(Union[Unset, str], UNSET)

        analysis_step_update_with_message = cls(
            status=status,
            status_message=status_message,
        )

        analysis_step_update_with_message.additional_properties = d
        return analysis_step_update_with_message

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
    def status(self) -> AnalysisStepUpdateWithMessageStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: AnalysisStepUpdateWithMessageStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET

    @property
    def status_message(self) -> str:
        if isinstance(self._status_message, Unset):
            raise NotPresentError(self, "status_message")
        return self._status_message

    @status_message.setter
    def status_message(self, value: str) -> None:
        self._status_message = value

    @status_message.deleter
    def status_message(self) -> None:
        self._status_message = UNSET
