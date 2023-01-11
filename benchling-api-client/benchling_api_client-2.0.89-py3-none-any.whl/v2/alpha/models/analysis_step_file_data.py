from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.analysis_step_file_data_kind import AnalysisStepFileDataKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStepFileData")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStepFileData:
    """  """

    _is_multi: Union[Unset, None] = UNSET
    _kind: Union[Unset, AnalysisStepFileDataKind] = UNSET
    _name: Union[Unset, None] = UNSET
    _file_ids: Union[Unset, List[str]] = UNSET
    _id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("is_multi={}".format(repr(self._is_multi)))
        fields.append("kind={}".format(repr(self._kind)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("file_ids={}".format(repr(self._file_ids)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStepFileData({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        is_multi = None

        kind: Union[Unset, int] = UNSET
        if not isinstance(self._kind, Unset):
            kind = self._kind.value

        name = None

        file_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._file_ids, Unset):
            file_ids = self._file_ids

        id = self._id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if kind is not UNSET:
            field_dict["kind"] = kind
        if name is not UNSET:
            field_dict["name"] = name
        if file_ids is not UNSET:
            field_dict["fileIds"] = file_ids
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_is_multi() -> Union[Unset, None]:
            is_multi = None

            return is_multi

        try:
            is_multi = get_is_multi()
        except KeyError:
            if strict:
                raise
            is_multi = cast(Union[Unset, None], UNSET)

        def get_kind() -> Union[Unset, AnalysisStepFileDataKind]:
            kind = UNSET
            _kind = d.pop("kind")
            if _kind is not None and _kind is not UNSET:
                try:
                    kind = AnalysisStepFileDataKind(_kind)
                except ValueError:
                    kind = AnalysisStepFileDataKind.of_unknown(_kind)

            return kind

        try:
            kind = get_kind()
        except KeyError:
            if strict:
                raise
            kind = cast(Union[Unset, AnalysisStepFileDataKind], UNSET)

        def get_name() -> Union[Unset, None]:
            name = None

            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, None], UNSET)

        def get_file_ids() -> Union[Unset, List[str]]:
            file_ids = cast(List[str], d.pop("fileIds"))

            return file_ids

        try:
            file_ids = get_file_ids()
        except KeyError:
            if strict:
                raise
            file_ids = cast(Union[Unset, List[str]], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        analysis_step_file_data = cls(
            is_multi=is_multi,
            kind=kind,
            name=name,
            file_ids=file_ids,
            id=id,
        )

        analysis_step_file_data.additional_properties = d
        return analysis_step_file_data

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
    def kind(self) -> AnalysisStepFileDataKind:
        if isinstance(self._kind, Unset):
            raise NotPresentError(self, "kind")
        return self._kind

    @kind.setter
    def kind(self, value: AnalysisStepFileDataKind) -> None:
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
    def file_ids(self) -> List[str]:
        if isinstance(self._file_ids, Unset):
            raise NotPresentError(self, "file_ids")
        return self._file_ids

    @file_ids.setter
    def file_ids(self, value: List[str]) -> None:
        self._file_ids = value

    @file_ids.deleter
    def file_ids(self) -> None:
        self._file_ids = UNSET

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
