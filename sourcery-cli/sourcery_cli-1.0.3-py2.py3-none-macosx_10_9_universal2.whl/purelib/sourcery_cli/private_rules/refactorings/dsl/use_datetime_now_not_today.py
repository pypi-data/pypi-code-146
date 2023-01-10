from typing import List, Set, Type

from sourcery.conditions.import_conditions import ImportConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    FunctionCallsChanged,
    SemanticDifference,
)


class UseDatetimeNowNotTodayProposer(DSLProposer, ImportConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${dt |
                        self.is_name_node_for_import_name(dt, 'datetime.datetime')
                    }.today()
                """,
                replacement="${self.node_for_import_name('datetime.datetime')}.now()",
                top_level_condition=lambda _: self.has_available_import_name(
                    "datetime.datetime"
                ),
            )
        ]

    def description(self) -> str:
        return "Replace datetime.datetime.today() with datetime.datetime.now()"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {FunctionCallsChanged}

    def is_semantic_improvement(self) -> bool:
        # This refactoring chooses the more expressive name from 2 functionally
        # equivalent functions.
        return True
