from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.classification_options import ClassificationOptions


T = TypeVar("T", bound="ConfigPatchOptions")


@attr.s(auto_attribs=True)
class ConfigPatchOptions:
    """
    Attributes:
        classification (Union[Unset, ClassificationOptions]):
        collaborative_annotation (Union[Unset, bool]):
        image (Union[Unset, str]):
        label (Union[Unset, str]):
        metafacets (Union[Unset, List[str]]):
    """

    classification: Union[Unset, "ClassificationOptions"] = UNSET
    collaborative_annotation: Union[Unset, bool] = UNSET
    image: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    metafacets: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        classification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.classification, Unset):
            classification = self.classification.to_dict()

        collaborative_annotation = self.collaborative_annotation
        image = self.image
        label = self.label
        metafacets: Union[Unset, List[str]] = UNSET
        if not isinstance(self.metafacets, Unset):
            metafacets = self.metafacets

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if classification is not UNSET:
            field_dict["classification"] = classification
        if collaborative_annotation is not UNSET:
            field_dict["collaborativeAnnotation"] = collaborative_annotation
        if image is not UNSET:
            field_dict["image"] = image
        if label is not UNSET:
            field_dict["label"] = label
        if metafacets is not UNSET:
            field_dict["metafacets"] = metafacets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.classification_options import ClassificationOptions

        d = src_dict.copy()
        _classification = d.pop("classification", UNSET)
        classification: Union[Unset, ClassificationOptions]
        if isinstance(_classification, Unset):
            classification = UNSET
        else:
            classification = ClassificationOptions.from_dict(_classification)

        collaborative_annotation = d.pop("collaborativeAnnotation", UNSET)

        image = d.pop("image", UNSET)

        label = d.pop("label", UNSET)

        metafacets = cast(List[str], d.pop("metafacets", UNSET))

        config_patch_options = cls(
            classification=classification,
            collaborative_annotation=collaborative_annotation,
            image=image,
            label=label,
            metafacets=metafacets,
        )

        return config_patch_options
