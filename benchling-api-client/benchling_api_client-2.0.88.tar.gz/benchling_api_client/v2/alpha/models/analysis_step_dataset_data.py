from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.analysis_step_dataset_data_kind import AnalysisStepDatasetDataKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStepDatasetData")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStepDatasetData:
    """  """

    _id: Union[Unset, None] = UNSET
    _is_multi: Union[Unset, None] = UNSET
    _kind: Union[Unset, AnalysisStepDatasetDataKind] = UNSET
    _name: Union[Unset, None] = UNSET
    _dataset_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("is_multi={}".format(repr(self._is_multi)))
        fields.append("kind={}".format(repr(self._kind)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("dataset_ids={}".format(repr(self._dataset_ids)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStepDatasetData({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = None

        is_multi = None

        kind: Union[Unset, int] = UNSET
        if not isinstance(self._kind, Unset):
            kind = self._kind.value

        name = None

        dataset_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._dataset_ids, Unset):
            dataset_ids = self._dataset_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if kind is not UNSET:
            field_dict["kind"] = kind
        if name is not UNSET:
            field_dict["name"] = name
        if dataset_ids is not UNSET:
            field_dict["datasetIds"] = dataset_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> Union[Unset, None]:
            id = None

            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, None], UNSET)

        def get_is_multi() -> Union[Unset, None]:
            is_multi = None

            return is_multi

        try:
            is_multi = get_is_multi()
        except KeyError:
            if strict:
                raise
            is_multi = cast(Union[Unset, None], UNSET)

        def get_kind() -> Union[Unset, AnalysisStepDatasetDataKind]:
            kind = UNSET
            _kind = d.pop("kind")
            if _kind is not None and _kind is not UNSET:
                try:
                    kind = AnalysisStepDatasetDataKind(_kind)
                except ValueError:
                    kind = AnalysisStepDatasetDataKind.of_unknown(_kind)

            return kind

        try:
            kind = get_kind()
        except KeyError:
            if strict:
                raise
            kind = cast(Union[Unset, AnalysisStepDatasetDataKind], UNSET)

        def get_name() -> Union[Unset, None]:
            name = None

            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, None], UNSET)

        def get_dataset_ids() -> Union[Unset, List[str]]:
            dataset_ids = cast(List[str], d.pop("datasetIds"))

            return dataset_ids

        try:
            dataset_ids = get_dataset_ids()
        except KeyError:
            if strict:
                raise
            dataset_ids = cast(Union[Unset, List[str]], UNSET)

        analysis_step_dataset_data = cls(
            id=id,
            is_multi=is_multi,
            kind=kind,
            name=name,
            dataset_ids=dataset_ids,
        )

        analysis_step_dataset_data.additional_properties = d
        return analysis_step_dataset_data

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
    def id(self) -> None:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: None) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def is_multi(self) -> None:
        if isinstance(self._is_multi, Unset):
            raise NotPresentError(self, "is_multi")
        return self._is_multi

    @is_multi.setter
    def is_multi(self, value: None) -> None:
        self._is_multi = value

    @is_multi.deleter
    def is_multi(self) -> None:
        self._is_multi = UNSET

    @property
    def kind(self) -> AnalysisStepDatasetDataKind:
        if isinstance(self._kind, Unset):
            raise NotPresentError(self, "kind")
        return self._kind

    @kind.setter
    def kind(self, value: AnalysisStepDatasetDataKind) -> None:
        self._kind = value

    @kind.deleter
    def kind(self) -> None:
        self._kind = UNSET

    @property
    def name(self) -> None:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: None) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def dataset_ids(self) -> List[str]:
        if isinstance(self._dataset_ids, Unset):
            raise NotPresentError(self, "dataset_ids")
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, value: List[str]) -> None:
        self._dataset_ids = value

    @dataset_ids.deleter
    def dataset_ids(self) -> None:
        self._dataset_ids = UNSET
