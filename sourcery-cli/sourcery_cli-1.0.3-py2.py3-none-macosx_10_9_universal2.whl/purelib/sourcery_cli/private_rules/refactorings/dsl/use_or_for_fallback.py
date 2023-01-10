from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class UseOrForFallbackProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${value} = ${first}
                    if not ${value}:
                      ${value} = ${fallback}
                """,
                replacement="${value} = ${first} or ${fallback}",
            )
        ]

    def description(self) -> str:
        return "Use `or` for providing a fallback value"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def should_produce_1_line(self) -> bool:
        # This refactoring should be applied only if the resulting `or` expression fits
        # to 1 line.
        # https://sourcery-ai.slack.com/archives/C02JA0WDKTP/p1646815696477669
        return True
