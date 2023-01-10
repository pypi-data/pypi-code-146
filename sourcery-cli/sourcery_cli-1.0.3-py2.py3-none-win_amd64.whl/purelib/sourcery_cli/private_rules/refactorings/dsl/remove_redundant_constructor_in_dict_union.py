from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class RemoveRedundantConstructorInDictUnionProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            # Unpack an unnecessary dict constructor
            # x = dict(y) | z => x = y | z
            CodeChange(
                pattern="""
                    dict(${initial | has_dict_type}) | ${other}
                """,
                replacement="""
                    ${initial} | ${other}
                """,
            ),
            # x = y | dict(z) => x = y | z
            CodeChange(
                pattern="""
                    ${initial | has_dict_type} | dict(${other})
                """,
                replacement="""
                    ${initial} | ${other}
                """,
            ),
            # Unpack an unnecessary dict copy
            # x = y.copy() | z => x = y | z
            CodeChange(
                pattern="""
                    ${initial | has_dict_type}.copy() | ${other}
                """,
                replacement="""
                    ${initial} | ${other}
                """,
            ),
            # x = y | z.copy() => x = y | z
            CodeChange(
                pattern="""
                    ${initial | has_dict_type} | ${other | has_dict_type}.copy()
                """,
                replacement="""
                    ${initial} | ${other}
                """,
            ),
        ]

    def description(self) -> str:
        return "Remove a redundant constructor in a dictionary union"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
