import copy
from typing import Iterator, List

from lib.version import PythonVersion
from sourcery.ast import Call, Expression, Tuple
from sourcery.conditions.import_conditions import (
    AddImportPostCondition,
    ImportConditions,
)
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class UseContextlibSuppressProposer(DSLProposer, ImportConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    try:
                        ${statements+}
                    except ${exceptions} as ${exception_name?}:
                        pass
                """,
                replacement="""
                    with ${self.suppress_function(exceptions)}:
                        ${statements}
                """,
                add_imports_post_condition=self.contextlib_suppress(),
            )
        ]

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=4)

    def description(self) -> str:
        return "Use `contextlib`'s `suppress` method to silence an error"

    def suppress_function(self, exceptions: Expression) -> Call:
        node_for_contextlib = self.contextlib_suppress().node_for_import_name()
        exception_args = tuple(self.get_exception_names(exceptions))
        return Call(node_for_contextlib, exception_args)

    def contextlib_suppress(self) -> AddImportPostCondition:
        return self.upsert_import("contextlib.suppress")

    def get_exception_names(self, exceptions: Expression) -> Iterator[Expression]:
        if not isinstance(exceptions, Tuple):
            yield copy.deepcopy(exceptions)
        else:
            yield from map(copy.deepcopy, exceptions.elts)  # type: ignore
