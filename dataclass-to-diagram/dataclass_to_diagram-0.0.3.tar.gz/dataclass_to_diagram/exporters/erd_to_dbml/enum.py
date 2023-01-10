"""Перечисление в DBML."""

from typing import Final

from dataclass_to_diagram.models.erd import Enum, EnumValue

from .note import note_to_dbml

ENUM_VALUE: Final[str] = "    {name}{note}"
ENUM: Final[
    str
] = """enum "{name}" {{
{values}
}}
"""


def _enum_value_to_dbml(enum_value: EnumValue) -> str:
    note: str = ""
    if enum_value.note is not None:
        note_dbml = note_to_dbml(enum_value.note, "column")
        note = " [{0}]".format(note_dbml)
    return ENUM_VALUE.format(
        name=enum_value.enum_value,
        note=note,
    )


def enum_to_dbml(enum: Enum) -> str:
    """Перечисление в DBML."""
    enum_values: list[str] = [
        _enum_value_to_dbml(ev) for ev in enum.enum_values
    ]
    return ENUM.format(
        name=enum.name,
        values="\n".join(enum_values),
    )
