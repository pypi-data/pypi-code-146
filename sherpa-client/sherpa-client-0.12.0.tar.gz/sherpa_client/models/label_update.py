from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelUpdate")


@attr.s(auto_attribs=True)
class LabelUpdate:
    """
    Attributes:
        color (Union[Unset, str]):
        guideline (Union[Unset, str]):
        identifier (Union[Unset, str]):
        label (Union[Unset, str]):
        label_set_name (Union[Unset, str]):
    """

    color: Union[Unset, str] = UNSET
    guideline: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    label_set_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        guideline = self.guideline
        identifier = self.identifier
        label = self.label
        label_set_name = self.label_set_name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if guideline is not UNSET:
            field_dict["guideline"] = guideline
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if label is not UNSET:
            field_dict["label"] = label
        if label_set_name is not UNSET:
            field_dict["labelSetName"] = label_set_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        guideline = d.pop("guideline", UNSET)

        identifier = d.pop("identifier", UNSET)

        label = d.pop("label", UNSET)

        label_set_name = d.pop("labelSetName", UNSET)

        label_update = cls(
            color=color,
            guideline=guideline,
            identifier=identifier,
            label=label,
            label_set_name=label_set_name,
        )

        return label_update
