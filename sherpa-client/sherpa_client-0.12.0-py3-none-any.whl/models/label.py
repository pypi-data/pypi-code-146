from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Label")


@attr.s(auto_attribs=True)
class Label:
    """
    Attributes:
        color (str):
        label (str):
        name (str):
        count (Union[Unset, int]):
        guideline (Union[Unset, str]):
        identifier (Union[Unset, str]):
        label_set_name (Union[Unset, str]):
    """

    color: str
    label: str
    name: str
    count: Union[Unset, int] = UNSET
    guideline: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    label_set_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        label = self.label
        name = self.name
        count = self.count
        guideline = self.guideline
        identifier = self.identifier
        label_set_name = self.label_set_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "color": color,
                "label": label,
                "name": name,
            }
        )
        if count is not UNSET:
            field_dict["count"] = count
        if guideline is not UNSET:
            field_dict["guideline"] = guideline
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if label_set_name is not UNSET:
            field_dict["labelSetName"] = label_set_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color")

        label = d.pop("label")

        name = d.pop("name")

        count = d.pop("count", UNSET)

        guideline = d.pop("guideline", UNSET)

        identifier = d.pop("identifier", UNSET)

        label_set_name = d.pop("labelSetName", UNSET)

        label = cls(
            color=color,
            label=label,
            name=name,
            count=count,
            guideline=guideline,
            identifier=identifier,
            label_set_name=label_set_name,
        )

        return label
