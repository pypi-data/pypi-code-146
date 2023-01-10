from typing import List, Set, Type

from sourcery.ast import Node
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import USE_COUNT_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    SemanticDifference,
    StdOutChangedOnException,
)


class UseCountProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    sum(${item} == ${value|self.can_convert_to_count(value, collection)}
                    for ${item} in ${collection})
                """,
                replacement="${collection}.count(${value})",
            )
        ]

    def description(self) -> str:
        return USE_COUNT_DESC

    def can_convert_to_count(self, value: Node, node: Node) -> bool:
        return hash(value) != hash(node) and (
            self.has_list_type(node)
            or self.has_str_type(node)
            and self.has_str_type(value)
        )

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {ExceptionRemoved, StdOutChangedOnException}
