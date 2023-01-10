from typing import List, Union

from typing_extensions import TypeGuard

from sourcery.analysis.nodes_in_loops import NodesInLoops
from sourcery.ast import Break, Continue, Node
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class BreakOrContinueOutsideLoopProposer(DSLProposer):
    nodes_in_loops: NodesInLoops

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern=pattern,
                replacement="",
                top_level_condition=self.is_break_or_continue_outside_loop,
            )
            for pattern in ("break", "continue")
        ]

    def is_break_or_continue_outside_loop(
        self, node: Node
    ) -> TypeGuard[Union[Break, Continue]]:
        return isinstance(node, (Break, Continue)) and node not in self.nodes_in_loops

    def description(self) -> str:
        return "Remove break or continue statement found outside for or while loop"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
