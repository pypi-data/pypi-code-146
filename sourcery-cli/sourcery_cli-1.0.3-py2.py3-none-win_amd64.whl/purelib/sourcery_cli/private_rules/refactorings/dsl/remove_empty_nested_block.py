from typing import List, Set, Type

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import REMOVE_EMPTY_NESTED_BLOCK
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    LocalValueMissing,
    SemanticDifference,
    StdOutChangedOnException,
)


class RemoveEmptyNestedBlockProposer(
    DSLProposer, DependencyConditions, VariableUsageConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    for ${item|not self.is_accessed_later(item)} in ${
                        collection|not self.writes_any_variables(collection)
                    }:
                      pass
                """,
                replacement="",
            ),
            CodeChange(
                pattern="""
                    if ${test|not self.writes_any_variables(test)}:
                      pass
                """,
                replacement="",
            ),
        ]

    def description(self) -> str:
        return REMOVE_EMPTY_NESTED_BLOCK

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {LocalValueMissing, ExceptionRemoved, StdOutChangedOnException}
