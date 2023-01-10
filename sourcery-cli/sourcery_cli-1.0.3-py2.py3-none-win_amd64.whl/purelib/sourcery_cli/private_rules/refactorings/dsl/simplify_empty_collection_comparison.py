from typing import List, Set, Type

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    FunctionCallsChanged,
    SemanticDifference,
)


class SimplifyEmptyCollectionComparisonProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a | has_str_type} == ""
                """,
                replacement="""
                    not ${a}
                """,
            ),
            CodeChange(
                pattern="""
                    ${a | has_tuple_type} == ()
                """,
                replacement="""
                    not ${a}
                """,
            ),
            CodeChange(
                pattern="""
                    ${a | has_list_type} == []
                """,
                replacement="""
                    not ${a}
                """,
            ),
            CodeChange(
                pattern="""
                    ${a | has_dict_type} == {}
                """,
                replacement="""
                    not ${a}
                """,
            ),
            CodeChange(
                pattern="""
                    ${a | has_set_type} == set()
                """,
                replacement="""
                    not ${a}
                """,
            ),
        ]

    def description(self) -> str:
        return "Replaces an empty collection equality with a boolean operation"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {FunctionCallsChanged}
