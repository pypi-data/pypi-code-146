from typing import Any, Dict, Type, TypeVar

import attr

from ..models.category_patch_status import CategoryPatchStatus

T = TypeVar("T", bound="CategoryPatch")


@attr.s(auto_attribs=True)
class CategoryPatch:
    """
    Attributes:
        status (CategoryPatchStatus): Status of the category
    """

    status: CategoryPatchStatus

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
        status = CategoryPatchStatus(d.pop("status"))

        category_patch = cls(
            status=status,
        )

        return category_patch
