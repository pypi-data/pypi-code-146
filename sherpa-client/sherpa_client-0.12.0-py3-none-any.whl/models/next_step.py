from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="NextStep")


@attr.s(auto_attribs=True)
class NextStep:
    """
    Attributes:
        hint (str):
        id (str):
    """

    hint: str
    id: str

    def to_dict(self) -> Dict[str, Any]:
        hint = self.hint
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "hint": hint,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hint = d.pop("hint")

        id = d.pop("id")

        next_step = cls(
            hint=hint,
            id=id,
        )

        return next_step
