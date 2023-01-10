from typing import List

from lib.version import PythonVersion
from sourcery.conditions.import_conditions import (
    AddImportPostCondition,
    ImportConditions,
)
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class PathReadProposer(DSLProposer, ImportConditions):
    """Proposes :py:mod:`pathlib` reads replacing file reads."""

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    with open(${path}) as ${f}:
                        ${contents} = ${f}.read()
                """,
                replacement="""
                    ${contents} = ${
                        self.pathlib_path().node_for_import_name()
                    }(${path}).read_text()
                """,
                add_imports_post_condition=self.pathlib_path(),
            )
        ]

    def pathlib_path(self) -> AddImportPostCondition:
        return self.upsert_import("pathlib.Path")

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=5)

    def description(self) -> str:
        return "Simplify basic file reads with `pathlib`"
