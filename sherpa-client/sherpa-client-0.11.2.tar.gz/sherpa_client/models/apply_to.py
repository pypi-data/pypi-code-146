from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ApplyTo")


@attr.s(auto_attribs=True)
class ApplyTo:
    """
    Attributes:
        path (str):
    """

    path: str

    def to_dict(self) -> Dict[str, Any]:
        path = self.path

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "path": path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        apply_to = cls(
            path=path,
        )

        return apply_to
