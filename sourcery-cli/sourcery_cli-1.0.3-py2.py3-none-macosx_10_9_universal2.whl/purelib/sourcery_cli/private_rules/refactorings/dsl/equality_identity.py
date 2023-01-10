from typing import List

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.dsl.utils import not_in_equality_dunder


class EqualityIdentityProposer(DSLProposer, DependencyConditions, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${ x | (
                        self.has_built_in_type(x)
                        and not self.writes_any_variables(x)
                        and not self.has_float_type(x)
                        and not self.has_complex_number_type(x)
                    )} == ${x}
                """,
                replacement="""
                    True
                """,
                top_level_condition=not_in_equality_dunder,
            ),
            CodeChange(
                pattern="""
                    ${ x | (
                        self.has_built_in_type(x)
                        and not self.writes_any_variables(x)
                        and not self.has_float_type(x)
                        and not self.has_complex_number_type(x)
                    )} != ${x}
                """,
                replacement="""
                    False
                """,
                top_level_condition=not_in_equality_dunder,
            ),
        ]

    def description(self) -> str:
        return "Simplify x == x -> True and x != x -> False"
