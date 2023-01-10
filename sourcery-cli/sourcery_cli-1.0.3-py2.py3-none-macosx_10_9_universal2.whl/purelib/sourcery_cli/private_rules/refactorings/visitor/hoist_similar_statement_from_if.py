"""Contains refactorings for similar code hoisting."""
from typing import List, Set, Tuple, Type

from sourcery.analysis.clone_detection import NodeClones
from sourcery.ast import AST, Block, If, Statement, find_common_ancestor_children
from sourcery.ast.differences import Difference, DiffType, all_differences
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.visitor.if_proposals import (
    SwapIfElseBranchesProposal,
)
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionRemoved,
    ExceptionTypeChanged,
    LocalChangeOnException,
    SemanticDifference,
)


class HoistSimilarStatementFromIfProposer(Proposer, DependencyConditions):
    """AST walker that proposes the similar code hoisting refactoring.

    This seeks out code hoisting opportunites where there is an If node
    with very similar body and orelse blocks.

    It first goes through the tree on each side, matching nodes where
    possible and flagging updates, inserts or deletes otherwise. A
    parent match is one where the subtrees based on two nodes do not match
    but the nodes themselves do.

    It will attempt to hoist at the highest level possible, by finding
    differences between groups of statements where the parents match and
    choosing the highest level one.
    """

    node_clones: NodeClones

    def leave_if(self, node: If):
        if (
            not node.elifs
            and node.orelse
            and (
                hoistable_differences := self.hoistable_differences(
                    node.body, node.orelse
                )
            )
        ):
            changed_diffs, change_index = self.changed_diffs(hoistable_differences)

            if self.valid_diff(node, changed_diffs[0]):
                change_parent = changed_diffs[0].node.parent
                assert isinstance(change_parent, Block)
                self.propose(
                    HoistSimilarStatementFromIfProposal(
                        self.ast, node, changed_diffs, change_parent, change_index
                    )
                )

    def hoistable_differences(self, body: Block, orelse: Block) -> List[Difference]:
        """Finds differences between if branches that can be hoisted.

        A set of correspondences between nodes with matching parents, where
        the first or last statement is a match or the differences are in a
        deeper block (so can be hoisted).
        """
        differences = all_differences(body, orelse, self.node_clones)

        if common_ancestor_children := find_common_ancestor_children(
            [
                diff.node
                for diff in differences
                if diff.diff_type not in [DiffType.MATCH, DiffType.PARENT_MATCH]
            ]
        ):
            common_parent = common_ancestor_children[0].parent
            if isinstance(common_parent, Block):
                block_differences = [
                    diff for diff in differences if diff.node.parent == common_parent
                ]

                # Can hoist if the first or last child is a match
                if block_differences and (
                    block_differences[0].diff_type == DiffType.MATCH
                    or block_differences[-1].diff_type == DiffType.MATCH
                    or block_differences[0].node.parent != body
                ):
                    return block_differences

        return []

    def changed_diffs(
        self, differences: List[Difference]
    ) -> Tuple[List[Difference], int]:
        """Return the subset of differences where an actual change has occurred."""
        first_change_index = 0

        while differences[0].diff_type == DiffType.MATCH:
            differences = differences[1:]
            first_change_index += 1

        while differences[-1].diff_type == DiffType.MATCH:
            differences = differences[:-1]

        return differences, first_change_index

    def valid_diff(self, node: If, difference: Difference) -> bool:
        """Check that the if statement can be hoisted before the first change."""
        if difference.diff_type == DiffType.INSERT:
            # If all diffs are matches followed by inserts we need to check
            # can_move_node_ahead_of in the else branch to avoid index out of range
            first_change = difference.diff_node
        else:
            first_change = difference.node

        return isinstance(first_change, Statement) and self.can_be_moved_ahead_of(
            node, first_change
        )


class HoistSimilarStatementFromIfProposal(Proposal):
    """Hoists code that is always executed out of an if statement.

    N.B. This has the same name and id as its counterpart in hoist_proposal.
    This is so they can be skipped together
    """

    def __init__(
        self,
        ast: AST,
        node: If,
        differences: List[Difference],
        new_if_parent: Block,
        new_if_index: int,
    ) -> None:
        self.ast = ast
        self.node = node
        self.new_if_parent = new_if_parent
        self.new_if_index = new_if_index
        self.differences = differences

    def description(self):
        return "Hoist nested repeated code outside conditional statements"

    def execute(self) -> None:
        body = Block(
            tuple(
                diff.node  # type: ignore
                for diff in self.differences
                if diff.diff_type != DiffType.INSERT
            )
        )
        orelse = Block(
            tuple(
                diff.diff_node  # type: ignore
                for diff in self.differences
                if diff.diff_type != DiffType.DELETE
            )
        )
        new_if = If(test=self.node.test, body=body, elifs=(), orelse=orelse)

        self.new_if_parent[self.new_if_index : self.new_if_index + len(body)] = (
            new_if,
        )

        node_index = self.node.parent.index(self.node)
        self.node.parent[node_index : node_index + 1] = self.node.body.statements

        if not body:
            SwapIfElseBranchesProposal(self.ast, new_if).execute()

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {
            ExceptionArgsChanged,
            LocalChangeOnException,
            ExceptionRemoved,
            ExceptionTypeChanged,
        }
