from typing import Any, Callable, Dict, Generator


class StrCommand(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], "StrCommand"], None, None]:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        pass

    @classmethod
    def validate(cls, v: str) -> "StrCommand":
        if isinstance(v, bool):
            return StrCommand(str(v).lower())

        if isinstance(v, dict) or isinstance(v, list):
            raise ValueError("must be a string")

        as_str = str(v)
        if len(as_str) == 0:
            raise ValueError("ensure command has at least 1 characters")

        return StrCommand(as_str)
