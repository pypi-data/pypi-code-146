from typing import List, Set, Type

from sourcery.ast import Node, Tuple, get_nodes
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import ISINSTANCE_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    LocalChangeOnException,
    SemanticDifference,
    StdOutChangedOnException,
)

# pylint: disable=line-too-long


class MergeIsinstanceProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="... or isinstance(${i}, ${j}) or isinstance(${i}, ${k}) or ...",
                replacement="... or isinstance(${i}, ${self.merge_values(j, k)}) or ...",
            )
        ]

    def description(self) -> str:
        return ISINSTANCE_DESC

    def merge_values(self, first, second) -> Node:
        comparisons = get_nodes(first) + get_nodes(second)
        return Tuple(tuple(comparisons))

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {StdOutChangedOnException, ExceptionRemoved, LocalChangeOnException}
