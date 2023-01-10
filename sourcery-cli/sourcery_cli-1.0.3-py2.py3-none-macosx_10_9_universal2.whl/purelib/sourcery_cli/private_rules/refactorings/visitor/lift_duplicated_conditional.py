from typing import List, Optional

from sourcery.ast import AST, Block, BoolOp, Expression, If
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import HOIST_COND_DESC
from sourcery.rules.private.refactorings.visitor.remove_redundant_if import (
    RemoveRedundantIfProposal,
)


class LiftDuplicatedConditionalProposer(Proposer):
    def enter_if(self, node: If):
        if (
            not node.orelse
            and node.elifs
            and isinstance(node.test, BoolOp)
            and node.test.op == BoolOp.AND
        ):
            condition_to_hoist = node.test.values[0]
            hoistable = [
                self.hoistable_condition(elif_node.test, hash(condition_to_hoist))
                for elif_node in node.elifs
            ]
            if all(hoistable):
                self.propose(
                    LiftDuplicatedConditionalProposal(
                        self.ast, node, condition_to_hoist, hoistable  # type: ignore
                    )
                )

    def hoistable_condition(
        self, condition: Expression, compare_hash: int
    ) -> Optional[Expression]:
        assert isinstance(condition.parent.parent, If)
        if (
            hash(condition) == compare_hash
            and condition.parent == condition.parent.parent.elifs[-1]
        ):
            return condition
        elif (
            isinstance(condition, BoolOp)
            and condition.op == BoolOp.AND
            and hash(condition.values[0]) == compare_hash
        ):
            return condition.values[0]
        else:
            return None


class LiftDuplicatedConditionalProposal(Proposal):
    """Hoists an if proposal out of another one."""

    def __init__(
        self,
        ast: AST,
        node: If,
        condition_to_hoist: Expression,
        elif_conditions: List[Expression],
    ) -> None:
        self.ast = ast
        self.node = node
        self.condition_to_hoist = condition_to_hoist
        self.elif_conditions = elif_conditions

    def description(self):
        return HOIST_COND_DESC

    def execute(self) -> None:
        RemoveRedundantIfProposal(
            self.ast, self.node, {self.condition_to_hoist: True}
        ).execute()
        for condition, node in zip(self.elif_conditions, self.node.elifs):
            RemoveRedundantIfProposal(self.ast, node, {condition: True}).execute()

        new_inner = self.node.copy_as_root()
        new_inner.original_path = None
        new_if = If(
            self.condition_to_hoist,
            Block((new_inner,)),
            (),
            Block(()),
        )
        self.node.replace(new_if)
