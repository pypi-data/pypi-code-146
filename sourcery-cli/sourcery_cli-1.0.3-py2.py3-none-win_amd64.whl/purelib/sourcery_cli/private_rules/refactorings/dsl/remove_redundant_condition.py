from typing import List

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class RemoveRedundantConditionProposer(DSLProposer, DependencyConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            # Function calls are considered writes to the global state, so this
            # refactoring can't be called for functional conditions.
            # Future improvements include extracting the conditional function ahead of
            # the assignment or analyzing `cond` for purity (a pure function could be
            # dropped).
            CodeChange(
                pattern="""
                    ${x} = ${var} if ${
                        cond | not self.writes_any_variables(cond)
                    } else ${var}
                """,
                replacement="""
                    ${x} = ${var}
                """,
            ),
        ]

    def description(self) -> str:
        return "Remove an unnecessary condition used during variable assignment"
