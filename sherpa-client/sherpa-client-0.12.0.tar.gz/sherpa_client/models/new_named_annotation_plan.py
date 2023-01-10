from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_plan import AnnotationPlan


T = TypeVar("T", bound="NewNamedAnnotationPlan")


@attr.s(auto_attribs=True)
class NewNamedAnnotationPlan:
    """
    Attributes:
        label (str):
        parameters (AnnotationPlan):
        tags (Union[Unset, List[str]]):
    """

    label: str
    parameters: "AnnotationPlan"
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        parameters = self.parameters.to_dict()

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "parameters": parameters,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotation_plan import AnnotationPlan

        d = src_dict.copy()
        label = d.pop("label")

        parameters = AnnotationPlan.from_dict(d.pop("parameters"))

        tags = cast(List[str], d.pop("tags", UNSET))

        new_named_annotation_plan = cls(
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return new_named_annotation_plan
