from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..models.annotated_doc_category_creation_mode import AnnotatedDocCategoryCreationMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotated_doc_category_properties import AnnotatedDocCategoryProperties


T = TypeVar("T", bound="AnnotatedDocCategory")


@attr.s(auto_attribs=True)
class AnnotatedDocCategory:
    """A document category

    Attributes:
        label_name (str): Label name
        creation_mode (Union[Unset, AnnotatedDocCategoryCreationMode]): Creation mode
        label (Union[Unset, str]): Human-friendly label
        label_id (Union[Unset, str]): External label identifier
        properties (Union[Unset, AnnotatedDocCategoryProperties]): Additional properties
        score (Union[Unset, float]): Score of the category
    """

    label_name: str
    creation_mode: Union[Unset, AnnotatedDocCategoryCreationMode] = UNSET
    label: Union[Unset, str] = UNSET
    label_id: Union[Unset, str] = UNSET
    properties: Union[Unset, "AnnotatedDocCategoryProperties"] = UNSET
    score: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label_name = self.label_name
        creation_mode: Union[Unset, str] = UNSET
        if not isinstance(self.creation_mode, Unset):
            creation_mode = self.creation_mode.value

        label = self.label
        label_id = self.label_id
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        score = self.score

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labelName": label_name,
            }
        )
        if creation_mode is not UNSET:
            field_dict["creationMode"] = creation_mode
        if label is not UNSET:
            field_dict["label"] = label
        if label_id is not UNSET:
            field_dict["labelId"] = label_id
        if properties is not UNSET:
            field_dict["properties"] = properties
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotated_doc_category_properties import AnnotatedDocCategoryProperties

        d = src_dict.copy()
        label_name = d.pop("labelName")

        _creation_mode = d.pop("creationMode", UNSET)
        creation_mode: Union[Unset, AnnotatedDocCategoryCreationMode]
        if isinstance(_creation_mode, Unset):
            creation_mode = UNSET
        else:
            creation_mode = AnnotatedDocCategoryCreationMode(_creation_mode)

        label = d.pop("label", UNSET)

        label_id = d.pop("labelId", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, AnnotatedDocCategoryProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = AnnotatedDocCategoryProperties.from_dict(_properties)

        score = d.pop("score", UNSET)

        annotated_doc_category = cls(
            label_name=label_name,
            creation_mode=creation_mode,
            label=label,
            label_id=label_id,
            properties=properties,
            score=score,
        )

        return annotated_doc_category
