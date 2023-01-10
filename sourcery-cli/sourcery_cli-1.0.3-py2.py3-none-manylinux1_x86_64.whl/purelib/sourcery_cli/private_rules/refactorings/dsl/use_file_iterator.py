from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class UseFileIteratorProposer(DSLProposer, TypeConditions, VariableUsageConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    for ${line} in ${file|self.has_type(file, 'IO')}.readlines():
                        ${statements+| not self.directly_accesses_variable(statements, file)}
                """,
                replacement="""
                    for ${line} in ${file}:
                        ${statements}
                """,
            )
        ]

    def description(self) -> str:
        return "Iterate over files directly rather than using readlines()"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
