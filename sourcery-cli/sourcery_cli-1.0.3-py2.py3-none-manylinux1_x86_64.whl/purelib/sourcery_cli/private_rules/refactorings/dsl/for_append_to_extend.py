from typing import List, Set, Type

from sourcery.conditions import CaptureConditions
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    LocalChangeOnException,
    LocalValueMissing,
    SemanticDifference,
)


class ForAppendToExtendProposer(  # pylint: disable=too-many-ancestors
    DSLProposer,
    DependencyConditions,
    TypeConditions,
    CaptureConditions,
    VariableUsageConditions,
):
    def create_code_changes(self) -> List[CodeChange]:
        # pylint: disable=line-too-long
        return [
            CodeChange(
                pattern="""
                    for ${target | not self.is_accessed_later(target)} in ${iter}:
                        ${L | self.has_list_type(L) and (self.is_name(L) or self.is_attribute(L)) }.append(${expr})
                """,
                replacement="""
                    ${L}.extend(${expr} for ${target} in ${iter})
                """,
                top_level_condition=lambda node: not self.contains_type_disallowed_in_generator(
                    node
                ),
            ),
            CodeChange(
                pattern="""
                    for ${target | not self.is_accessed_later(target)} in ${iter}:
                        if ${cond}:
                            ${L | (
                                self.has_list_type(L)
                                and not self.accesses_any_variables(cond, L)
                                and (self.is_name(L) or self.is_attribute(L))
                            )}.append(${expr})
                """,
                replacement="""
                    ${L}.extend(${expr} for ${target} in ${iter} if ${cond})
                """,
                top_level_condition=lambda node: not self.contains_type_disallowed_in_generator(
                    node
                ),
            ),
        ]

    def description(self) -> str:
        return "Replace a for append loop with list extend"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {LocalValueMissing, LocalChangeOnException}
