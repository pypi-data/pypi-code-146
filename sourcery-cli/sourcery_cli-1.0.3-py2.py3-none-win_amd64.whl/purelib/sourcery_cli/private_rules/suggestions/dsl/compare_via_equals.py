"""Suggestion to replace `is` comparisons with `==`.

Based on a team rule of Senseye.

Using == or != is the preferred syntax for comparing str, bytes and int literals
according to Flake8 F632
https://flake8.pycqa.org/en/latest/user/error-codes.html

This suggestion has a broader scope:
It is shown not only for literals, but for all int values.
"""

from typing import List

from sourcery.analysis.typing.statement_types import UNKNOWN_TYPE
from sourcery.ast.nodes import Node
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType

EQUALS_COMPARISONS = [
    {"int"},
    {"int", "optional"},
    {"int", UNKNOWN_TYPE},
    {"int", "float"},
    {"float"},
    {"float", "optional"},
    {"float", UNKNOWN_TYPE},
    {"str"},
    {"str", "optional"},
    {"str", UNKNOWN_TYPE},
    {"bytes"},
    {"bytes", "optional"},
    {"bytes", UNKNOWN_TYPE},
]


class CompareViaEqualsProposer(DSLProposer, LiteralConditions, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a} is ${b|self.should_be_compared_via_equals(a,b)}
                """,
                replacement="""
                    ${a} == ${b}
                """,
            ),
            CodeChange(
                pattern="""
                    ${a} is not ${b|self.should_be_compared_via_equals(a,b)}
                """,
                replacement="""
                    ${a} != ${b}
                """,
            ),
        ]

    def description(self) -> str:
        return "Use == or != to compare str, bytes, int, and float"

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION

    def should_be_compared_via_equals(self, a: Node, b: Node) -> bool:
        compared_types = {self.infer_type(a), self.infer_type(b)}
        return compared_types in EQUALS_COMPARISONS and self.both_not_none(a, b)

    def both_not_none(self, a: Node, b: Node) -> bool:
        return not (self.is_none_literal(a) or self.is_none_literal(b))
