import typing

from sourcery.analysis.control_flow_next_node import ControlFlowNextNode
from sourcery.ast import (
    AST,
    ClassDef,
    Continue,
    For,
    If,
    Node,
    Pass,
    Try,
    While,
    find_parent_of_type,
)
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import (
    FLATTEN_NESTED_TRY_DESC,
    REMOVE_REDUNDANT_CONTINUE,
    REMOVE_REDUNDANT_PASS,
)
from sourcery.rules.private.refactorings.visitor.if_proposals import (
    SwapIfElseBranchesProposal,
)


class RemoveRedundantCodeProposer(MultiProposer):
    """AST walker that proposes removing redundant code."""

    next_nodes: ControlFlowNextNode

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {
            RemoveRedundantPassProposal,
            RemoveRedundantContinueProposal,
            FlattenNestedTryProposal,
        }

    def enter_continue(self, node: Continue):
        self.remove_redundant_continue(node)

    def remove_redundant_continue(self, node: Continue) -> None:
        if node.next_sibling():
            return

        if next_node := self.next_nodes[node]:
            parent_loop = find_parent_of_type(node, (For, While))
            if parent_loop and not parent_loop.orelse:  # type: ignore
                loop_next_node = self.next_nodes[parent_loop]
                if next_node == loop_next_node:
                    self.propose_remove_continue(node)
        else:
            self.propose_remove_continue(node)

    def propose_remove_continue(self, node: Continue):
        if len(node.parent.statements) > 1:
            self.propose(RemoveRedundantContinueProposal(self.ast, node))
        elif isinstance(node.parent.parent, If):
            parent_if = node.parent.parent
            if parent_if.body and parent_if.orelse and not parent_if.elifs:
                self.propose(RemoveRedundantContinueProposal(self.ast, node))

    def enter_pass(self, node: Pass):
        if not isinstance(node.parent.parent, ClassDef) and (
            len(node.parent) > 1
            or (len(node.parent) == 1 and node.parent.is_else_block())
        ):
            self.propose(RemoveRedundantPassProposal(self.ast, node))

    def enter_try(self, node: Try):
        grandparent = node.parent.parent
        if (
            isinstance(grandparent, Try)
            and len(node.parent) == 1
            and grandparent.body == node.parent  # is within try-clause
            and len(grandparent.handlers) == 0
            and len(node.finalbody.statements) == 0
        ):
            self.propose(FlattenNestedTryProposal(self.ast, grandparent, node))


class RemoveRedundantContinueProposal(Proposal):
    """Removes redundant continue."""

    def __init__(self, ast: AST, node: Continue) -> None:
        self.ast = ast
        self.node = node
        self.node_index = self.node.parent.index(self.node)

    def description(self):
        return REMOVE_REDUNDANT_CONTINUE

    def target_nodes(self) -> typing.Tuple[Node, ...]:
        if (
            isinstance(self.node.parent.parent, If)
            and len(self.node.parent) == 1
            and not self.node.parent.is_else_block()
        ):
            return SwapIfElseBranchesProposal(
                self.ast, self.node.parent.parent
            ).target_nodes()
        return (self.node,)

    def transient(self) -> bool:
        return True

    def execute(self) -> None:
        if (
            isinstance(self.node.parent.parent, If)
            and len(self.node.parent) == 1
            and not self.node.parent.is_else_block()
        ):
            SwapIfElseBranchesProposal(self.ast, self.node.parent.parent).execute()
        self.node.parent.remove(self.node)


class RemoveRedundantPassProposal(Proposal):
    """Removes redundant pass."""

    def __init__(self, ast: AST, node: Pass) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return REMOVE_REDUNDANT_PASS

    def execute(self) -> None:
        self.node.parent.remove(self.node)


class FlattenNestedTryProposal(Proposal):
    def __init__(self, ast: AST, outer_try: Try, inner_try: Try) -> None:
        self.ast = ast
        self.outer_try = outer_try
        self.inner_try = inner_try

    def description(self) -> str:
        return FLATTEN_NESTED_TRY_DESC

    def target_nodes(self) -> typing.Tuple[Node, ...]:
        return (self.outer_try,)

    def execute(self) -> None:
        self.outer_try.handlers = self.inner_try.handlers + self.outer_try.handlers
        self.outer_try.orelse = self.inner_try.orelse
        self.outer_try.body.statements = self.inner_try.body.statements
