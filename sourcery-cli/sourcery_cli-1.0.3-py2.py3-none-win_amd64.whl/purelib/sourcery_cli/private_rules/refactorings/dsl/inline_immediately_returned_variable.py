"""Refactoring to inline variables."""
from typing import List

from sourcery.conditions import CaptureConditions, DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class InlineImmediatelyReturnedVariableProposer(
    DSLProposer, DependencyConditions, CaptureConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${var | not self.writes_to_global_state(var) and self.is_name(var)}: !!! = ${expr}
                    return ${var}
                """,
                replacement="""
                    return ${expr}
                """,
            ),
        ]

    def description(self) -> str:
        return "Inline variable that is immediately returned"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
