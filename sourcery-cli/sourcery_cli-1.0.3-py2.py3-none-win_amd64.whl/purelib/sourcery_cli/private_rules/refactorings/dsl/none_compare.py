from typing import List

from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import NONE_COMP_DESC
from sourcery.rules.private.refactorings.dsl.utils import not_in_equality_dunder


class NoneCompareProposer(DSLProposer, LiteralConditions):
    """Use x is None rather than x == None.

    When defining custom classes with the equality dunder method, this should not
    be proposed
    """

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a | not self.is_literal(a)} == None
                """,
                replacement="""
                    ${a} is None
                """,
                top_level_condition=not_in_equality_dunder,
            )
        ]

    def description(self) -> str:
        return NONE_COMP_DESC
