"""Hoist conditional out of nested conditional."""

from typing import Set, Type

from sourcery.analysis.boolean_algebra import is_tautology
from sourcery.analysis.logic_solver import NodeExpressions
from sourcery.analysis.node_dependencies import NodeDependencies
from sourcery.ast import AST, If, Node
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import HOIST_IF_DESC
from sourcery.semantic_equivalence.semantic_types import (
    NewException,
    SemanticDifference,
)


class HoistIfFromIfProposer(Proposer):
    node_dependencies: NodeDependencies
    node_expressions: NodeExpressions

    def enter_if(self, node: If):
        if self.can_hoist_if(node):
            self.propose(HoistIfFromIfProposal(self.ast, node))

    def can_hoist_if(self, node: If) -> bool:
        grandparent = node.parent.parent

        if not isinstance(grandparent, If) or grandparent.elifs:
            return False

        test_vars = self.node_dependencies[node.test].all_reads_and_writes()
        grandparent_test_deps = self.node_dependencies[grandparent.test]
        other_grandparent_block_deps = self.node_dependencies[
            grandparent.body if node.parent.is_else_block() else grandparent.orelse
        ]

        return (
            not node.orelse
            and not node.elifs
            and not grandparent_test_deps.writes_vars(test_vars)
            and not other_grandparent_block_deps.writes_vars(test_vars)
            and self.is_last_statement(node)
            and self.conditions_match(
                grandparent.test, node.test, node.parent.is_else_block()
            )
        )

    def is_last_statement(self, node: If) -> bool:
        return node.parent[-1] == node

    def conditions_match(
        self, parent_condition: Node, condition: Node, is_else: bool
    ) -> bool:
        parent_condition_expression = self.node_expressions.expression_for(
            parent_condition
        )
        parent_expression = (
            ~parent_condition_expression if is_else else parent_condition_expression
        )

        return is_tautology(
            self.node_expressions.expression_for(condition) >> parent_expression
        )


class HoistIfFromIfProposal(Proposal):
    """Hoists an if proposal out of another one."""

    def __init__(self, ast: AST, node: If) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return HOIST_IF_DESC

    def execute(self) -> None:
        parent_if = self.node.parent.parent
        assert isinstance(parent_if, If)
        self.node.parent.pop()
        parent_index = parent_if.parent.index(parent_if)
        parent_if.parent.insert(parent_index + 1, self.node)
        if not parent_if.body:
            parent_if.parent.pop(parent_index)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {NewException}
