from typing import List

from sourcery.ast.nodes import ExceptHandler
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class SimplifySingleExceptionTupleProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="(${exc},)",
                replacement="${exc}",
                top_level_condition=lambda node: isinstance(node.parent, ExceptHandler),
            )
        ]

    def description(self) -> str:
        return "Replace length-one exception tuple with exception"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
