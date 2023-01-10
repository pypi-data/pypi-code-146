from typing import List

from sourcery import ast
from sourcery.conditions.capture_conditions import CaptureConditions
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import TERNARY_TO_IF_EXP_DESC


# pylint: disable=too-many-ancestors
class TernaryToIfExpressionProposer(
    DSLProposer, CaptureConditions, LiteralConditions, TypeConditions
):
    """The preferred if-else expression replaces the ternary boolean expression.

    `a and b or c` -> `b if a else c`
    """

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    (
                        ${a}
                        and ${b | is_truthy_literal}
                        or ${c | not self.is_boolop(c) and not self.has_bool_type(c)}
                    )
                """,
                replacement="""
                    ${b} if ${a} else ${c}
                """,
                top_level_condition=lambda node: isinstance(
                    node.parent, (ast.Assign, ast.Return)
                ),
            )
        ]

    def description(self) -> str:
        return TERNARY_TO_IF_EXP_DESC
