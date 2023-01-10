from typing import List, Set, Type

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    SemanticDifference,
)


class SimplifySubstringSearchProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        find_code_changes = [
            CodeChange(
                pattern="${text|has_str_type}.find(${substr}) " + condition,
                replacement="${substr} in ${text}",
            )
            for condition in ["!= -1", ">= 0", "> -1"]
        ]
        find_code_changes.append(
            CodeChange(
                pattern="${text|has_str_type}.find(${substr}) == -1",
                replacement="${substr} not in ${text}",
            )
        )

        count_code_changes = [
            CodeChange(
                pattern="${text|has_str_type}.count(${substr}) " + condition,
                replacement="${substr} in ${text}",
            )
            for condition in ["!= 0", ">= 1", "> 0"]
        ]
        count_code_changes.append(
            CodeChange(
                pattern="${text|has_str_type}.count(${substr}) == 0",
                replacement="${substr} not in ${text}",
            )
        )

        return find_code_changes + count_code_changes

    def description(self) -> str:
        return "Simplify finding if substrings are present by using `in`"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged}
