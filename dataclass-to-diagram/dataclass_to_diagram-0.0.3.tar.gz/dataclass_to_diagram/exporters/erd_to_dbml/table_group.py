"""Преобразование групп таблиц."""

from typing import Final, Iterable

from dataclass_to_diagram.models.erd.erd import Table, TableGroup

TEMPLATE: Final[
    str
] = """TableGroup {name} {{
{tables}
}}
"""


def _table_names(tables: Iterable[Table]):
    tables_list: list[str] = ["    {0}".format(table.name) for table in tables]
    return "\n".join(tables_list)


def table_group_to_dbml(table_group: TableGroup) -> str:
    """Преобразование групп таблиц."""
    return TEMPLATE.format(
        name=table_group.name,
        tables=_table_names(table_group.tables),
    )
