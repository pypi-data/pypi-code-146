"""Преобразование всей схемы БД."""

# pyright: reportShadowedImports=false

from typing import Final, Iterable

from dataclass_to_diagram.models.erd import (
    Database,
    Enum,
    ProjectDefinition,
    Relation,
    Table,
)
from dataclass_to_diagram.models.erd.erd import TableGroup

from .enum import enum_to_dbml
from .project_definition import project_definition_to_dbml
from .relation import relation_to_dbml
from .table import table_to_dbml
from .table_group import table_group_to_dbml

TEMPLATE: Final[
    str
] = """
{project_definition}{enums}{tables}{relations}{table_groups}
"""
NOT_EXIST: Final[str] = ""
LIST_NEW_LINE_SEPARATED: Final[str] = "\n{0}"


def _proj_def_to_dbml(proj_def: ProjectDefinition | None) -> str:
    if proj_def is None:
        return NOT_EXIST
    return "{0}".format(project_definition_to_dbml(proj_def))


def _enums_to_dbml(enums: Iterable[Enum] | None) -> str:
    if enums is None:
        return NOT_EXIST
    enums_list: list[str] = [enum_to_dbml(enum) for enum in enums]
    enums_str = "\n".join(enums_list)
    return LIST_NEW_LINE_SEPARATED.format(enums_str)


def _tables_to_dbml(tables: Iterable[Table] | None) -> str:
    if tables is None:
        return NOT_EXIST
    tables_list: list[str] = [table_to_dbml(table) for table in tables]
    tables_str = "\n".join(tables_list)
    return LIST_NEW_LINE_SEPARATED.format(tables_str)


def _relations_to_dbml(relations: Iterable[Relation] | None) -> str:
    if relations is None:
        return NOT_EXIST
    relations_list: list[str] = [relation_to_dbml(rel) for rel in relations]
    relations_str = "\n".join(relations_list)
    return LIST_NEW_LINE_SEPARATED.format(relations_str)


def _table_groups_to_dbml(table_groups: Iterable[TableGroup] | None) -> str:
    if table_groups is None:
        return NOT_EXIST
    tg_list: list[str] = [table_group_to_dbml(tg) for tg in table_groups]
    tg_str: str = "\n".join(tg_list)
    return LIST_NEW_LINE_SEPARATED.format(tg_str)


def database_to_dbml(database: Database) -> str:
    """Преобразование всей схемы БД."""
    return TEMPLATE.format(
        project_definition=_proj_def_to_dbml(database.project_definition),
        enums=_enums_to_dbml(database.enums),
        tables=_tables_to_dbml(database.tables),
        relations=_relations_to_dbml(database.relations),
        table_groups=_table_groups_to_dbml(database.table_groups),
    )
