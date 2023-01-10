from typing import List, Set

from sourcery.analysis.typing.exception_types import parents_of_exception
from sourcery.ast.nodes import Expression, Tuple
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class RemoveRedundantExceptionProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    try:
                        ${statements+}
                    $except{excepts*}
                    except ${exc|self.contains_subclass_exception(exc)} as ${exception_name?}:
                        ${exc_statements+}
                    $except{excepts_after*}
                    else:
                        ${else_statements*}
                    finally:
                        ${finally_statements*}
                """,
                replacement="""
                    try:
                        ${statements}
                    $except{excepts}
                    except ${self.cleaned_exceptions(exc)} as ${exception_name}:
                        ${exc_statements}
                    $except{excepts_after}
                    else:
                        ${else_statements}
                    finally:
                        ${finally_statements}
                """,
            ),
        ]

    def description(self) -> str:
        return "Remove redundant exceptions from an except clause"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def contains_subclass_exception(self, exceptions: Expression) -> bool:
        return (
            bool(self._exceptions_with_parents_present(exceptions))
            if isinstance(exceptions, Tuple)
            else False
        )

    def _exceptions_with_parents_present(self, exceptions: Tuple) -> Set[str]:
        exception_strs = {ex.unparse() for ex in exceptions.elts}
        return {
            ex
            for ex in exception_strs
            if set(parents_of_exception(ex)).intersection(exception_strs)
        }

    def cleaned_exceptions(self, exceptions: Tuple) -> Tuple:
        exceptions_with_parents = self._exceptions_with_parents_present(exceptions)
        cleaned_exceptions = tuple(
            ex for ex in exceptions.elts if ex.unparse() not in exceptions_with_parents
        )

        return Tuple(elts=cleaned_exceptions)
