from typing import List, Set, Type

from sourcery.conditions.capture_conditions import CaptureConditions
from sourcery.conditions.name_conditions import NameConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import SWAP_VAR_DESC
from sourcery.semantic_equivalence.semantic_types import (
    LocalValueMissing,
    SemanticDifference,
)


class SwapVariableProposer(  # pylint: disable=too-many-ancestors
    DSLProposer, CaptureConditions, NameConditions, VariableUsageConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${
                        temp|self.is_name(temp) and not self.equals(a, temp)
                    } = ${a|self.is_name(a)}
                    ${a} = ${ b | (
                        self.is_name(b)
                        and not self.equals(b, a)
                        and not self.equals(b, temp)
                    )}
                    ${b} = ${temp|not self.is_accessed_later(temp)}
                """,
                replacement="""
                    ${a}, ${b} = ${b}, ${a}
                """,
            )
        ]

    def description(self) -> str:
        return SWAP_VAR_DESC

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {LocalValueMissing}
