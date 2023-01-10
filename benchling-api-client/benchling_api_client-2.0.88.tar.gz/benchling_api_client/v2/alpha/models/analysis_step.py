from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.analysis_step_dataset_data import AnalysisStepDatasetData
from ..models.analysis_step_file_data import AnalysisStepFileData
from ..models.analysis_step_status import AnalysisStepStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStep")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStep:
    """  """

    _id: Union[Unset, str] = UNSET
    _input_data: Union[Unset, List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]] = UNSET
    _output_data: Union[
        Unset, List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]
    ] = UNSET
    _status: Union[Unset, AnalysisStepStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("input_data={}".format(repr(self._input_data)))
        fields.append("output_data={}".format(repr(self._output_data)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStep({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        input_data: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._input_data, Unset):
            input_data = []
            for input_data_item_data in self._input_data:
                if isinstance(input_data_item_data, UnknownType):
                    input_data_item = input_data_item_data.value
                elif isinstance(input_data_item_data, AnalysisStepFileData):
                    input_data_item = input_data_item_data.to_dict()

                else:
                    input_data_item = input_data_item_data.to_dict()

                input_data.append(input_data_item)

        output_data: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._output_data, Unset):
            output_data = []
            for output_data_item_data in self._output_data:
                if isinstance(output_data_item_data, UnknownType):
                    output_data_item = output_data_item_data.value
                elif isinstance(output_data_item_data, AnalysisStepFileData):
                    output_data_item = output_data_item_data.to_dict()

                else:
                    output_data_item = output_data_item_data.to_dict()

                output_data.append(output_data_item)

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if input_data is not UNSET:
            field_dict["inputData"] = input_data
        if output_data is not UNSET:
            field_dict["outputData"] = output_data
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_input_data() -> Union[
            Unset, List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]
        ]:
            input_data = []
            _input_data = d.pop("inputData")
            for input_data_item_data in _input_data or []:

                def _parse_input_data_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]:
                    input_data_item: Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        analysis_step_data = AnalysisStepFileData.from_dict(data, strict=True)

                        return analysis_step_data
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        analysis_step_data = AnalysisStepDatasetData.from_dict(data, strict=True)

                        return analysis_step_data
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                input_data_item = _parse_input_data_item(input_data_item_data)

                input_data.append(input_data_item)

            return input_data

        try:
            input_data = get_input_data()
        except KeyError:
            if strict:
                raise
            input_data = cast(
                Union[Unset, List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]], UNSET
            )

        def get_output_data() -> Union[
            Unset, List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]
        ]:
            output_data = []
            _output_data = d.pop("outputData")
            for output_data_item_data in _output_data or []:

                def _parse_output_data_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]:
                    output_data_item: Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        analysis_step_data = AnalysisStepFileData.from_dict(data, strict=True)

                        return analysis_step_data
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        analysis_step_data = AnalysisStepDatasetData.from_dict(data, strict=True)

                        return analysis_step_data
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                output_data_item = _parse_output_data_item(output_data_item_data)

                output_data.append(output_data_item)

            return output_data

        try:
            output_data = get_output_data()
        except KeyError:
            if strict:
                raise
            output_data = cast(
                Union[Unset, List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]], UNSET
            )

        def get_status() -> Union[Unset, AnalysisStepStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = AnalysisStepStatus(_status)
                except ValueError:
                    status = AnalysisStepStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, AnalysisStepStatus], UNSET)

        analysis_step = cls(
            id=id,
            input_data=input_data,
            output_data=output_data,
            status=status,
        )

        analysis_step.additional_properties = d
        return analysis_step

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
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def input_data(self) -> List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]:
        if isinstance(self._input_data, Unset):
            raise NotPresentError(self, "input_data")
        return self._input_data

    @input_data.setter
    def input_data(
        self, value: List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]
    ) -> None:
        self._input_data = value

    @input_data.deleter
    def input_data(self) -> None:
        self._input_data = UNSET

    @property
    def output_data(self) -> List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]:
        if isinstance(self._output_data, Unset):
            raise NotPresentError(self, "output_data")
        return self._output_data

    @output_data.setter
    def output_data(
        self, value: List[Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]]
    ) -> None:
        self._output_data = value

    @output_data.deleter
    def output_data(self) -> None:
        self._output_data = UNSET

    @property
    def status(self) -> AnalysisStepStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: AnalysisStepStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
