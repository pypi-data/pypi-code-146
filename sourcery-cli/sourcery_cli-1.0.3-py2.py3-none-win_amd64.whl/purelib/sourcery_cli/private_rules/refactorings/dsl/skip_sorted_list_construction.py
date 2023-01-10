from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class SkipSortedListConstructionProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a_list} = list(${an_iterable})
                    ${a_list}.sort()
                """,
                replacement="""
                    ${a_list} = sorted(${an_iterable})
                """,
            ),
            CodeChange(
                pattern="""
                    ${a_list} = ${an_iterable | has_list_type}.copy()
                    ${a_list}.sort()
                """,
                replacement="""
                    ${a_list} = sorted(${an_iterable})
                """,
            ),
            CodeChange(
                pattern="""
                    ${a_list} = ${an_iterable | has_list_type}[:]
                    ${a_list}.sort()
                """,
                replacement="""
                    ${a_list} = sorted(${an_iterable})
                """,
            ),
        ]

    def description(self) -> str:
        return "Remove an unnecessary list construction call prior to sorting"
