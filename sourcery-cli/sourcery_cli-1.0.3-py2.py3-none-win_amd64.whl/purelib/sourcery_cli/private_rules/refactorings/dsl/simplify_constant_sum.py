from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import SIMPLIFY_SUM_DESC


class SimplifyConstantSumProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="sum(1 for ${item} in ${collection} if ${test})",
                replacement="""
                    sum(bool(${test})
                    for ${item} in ${collection})
                """,
            ),
        ]

    def description(self) -> str:
        return SIMPLIFY_SUM_DESC
