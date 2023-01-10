from typing import List

from sourcery.ast import Constant
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class StrPrefixSuffixProposer(DSLProposer, TypeConditions, LiteralConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a | has_str_type}[:${num | is_int_literal}] == (
                        ${b | self.is_str_len(b, num)})
                """,
                replacement="""
                    ${a}.startswith(${b})
                """,
            ),
            CodeChange(
                pattern="""
                    ${a | has_str_type}[${num | is_int_literal}:] == (
                        ${b | self.is_negative_str_len(b, num)})
                """,
                replacement="""
                    ${a}.endswith(${b})
                """,
            ),
        ]

    def is_str_len(self, substring: Constant, num: Constant) -> bool:
        return self.is_str_literal(substring) and len(substring.value) == num.value

    def is_negative_str_len(self, substring: Constant, num: Constant) -> bool:
        return self.is_str_literal(substring) and len(substring.value) == -num.value

    def description(self) -> str:
        return "Replace str prefix/suffix check with call to `startswith/endswith`"
