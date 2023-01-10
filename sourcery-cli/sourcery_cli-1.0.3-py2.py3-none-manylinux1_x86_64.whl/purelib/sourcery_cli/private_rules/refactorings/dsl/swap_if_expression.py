from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class SwapIfExpressionProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a} if not ${cond} else ${b}
                """,
                replacement="""
                    ${b} if ${cond} else ${a}
                """,
            )
        ]

    def description(self) -> str:
        return "Swap if/else branches of if expression to remove negation"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
