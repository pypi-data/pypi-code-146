from typing import Final

from dataclass_to_diagram.models.erd import Table

from .column import column_to_dbml
from .note import note_to_dbml

TEMPLATE: Final[
    str
] = """Table {name} {{
{columns}
{note}
}}
"""


def table_to_dbml(table: Table) -> str:
    columns = [column_to_dbml(col) for col in table.columns]
    columns = ["    {0}".format(col) for col in columns]
    if table.note:
        note = note_to_dbml(table.note)
        note = "    {0}".format(note)
    else:
        note = ""

    return TEMPLATE.format(
        name=table.name,
        columns="\n".join(columns),
        note=note,
    )
