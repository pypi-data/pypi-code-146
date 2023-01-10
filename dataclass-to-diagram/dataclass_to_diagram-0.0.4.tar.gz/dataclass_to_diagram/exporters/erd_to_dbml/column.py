from typing import Any, Final

from dataclass_to_diagram.models.erd import Column, Enum

from .note import note_to_dbml

TEMPLATE: Final[str] = "{name} {datatype} [{settings}]"


def _datatype_to_dbml(datatype: Any) -> str:
    if isinstance(datatype, Enum):
        out_datatype = datatype.name
    else:
        out_datatype = datatype
    return '"{0}"'.format(out_datatype)


def column_to_dbml(column: Column) -> str:
    settings: list[str] = []
    if column.note:
        settings.append(note_to_dbml(column.note, "column"))
    if column.is_pk:
        settings.append("pk")
    if column.can_be_null:
        settings.append("null")
    else:
        settings.append("not null")
    if column.is_unique:
        settings.append("unique")
    if column.default_value is not None:
        settings.append("default: '{0}'".format(column.default_value))
    if column.is_increment:
        settings.append("increment")

    return TEMPLATE.format(
        name=column.name,
        datatype=_datatype_to_dbml(column.datatype),
        settings=", ".join(settings),
    )
