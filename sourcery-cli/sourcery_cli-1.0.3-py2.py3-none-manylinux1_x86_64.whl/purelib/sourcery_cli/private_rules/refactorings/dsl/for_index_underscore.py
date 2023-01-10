from typing import List, Set, Type

from typing_extensions import TypeGuard

from sourcery.ast import Name, Node
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    LocalChangeOnException,
    LocalValueMissing,
    SemanticDifference,
)


class ForIndexUnderscoreProposer(
    DSLProposer, DependencyConditions, VariableUsageConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        for_code_change = [
            CodeChange(
                pattern="""
                    for ${item|self._suitable_value(item)} in ${collection}:
                      ${statements+|not self.accesses_any_variables(statements, item)}
                """,
                replacement="""
                    for _ in ${collection}:
                      ${statements}
                """,
            )
        ]
        comprehension_pattern = (
            "${value|not self.accesses_any_variables(value, item)} "
            "for ${item|self._suitable_target(item)} in ${collection} "
            "if ${condition?|not self.accesses_any_variables(condition, item)}"
        )
        comprehension_replacement = "${value} for _ in ${collection} if ${condition}"
        comp_changes = [
            CodeChange(
                pattern=f"""
                    [{comprehension_pattern}]
                """,
                replacement=f"""
                    [{comprehension_replacement}]
                """,
            ),
            CodeChange(
                pattern=f"""
                    ({comprehension_pattern})
                """,
                replacement=f"""
                    ({comprehension_replacement})
                """,
            ),
            CodeChange(
                pattern=f"""
                    {{{comprehension_pattern}}}
                """,
                replacement=f"""
                    {{{comprehension_replacement}}}
                """,
            ),
        ]

        return comp_changes + for_code_change

    def _suitable_value(self, node: Node) -> TypeGuard[Name]:
        return self._suitable_target(node) and not self.is_accessed_later(node)

    def _suitable_target(self, node: Node) -> TypeGuard[Name]:
        return isinstance(node, Name) and not node.id.startswith("_")

    def description(self) -> str:
        return "Replace unused for index with underscore"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        # StdOutChanged here is due to the pattern generation printing out
        # the generator.
        return {LocalValueMissing, LocalChangeOnException}
