from typing import Any, Callable, Dict, Generator

from semantic_version import SimpleSpec, Version


class SemVerSpec(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], "SemVerSpec"], None, None]:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(examples=["^0.0.1", "==1.5.3", ">=2.1.0,<3.0.0"])

    @classmethod
    def validate(cls, v: str) -> "SemVerSpec":
        if not isinstance(v, str):
            raise ValueError("invalid semantic versioning spec")

        try:
            SimpleSpec(v)
        except ValueError:
            raise ValueError("invalid semantic versioning spec")

        return cls(v)

    def __contains__(self, item: object) -> bool:
        try:
            return Version(item) in SimpleSpec(self)
        except:  # noqa: E722
            return False
