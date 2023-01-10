from typing import List

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class RemoveAssertTrueProposer(DSLProposer, DependencyConditions):
    # TODO: this rule could probably be merged into `remove-unused-statement` once that
    # becomes a thing

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="assert True, ${reason?}",
                replacement="",
            )
        ]

    def description(self) -> str:
        return "Remove `assert True` statements"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
