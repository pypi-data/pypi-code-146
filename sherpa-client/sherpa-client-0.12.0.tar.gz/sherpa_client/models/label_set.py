from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelSet")


@attr.s(auto_attribs=True)
class LabelSet:
    """
    Attributes:
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        exclusive_classes (Union[Unset, bool]):
        guideline (Union[Unset, str]):
        label (Union[Unset, str]):
        modified_at (Union[Unset, str]):
        name (Union[Unset, str]):
        nature (Union[Unset, str]):
        tags (Union[Unset, List[str]]):
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    exclusive_classes: Union[Unset, bool] = False
    guideline: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    modified_at: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    nature: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at
        created_by = self.created_by
        exclusive_classes = self.exclusive_classes
        guideline = self.guideline
        label = self.label
        modified_at = self.modified_at
        name = self.name
        nature = self.nature
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if exclusive_classes is not UNSET:
            field_dict["exclusiveClasses"] = exclusive_classes
        if guideline is not UNSET:
            field_dict["guideline"] = guideline
        if label is not UNSET:
            field_dict["label"] = label
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if nature is not UNSET:
            field_dict["nature"] = nature
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        exclusive_classes = d.pop("exclusiveClasses", UNSET)

        guideline = d.pop("guideline", UNSET)

        label = d.pop("label", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        name = d.pop("name", UNSET)

        nature = d.pop("nature", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        label_set = cls(
            created_at=created_at,
            created_by=created_by,
            exclusive_classes=exclusive_classes,
            guideline=guideline,
            label=label,
            modified_at=modified_at,
            name=name,
            nature=nature,
            tags=tags,
        )

        return label_set
