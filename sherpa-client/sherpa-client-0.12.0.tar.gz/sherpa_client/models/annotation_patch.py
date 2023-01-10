from typing import Any, Dict, Type, TypeVar

import attr

from ..models.annotation_patch_status import AnnotationPatchStatus

T = TypeVar("T", bound="AnnotationPatch")


@attr.s(auto_attribs=True)
class AnnotationPatch:
    """
    Attributes:
        status (AnnotationPatchStatus): Status of the category
    """

    status: AnnotationPatchStatus

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = AnnotationPatchStatus(d.pop("status"))

        annotation_patch = cls(
            status=status,
        )

        return annotation_patch
