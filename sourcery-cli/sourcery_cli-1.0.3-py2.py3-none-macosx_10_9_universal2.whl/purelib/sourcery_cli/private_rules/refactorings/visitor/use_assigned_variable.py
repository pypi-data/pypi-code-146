from typing import List, Tuple

from sourcery.analysis.clone_detection import NodeClones
from sourcery.analysis.node_dependencies import (
    GLOBAL_STATE,
    NodeDependencies,
    can_move_statement_ahead_of,
)
from sourcery.analysis.node_paths import PathNodes
from sourcery.ast import (
    AST,
    Assign,
    AugAssign,
    Constant,
    Delete,
    Expression,
    Name,
    Node,
    Statement,
    Subscript,
    is_contained_in,
    is_single_target_assign,
)
from sourcery.ast.ast import is_constant
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import USE_ASSIGN_VAR_DESC


class UseAssignedVariableProposer(Proposer, DependencyConditions):
    """Use previously assigned local variables if possible."""

    node_dependencies: NodeDependencies
    node_clones: NodeClones
    # make sure paths are set on all the nodes
    node_paths: PathNodes

    def leave_assign(self, node: Assign):
        if self.suitable_assignment(node):
            index = node.parent.statements.index(node)
            to_nodes = [
                clone
                for clone in self.node_clones[node.value]
                if clone != node.value
                and is_contained_in(clone, node.parent)
                and not any(
                    is_contained_in(clone, previous)
                    for previous in node.parent.statements[:index]
                )
            ]
            if to_nodes and all(
                self.can_replace(node, clone.statement()) for clone in to_nodes
            ):
                self.propose(
                    UseAssignedVariableProposal(
                        self.ast, node, to_nodes  # type: ignore
                    )
                )

    def suitable_assignment(self, node: Assign) -> bool:
        """Returns whether the node can be used as a replacement for other assigns.

        Can't read itself as can't replace this (might be an increment)
        Have to ensure we are referencing an existing object
        not creating a new one so limit the permissible values
        Also only do this for assignments to simple local variables.
        """
        return (
            is_single_target_assign(node)
            and not self.node_dependencies[node].writes_vars([GLOBAL_STATE])
            and not self.node_dependencies[node.value].reads_vars(
                self.node_dependencies[node].all_writes()
            )
            and not self.writes_any_variables(node.value)
            and isinstance(node.targets[0], Name)
            and self.suitable_value(node.value)
        )

    def suitable_value(self, node: Node) -> bool:
        return (
            isinstance(node, Name)
            or (
                isinstance(node, Subscript)
                and isinstance(node.value, Name)
                and isinstance(node.slice, (Name, Constant))
            )
        ) and not is_constant(node)

    def can_replace(self, node: Assign, statement: Statement) -> bool:
        return not isinstance(
            statement, (Assign, AugAssign, Delete)
        ) and can_move_statement_ahead_of(
            node, statement, self.node_dependencies, check_reads=False
        )


class UseAssignedVariableProposal(Proposal):
    def __init__(self, ast: AST, assign: Assign, to_nodes: List[Expression]) -> None:
        self.ast = ast
        self.assign = assign
        self.to_nodes = to_nodes
        self.replacements: List[Node] = []

    def description(self):
        return USE_ASSIGN_VAR_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return (self.assign,)

    def execute(self) -> None:
        for node in self.to_nodes:
            node.replace(self.assign.targets[0])
            node.clear_original_source()
            node.statement().clear_original_source()
