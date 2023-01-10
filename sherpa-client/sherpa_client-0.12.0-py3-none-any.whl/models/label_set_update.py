from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelSetUpdate")


@attr.s(auto_attribs=True)
class LabelSetUpdate:
    """
    Attributes:
        exclusive_classes (Union[Unset, bool]):
        guideline (Union[Unset, str]):
        label (Union[Unset, str]):
        nature (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
    """

    exclusive_classes: Union[Unset, bool] = UNSET
    guideline: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    nature: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        exclusive_classes = self.exclusive_classes
        guideline = self.guideline
        label = self.label
        nature = self.nature
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if exclusive_classes is not UNSET:
            field_dict["exclusiveClasses"] = exclusive_classes
        if guideline is not UNSET:
            field_dict["guideline"] = guideline
        if label is not UNSET:
            field_dict["label"] = label
        if nature is not UNSET:
            field_dict["nature"] = nature
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exclusive_classes = d.pop("exclusiveClasses", UNSET)

        guideline = d.pop("guideline", UNSET)

        label = d.pop("label", UNSET)

        nature = d.pop("nature", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        label_set_update = cls(
            exclusive_classes=exclusive_classes,
            guideline=guideline,
            label=label,
            nature=nature,
            tags=tags,
        )

        return label_set_update
