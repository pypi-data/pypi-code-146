from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Annotator")


@attr.s(auto_attribs=True)
class Annotator:
    """
    Attributes:
        engine (str):
        favorite (bool):
        label (str):
        name (str):
        is_default (Union[Unset, bool]):
    """

    engine: str
    favorite: bool
    label: str
    name: str
    is_default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        engine = self.engine
        favorite = self.favorite
        label = self.label
        name = self.name
        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "engine": engine,
                "favorite": favorite,
                "label": label,
                "name": name,
            }
        )
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        engine = d.pop("engine")

        favorite = d.pop("favorite")

        label = d.pop("label")

        name = d.pop("name")

        is_default = d.pop("isDefault", UNSET)

        annotator = cls(
            engine=engine,
            favorite=favorite,
            label=label,
            name=name,
            is_default=is_default,
        )

        return annotator
