import typing
from typing import List

from sourcery.ast import Name, Node
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    FunctionCallsOnException,
    NewException,
    ReturnValuesChangedOnException,
    SemanticDifference,
)


class MaxMinDefaultProposer(DSLProposer, TypeConditions, DependencyConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${
                        max_min | is_max_min
                    }(${iterable}) if ${iterable | has_sized_type} else ${
                        default|not self.writes_any_variables(default)
                    }
                """,
                replacement="""
                    ${max_min}(${iterable}, default=${default})
                """,
            ),
            CodeChange(
                pattern="""
                    ${
                        max_min | is_max_min
                    }(${calculation} for ${thing} in ${iterable}) if ${
                        iterable | has_sized_type
                    } else ${default|not self.writes_any_variables(default)}
                """,
                replacement="""
                    ${max_min}(
                        (${calculation} for ${thing} in ${iterable}),
                        default=${default}
                    )
                """,
            ),
        ]

    def is_max_min(self, node: Node) -> bool:
        return isinstance(node, Name) and node.id in ["max", "min"]

    def description(self) -> str:
        return "Use max/min default argument instead of if statement"

    def expected_semantic_differences(
        self,
    ) -> typing.Set[typing.Type[SemanticDifference]]:
        return {NewException, ReturnValuesChangedOnException, FunctionCallsOnException}
