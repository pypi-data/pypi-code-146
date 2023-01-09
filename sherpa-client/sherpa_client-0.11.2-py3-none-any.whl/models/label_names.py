from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelNames")


@attr.s(auto_attribs=True)
class LabelNames:
    """
    Attributes:
        names (Union[Unset, List[str]]):
    """

    names: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.names, Unset):
            names = self.names

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if names is not UNSET:
            field_dict["names"] = names

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        names = cast(List[str], d.pop("names", UNSET))

        label_names = cls(
            names=names,
        )

        return label_names
