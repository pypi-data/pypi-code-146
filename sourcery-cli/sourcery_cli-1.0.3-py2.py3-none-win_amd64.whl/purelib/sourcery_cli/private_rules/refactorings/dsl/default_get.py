import typing
from typing import List

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import DEFAULT_GET_DESC
from sourcery.semantic_equivalence.semantic_types import (
    FunctionCallsOnException,
    LocalChangeOnException,
    NewException,
    SemanticDifference,
)


class DefaultGetProposer(DSLProposer, TypeConditions, DependencyConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${d|has_dict_type}[${key}] if ${key} in ${d} else ${
                        default|not self.writes_any_variables(default)
                    }
                """,
                replacement="${d}.get(${key}, ${default})",
            ),
            CodeChange(
                pattern="""
                    ${d|has_dict_type}.get(${key}) if ${key} in ${d} else ${
                        default|not self.writes_any_variables(default)
                    }
                """,
                replacement="${d}.get(${key}, ${default})",
            ),
        ]

    def description(self) -> str:
        return DEFAULT_GET_DESC

    def expected_semantic_differences(
        self,
    ) -> typing.Set[typing.Type[SemanticDifference]]:
        return {FunctionCallsOnException, LocalChangeOnException, NewException}
