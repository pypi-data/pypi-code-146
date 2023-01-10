from typing import List

from sourcery.conditions.capture_conditions import CaptureConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class InlineImmediatelyYieldedVariableProposer(
    DSLProposer, CaptureConditions, VariableUsageConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${var | is_name} = ${expr}
                    yield ${var | not self.is_accessed_later(var)}
                """,
                replacement="""
                    yield ${expr}
                """,
            ),
            CodeChange(
                pattern="""
                    ${var | is_name} = ${expr}
                    yield from ${var | not self.is_accessed_later(var)}
                """,
                replacement="""
                    yield from ${expr}
                """,
            ),
        ]

    def description(self) -> str:
        return "Inline variable that is immediately yielded"
