from typing import List, Set, Type

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import SIMPLIFY_STR_LEN_COMP
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    ReturnValuesChanged,
    ReturnValuesChangedOnException,
    SemanticDifference,
)


class SimplifyStrLenComparisonProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    len(${s | has_str_type}) == 0
                """,
                replacement="""
                    ${s} == ""
                """,
            ),
            CodeChange(
                pattern="""
                    len(${s | has_str_type}) != 0
                """,
                replacement="""
                    ${s} != ""
                """,
            ),
            CodeChange(
                pattern="""
                    len(${s | has_str_type}) > 0
                """,
                replacement="""
                    ${s} != ""
                """,
            ),
        ]

    def description(self) -> str:
        return SIMPLIFY_STR_LEN_COMP

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {ReturnValuesChanged, ReturnValuesChangedOnException, ExceptionRemoved}
