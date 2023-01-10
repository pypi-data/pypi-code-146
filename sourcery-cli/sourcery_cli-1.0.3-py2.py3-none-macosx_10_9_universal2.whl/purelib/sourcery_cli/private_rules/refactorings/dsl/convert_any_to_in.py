from typing import List, Set, Type

from sourcery.analysis.typing.statement_types import UNKNOWN_TYPE
from sourcery.ast.nodes import Node
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import SIMPLIFY_ANY_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    NewException,
    ReturnValuesChangedOnException,
    SemanticDifference,
)


class ConvertAnyToInProposer(DSLProposer, DependencyConditions, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    any(
                        ${item} == ${
                            value|not self.have_common_accessed_variables(value, item)
                        }
                        for ${item} in ${collection|has_not_str_type}
                    )
                """,
                replacement="${value} in ${collection}",
            )
        ]

    def description(self) -> str:
        return SIMPLIFY_ANY_DESC

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged, ReturnValuesChangedOnException, NewException}

    def has_not_str_type(self, node: Node) -> bool:
        return not self.has_type(node, "str", UNKNOWN_TYPE)
