from typing import List, Set, Type

from sourcery.ast import Node, parent_coerces_to_bool
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    FunctionCallsOnException,
    ReturnValuesChangedOnException,
    SemanticDifference,
)


class SimplifyLenComparisonProposer(DSLProposer, TypeConditions):
    """Simplify bool expressions to determine whether a sequence is empty.

    Replace various expressions comparing the length to 0 or 1 with evaluating
    the sequence as bool.
    """

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="len(${seq|has_sized_type}) == 0",
                replacement="not ${seq}",
            ),
            CodeChange(
                pattern="len(${seq|has_sized_type}) < 1",
                replacement="not ${seq}",
            ),
            CodeChange(
                pattern="len(${seq|is_valid_and_coerces_to_bool}) > 0",
                replacement="${seq}",
            ),
            CodeChange(
                pattern="len(${seq|is_valid_and_coerces_to_bool}) != 0",
                replacement="${seq}",
            ),
            CodeChange(
                pattern="len(${seq|is_valid_and_coerces_to_bool}) >= 1",
                replacement="${seq}",
            ),
            CodeChange(
                pattern="len(${seq|has_sized_type}) >= 0",
                replacement="True",
            ),
            CodeChange(
                pattern="len(${seq|has_sized_type}) < 0",
                replacement="False",
            ),
        ]

    def description(self) -> str:
        return "Simplify sequence length comparison"

    def is_valid_and_coerces_to_bool(self, node: Node):
        return self.has_sized_type(node) and parent_coerces_to_bool(node.parent.parent)

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {
            ExceptionRemoved,
            FunctionCallsOnException,
            ReturnValuesChangedOnException,
        }
