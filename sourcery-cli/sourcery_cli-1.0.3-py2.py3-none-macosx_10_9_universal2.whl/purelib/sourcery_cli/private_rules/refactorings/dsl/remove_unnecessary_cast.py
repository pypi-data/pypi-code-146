from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class RemoveUnnecessaryCastProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    int(${var|has_int_type})
                """,
                replacement="""
                    ${var}
                """,
            ),
            CodeChange(
                pattern="""
                    str(${var|has_str_type})
                """,
                replacement="""
                    ${var}
                """,
            ),
            CodeChange(
                pattern="""
                    float(${var|has_float_type})
                """,
                replacement="""
                    ${var}
                """,
            ),
            CodeChange(
                pattern="""
                    bool(${var|has_bool_type})
                """,
                replacement="""
                    ${var}
                """,
            ),
        ]

    def description(self) -> str:
        return "Remove unnecessary casts to int, str, float or bool"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
