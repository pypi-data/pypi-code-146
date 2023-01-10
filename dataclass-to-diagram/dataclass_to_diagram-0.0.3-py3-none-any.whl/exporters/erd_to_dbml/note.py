"""Строковое представление для заметок."""

from typing import Final, Literal

from dataclass_to_diagram.models.erd import Note

LONG: Final[
    str
] = """Note {{
   '''{content}'''
}}
"""

SHORT: Final[str] = "Note: '''{content}'''"

COLUMN: str = "note: '''{content}'''"


def note_to_dbml(
    note: Note,
    view: Literal["long", "short", "column"] = "short",
) -> str:
    match view:
        case "long":
            return LONG.format(content=note.note_content)
        case "short":
            return SHORT.format(content=note.note_content)
        case "column":
            return COLUMN.format(content=note.note_content)
        case _:
            raise ValueError("Unknown view: {0}".format(view))
