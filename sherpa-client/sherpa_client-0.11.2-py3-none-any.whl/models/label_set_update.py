from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelSetUpdate")


@attr.s(auto_attribs=True)
class LabelSetUpdate:
    """
    Attributes:
        exclusive_classes (Union[Unset, bool]):
        label (Union[Unset, str]):
        nature (Union[Unset, str]):
    """

    exclusive_classes: Union[Unset, bool] = UNSET
    label: Union[Unset, str] = UNSET
    nature: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        exclusive_classes = self.exclusive_classes
        label = self.label
        nature = self.nature

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if exclusive_classes is not UNSET:
            field_dict["exclusiveClasses"] = exclusive_classes
        if label is not UNSET:
            field_dict["label"] = label
        if nature is not UNSET:
            field_dict["nature"] = nature

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exclusive_classes = d.pop("exclusiveClasses", UNSET)

        label = d.pop("label", UNSET)

        nature = d.pop("nature", UNSET)

        label_set_update = cls(
            exclusive_classes=exclusive_classes,
            label=label,
            nature=nature,
        )

        return label_set_update
