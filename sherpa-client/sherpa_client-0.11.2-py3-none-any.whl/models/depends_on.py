from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="DependsOn")


@attr.s(auto_attribs=True)
class DependsOn:
    """
    Attributes:
        auto (bool):
        groups (List[str]):
        hint (str):
        steps (List[str]):
    """

    auto: bool
    groups: List[str]
    hint: str
    steps: List[str]

    def to_dict(self) -> Dict[str, Any]:
        auto = self.auto
        groups = self.groups

        hint = self.hint
        steps = self.steps

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "auto": auto,
                "groups": groups,
                "hint": hint,
                "steps": steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        auto = d.pop("auto")

        groups = cast(List[str], d.pop("groups"))

        hint = d.pop("hint")

        steps = cast(List[str], d.pop("steps"))

        depends_on = cls(
            auto=auto,
            groups=groups,
            hint=hint,
            steps=steps,
        )

        return depends_on
