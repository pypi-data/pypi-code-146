from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class NonEqualComparisonProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    if ${a | has_numeric_type} < ${b | has_numeric_type}:
                      return True
                    elif ${a} > ${b}:
                      return False
                """,
                replacement="""
                    if ${a} != ${b}:
                      return ${a} < ${b}
                """,
            ),
            CodeChange(
                pattern="""
                    if ${a | has_numeric_type} > ${b | has_numeric_type}:
                      return True
                    elif ${a} < ${b}:
                      return False
                """,
                replacement="""
                    if ${a} != ${b}:
                      return ${a} > ${b}
                """,
            ),
            CodeChange(
                pattern="""
                    if ${a | has_numeric_type} < ${b | has_numeric_type}:
                      return False
                    elif ${a} > ${b}:
                      return True
                """,
                replacement="""
                    if ${a} != ${b}:
                      return ${a} > ${b}
                """,
            ),
            CodeChange(
                pattern="""
                    if ${a | has_numeric_type} > ${b | has_numeric_type}:
                      return False
                    elif ${a} < ${b}:
                      return True
                """,
                replacement="""
                    if ${a} != ${b}:
                      return ${a} < ${b}
                """,
            ),
        ]

    def description(self) -> str:
        return "Simplify comparison of non equal values"
