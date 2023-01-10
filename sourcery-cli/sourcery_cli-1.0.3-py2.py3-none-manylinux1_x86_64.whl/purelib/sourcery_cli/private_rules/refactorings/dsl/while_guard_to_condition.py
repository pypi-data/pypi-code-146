from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class WhileGuardToConditionProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    while ${cond_a}:
                        if ${cond_b}:
                            break
                        ${statements*}
                """,
                replacement="""
                    while ${cond_a} and not ${cond_b}:
                        ${statements}
                """,
            )
        ]

    def description(self) -> str:
        return "Move a guard clause in a while statement's body into its test"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
