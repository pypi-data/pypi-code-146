from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetCreateFromFile")


@attr.s(auto_attribs=True, repr=False)
class DatasetCreateFromFile:
    """  """

    _file_id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("file_id={}".format(repr(self._file_id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DatasetCreateFromFile({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        file_id = self._file_id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if file_id is not UNSET:
            field_dict["fileId"] = file_id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_file_id() -> Union[Unset, str]:
            file_id = d.pop("fileId")
            return file_id

        try:
            file_id = get_file_id()
        except KeyError:
            if strict:
                raise
            file_id = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        dataset_create_from_file = cls(
            file_id=file_id,
            name=name,
        )

        dataset_create_from_file.additional_properties = d
        return dataset_create_from_file

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
    def file_id(self) -> str:
        """The File ID for a File with SUCCEEDED upload status. Dataset validation depends on the extension of the File.
        Only files with a `csv` extension can be used to create a Dataset.
        """
        if isinstance(self._file_id, Unset):
            raise NotPresentError(self, "file_id")
        return self._file_id

    @file_id.setter
    def file_id(self, value: str) -> None:
        self._file_id = value

    @file_id.deleter
    def file_id(self) -> None:
        self._file_id = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
