from typing import Final

from dataclass_to_diagram.models.erd import Relation

TEMPLATE: Final[
    str
] = """Ref: {table1}.{col1} {relation} {table2}.{col2} [{config}]
"""


def relation_to_dbml(relation: Relation) -> str:
    config: list[str] = []
    if relation.config_update is not None:
        config_update = "update: {0}".format(relation.config_update)
        config.append(config_update)
    if relation.config_delete is not None:
        config_delete = "delete: {0}".format(relation.config_delete)
        config.append(config_delete)
    return TEMPLATE.format(
        table1=relation.column1.table.name,
        col1=relation.column1.name,
        relation=relation.relation,
        table2=relation.column2.table.name,
        col2=relation.column2.name,
        config=", ".join(config),
    )
