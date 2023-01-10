from typing import List

from sourcery.ast.ast import invert_condition  # pylint: disable=unused-import
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class BooleanIfExpIdentityProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    True if ${cond} else False
                """,
                replacement="""
                    bool(${cond})
                """,
            ),
            CodeChange(
                pattern="""
                    False if ${cond} else True
                """,
                replacement="""
                    bool(${invert_condition(cond)})
                """,
            ),
        ]

    def description(self) -> str:
        return "Simplify boolean if expression"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
