from typing import List, Set, Type

from sourcery.ast import Node
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    SemanticDifference,
)


class RemoveRedundantSliceIndexProposer(DSLProposer, LiteralConditions):
    """Remove redundant initial index 0 of a slice.

    Similar refactoring: `remove-zero-from-range`
    """

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="${a}[0:${end_index?}:${step?|self.is_positive_int(step)}]",
                replacement="${a}[:${end_index}:${step}]",
            ),
            CodeChange(
                pattern="${a}[${start?}:len(${a}):${step?|self.is_positive_int(step)}]",
                replacement="${a}[${start}::${step}]",
            ),
        ]

    def description(self) -> str:
        return "Replace a[0:x] with a[:x] and a[x:len(a)] with a[x:]"

    def is_positive_int(self, node: Node) -> bool:
        return self.is_int_literal(node) and node.value > 0

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged}
