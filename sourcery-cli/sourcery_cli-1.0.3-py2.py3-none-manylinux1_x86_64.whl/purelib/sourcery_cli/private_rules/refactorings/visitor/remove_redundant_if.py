"""Remove redundant conditional."""

from typing import Dict, Union

from sourcery.analysis.logic_solver import (
    Condition,
    NodeExpressions,
    tautologies_and_contradictions,
)
from sourcery.analysis.statement_conditions import StatementConditions
from sourcery.ast import (
    AST,
    Block,
    BoolOp,
    Constant,
    Elif,
    Expression,
    If,
    is_pass_block,
)
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import REMOVE_IFS_DESC


class RemoveRedundantIfProposer(Proposer, DependencyConditions):
    """AST walker that proposes removing redundant if conditions."""

    conditions: StatementConditions
    expressions: NodeExpressions

    def enter_if(self, node: If):
        # Don't want to remove anything that might have side-effects
        if self.writes_any_variables(node.test):
            return

        if self.is_empty_if(node):
            # If this if only contains a Pass, remove it.
            replacements = {node.test: False}
        else:
            replacements = tautologies_and_contradictions(
                Condition(node.test),
                self.conditions[node],
                self.expressions,
            )

        if replacements:
            self.propose(RemoveRedundantIfProposal(self.ast, node, replacements))

    def enter_elif(self, node: Elif):
        # Don't want to remove anything that might have side-effects
        if self.writes_any_variables(node.test):
            return

        if replacements := tautologies_and_contradictions(
            Condition(node.test),
            self.conditions[node],
            self.expressions,
        ):
            self.propose(RemoveRedundantIfProposal(self.ast, node, replacements))

    def is_empty_if(self, node: If):
        return is_pass_block(node.body) and not node.orelse and not node.elifs


class RemoveRedundantIfProposal(Proposal):
    """Removes unnecessary conditions that are always true."""

    def __init__(
        self, ast: AST, node: Union[If, Elif], replacements: Dict[Expression, bool]
    ) -> None:
        self.ast = ast
        self.node = node
        self.replacements = replacements

    def description(self):
        return REMOVE_IFS_DESC

    def execute(self) -> None:
        # Replace tautologies and contradictions with True or False
        # and simplify booleans accordingly
        self.node.test = self.simplify_expression(self.node.test)

        # If a condition is always true use the body, always false
        # use the else.
        if isinstance(self.node.test, Constant):
            if isinstance(self.node, If):
                if self.node.test.value or not self.node.elifs:
                    index = self.node.parent.index(self.node)
                    parent_block = (
                        self.node.body if self.node.test.value else self.node.orelse
                    )
                    self.node.parent[index : index + 1] = parent_block.statements
                else:  # We have elifs and the if test is False
                    self.node.test = self.node.elifs[0].test
                    self.node.body = self.node.elifs[0].body
                    self.node.elifs = self.node.elifs[1:]
            else:
                assert isinstance(self.node, Elif)
                index = self.node.parent.elifs.index(self.node)
                if self.node.test.value:
                    self.node.parent.elifs = self.node.parent.elifs[:index]
                    self.node.parent.orelse = Block(self.node.body.statements)
                else:
                    self.node.parent.edit_tuple(
                        "elifs", lambda elifs: elifs.remove(self.node)
                    )

        self.node.test.clear_original_source()

    def simplify_expression(self, condition: Expression) -> Expression:
        if condition in self.replacements:
            return Constant(self.replacements[condition])
        elif isinstance(condition, BoolOp):
            values = tuple(
                self.simplify_expression(value) for value in condition.values
            )
            return self.simplify_boolop(BoolOp(condition.op, values))
        else:
            return condition

    def simplify_boolop(self, condition: BoolOp) -> Expression:
        consts = tuple(
            value.value for value in condition.values if isinstance(value, Constant)
        )
        values = tuple(
            value for value in condition.values if not isinstance(value, Constant)
        )

        if condition.op == BoolOp.AND:
            if not all(consts):
                return Constant(False)
            if not values:
                return Constant(True)
        else:
            if any(consts):
                return Constant(True)
            if not values:
                return Constant(False)

        return BoolOp(condition.op, values) if len(values) > 1 else values[0]
