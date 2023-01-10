from typing import List

from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class MissingDictItemsProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    for ${key}, ${value} in ${data|has_dict_type}:
                        ${statements+}
                """,
                replacement="""
                    for ${key}, ${value} in ${data}.items():
                        ${statements}
                """,
            ),
            CodeChange(
                pattern="""
                    {${modified_key}: ${modified_value} for ${key}, ${value} in ${data|has_dict_type} if ${condition?}}
                """,
                replacement="""
                    {${modified_key}: ${modified_value} for ${key}, ${value} in ${data}.items() if ${condition}}
                """,
            ),
            CodeChange(
                pattern="""
                    [${new_target} for ${key}, ${value} in ${data|has_dict_type} if ${condition?}]
                """,
                replacement="""
                    [${new_target} for ${key}, ${value} in ${data}.items() if ${condition}]
                """,
            ),
            CodeChange(
                pattern="""
                    {${new_target} for ${key}, ${value} in ${data|has_dict_type} if ${condition?}}
                """,
                replacement="""
                    {${new_target} for ${key}, ${value} in ${data}.items() if ${condition}}
                """,
            ),
        ]

    def description(self) -> str:
        return "Add missing .items() when iterating over dictionary"

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION
