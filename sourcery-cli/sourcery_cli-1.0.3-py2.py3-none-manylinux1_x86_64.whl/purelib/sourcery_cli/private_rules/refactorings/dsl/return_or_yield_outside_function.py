from typing import List

from sourcery.ast.nodes import FunctionDef
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class ReturnOrYieldOutsideFunctionProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern=pattern,
                replacement="",
                # the only condition is that the current node's scope is not a function
                # definition. If it is a module or a classdef, for instance, then the
                # statement must be removed.
                top_level_condition=lambda node: not isinstance(
                    node.scope(), FunctionDef
                ),
            )
            for pattern in (
                "return ${value?}",
                "yield ${value?}",
                "yield from ${value}",
            )
        ]

    def description(self) -> str:
        return "Remove return or yield statements found outside function definitions"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
