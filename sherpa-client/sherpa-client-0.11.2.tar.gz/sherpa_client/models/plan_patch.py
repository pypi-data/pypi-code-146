from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_plan import AnnotationPlan


T = TypeVar("T", bound="PlanPatch")


@attr.s(auto_attribs=True)
class PlanPatch:
    """
    Attributes:
        favorite (Union[Unset, bool]):
        label (Union[Unset, str]):
        parameters (Union[Unset, AnnotationPlan]):
        tags (Union[Unset, List[str]]):
    """

    favorite: Union[Unset, bool] = UNSET
    label: Union[Unset, str] = UNSET
    parameters: Union[Unset, "AnnotationPlan"] = UNSET
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        favorite = self.favorite
        label = self.label
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if label is not UNSET:
            field_dict["label"] = label
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotation_plan import AnnotationPlan

        d = src_dict.copy()
        favorite = d.pop("favorite", UNSET)

        label = d.pop("label", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, AnnotationPlan]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = AnnotationPlan.from_dict(_parameters)

        tags = cast(List[str], d.pop("tags", UNSET))

        plan_patch = cls(
            favorite=favorite,
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return plan_patch
