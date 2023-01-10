from typing import Final

from dataclass_to_diagram.models.erd import ProjectDefinition

from .note import note_to_dbml

TEMPLATE: Final[
    str
] = """Project {project_name} {{
    {database_type}
    {note}
}}
"""

DATABASE_TYPE: Final[str] = "database_type: '{database_type}'"


def project_definition_to_dbml(proj_def: ProjectDefinition) -> str:
    if proj_def.note:
        note = note_to_dbml(proj_def.note, "short")
    else:
        note = ""

    return TEMPLATE.format(
        project_name=proj_def.project_name.replace(" ", "_"),
        database_type=DATABASE_TYPE.format(
            database_type=proj_def.database_type,
        ),
        note=note,
    )
