from typing import List

from sourcery.ast.nodes import Node
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import USE_LEN_DESC


class UseLenProposer(DSLProposer, LiteralConditions, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="sum(1 for ${item} in ${collection|has_sized_type})",
                replacement="len(${collection})",
            ),
            CodeChange(
                pattern="""
                    sum(${a|is_non_unit_int}
                    for ${item} in ${collection|has_sized_type})
                """,
                replacement="len(${collection})*${a}",
            ),
        ]

    def is_non_unit_int(self, node: Node) -> bool:
        return self.is_int_literal(node) and node.value != 1

    def description(self) -> str:
        return USE_LEN_DESC
