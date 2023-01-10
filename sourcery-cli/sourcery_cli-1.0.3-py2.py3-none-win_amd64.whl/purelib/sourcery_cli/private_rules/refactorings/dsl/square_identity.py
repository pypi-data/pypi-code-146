from typing import List

from sourcery.ast import Constant, Node, is_annotation
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import SQUARE_DESC


class SquareIdentityProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${x} * ${x | is_suitable_value}
                """,
                replacement="""
                    ${x} ** 2
                """,
            )
        ]

    def description(self) -> str:
        return SQUARE_DESC

    def is_suitable_value(self, node: Node) -> bool:
        return (
            self.has_numeric_type(node)
            and not is_annotation(node)
            and not isinstance(node, Constant)
        )
