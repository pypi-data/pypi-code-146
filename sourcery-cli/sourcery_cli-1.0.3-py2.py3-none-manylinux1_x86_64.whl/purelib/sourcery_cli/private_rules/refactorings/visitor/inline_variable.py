from typing import Set

from sourcery.analysis.control_flow_next_node import ControlFlowNextNode
from sourcery.analysis.node_dependencies import NodeDependencies
from sourcery.analysis.nodes_in_loops import NodesInLoops
from sourcery.analysis.variable_usage import VariableUsage, accessed_later
from sourcery.ast import (
    AST,
    Assign,
    Attribute,
    BinOp,
    Call,
    Constant,
    FormattedValue,
    FunctionDef,
    Name,
    Node,
    Subscript,
    block_children,
    has_ancestor_of_type,
    is_single_target_assign,
)
from sourcery.code.source_unparser import MAX_LINE_LENGTH
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import INLINE_VAR_DESC
from sourcery.rules.private.refactorings.visitor.for_index_proposals import (
    gather_to_nodes,
)


class InlineVariableProposer(Proposer):
    """AST walker that proposes inlining variables."""

    node_dependencies: NodeDependencies
    variable_usage: VariableUsage
    next_nodes: ControlFlowNextNode
    nodes_in_loops: NodesInLoops

    def enter_assign(self, node: Assign):
        # pylint: disable=too-many-return-statements
        if not self.is_valid_assign(node):
            return

        assign_target = node.targets[0].unparse()

        if assign_target in self.node_dependencies[node.value].all_reads_and_writes():
            return

        next_sibling = node.next_sibling()
        if not next_sibling or block_children(next_sibling):
            return

        if not self.node_dependencies[next_sibling].reads_vars({assign_target}):
            return

        if accessed_later(
            {assign_target},
            next_sibling,
            self.variable_usage,
            self.next_nodes,
            self.nodes_in_loops,
        ):
            return

        outgoing = self.node_dependencies[node].outgoing.values()

        to_nodes = gather_to_nodes(outgoing)
        variable_to_nodes = {
            to_node for to_node in to_nodes if hash(to_node) == hash(node.targets[0])
        }
        if not len(variable_to_nodes) == len(to_nodes) == 1:
            return

        # TODO At the moment due to the way we split up the code, at module level
        # we don't know whether variables are used in later functions
        if not isinstance(node.scope(), FunctionDef):
            return

        if (
            len(node.value.unparse()) + len(next_sibling.unparse()) - len(assign_target)
            > MAX_LINE_LENGTH
        ):
            return

        # Dont inline strings into f-strings
        if has_ancestor_of_type(to_nodes[0], FormattedValue):
            return

        self.propose(InlineVariableProposal(self.ast, node, variable_to_nodes))

    def is_valid_assign(self, node: Assign):
        return (
            is_single_target_assign(node)
            and isinstance(node.targets[0], Name)
            and isinstance(
                node.value, (Call, Name, Attribute, Constant, Subscript, BinOp)
            )
        )


class InlineVariableProposal(Proposal):
    """Inlines a variable."""

    def __init__(
        self,
        ast: AST,
        node: Assign,
        variable_to_nodes: Set[Node],
    ) -> None:
        self.ast = ast
        self.node = node
        self.to_nodes = variable_to_nodes

    def description(self):
        return INLINE_VAR_DESC

    def transient(self) -> bool:
        return True

    def execute(self) -> None:
        for node in self.to_nodes:
            node.replace(self.node.value)
        self.node.parent.remove(self.node)
