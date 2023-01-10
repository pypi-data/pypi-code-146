from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class SimplifyNegativeIndexProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a|has_list_type}[len(${a})-1]
                """,
                replacement="""
                    ${a}[-1]
                """,
            ),
            CodeChange(
                pattern="""
                    ${a}[len(${a})-1:${stop?}:${step?}]
                """,
                replacement="""
                    ${a}[-1: ${stop}: ${step}]
                """,
            ),
            CodeChange(
                pattern="""
                    ${a}[${start?}:len(${a})-1:${step?}]
                """,
                replacement="""
                    ${a}[${start}: -1 : ${step}]
                """,
            ),
        ]

    def description(self) -> str:
        return "Simplify accessing last index of list"
