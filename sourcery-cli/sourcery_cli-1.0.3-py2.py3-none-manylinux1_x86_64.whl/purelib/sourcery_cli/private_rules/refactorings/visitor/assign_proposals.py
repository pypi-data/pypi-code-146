"""Move assignments to the block in which the variable is used."""
from collections import OrderedDict, defaultdict
from typing import Dict, List, Set, Tuple, Type

from sourcery.analysis.node_dependencies import NodeDependencies
from sourcery.ast import (
    AST,
    Assign,
    Await,
    Block,
    Elif,
    For,
    FunctionDef,
    Name,
    Node,
    Statement,
    Try,
    While,
    With,
    get_nodes,
)
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import MOVE_ASSIGN_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    ReturnValuesChangedOnException,
    SemanticDifference,
)


# TODO Can the move assign be extended to other types of statements?
class MoveAssignProposer(Proposer, DependencyConditions):
    """Proposes moving assignments to the first place they are used."""

    node_dependencies: NodeDependencies
    scope_assigns: List[Dict[str, List[Assign]]]

    def reset(self, ast: AST):
        super().reset(ast)
        self.scope_assigns = []

    def enter_functiondef(self, _node: FunctionDef):
        self.scope_assigns.append(defaultdict(list))

    def leave_functiondef(self, _node: FunctionDef):
        self.make_proposals()
        self.scope_assigns.pop()

    def leave_assign(self, node: Assign):
        if self.scope_assigns:
            for target in get_nodes(node.targets):
                if isinstance(target, Name):
                    self.scope_assigns[-1][target.id].append(node)

    def make_proposals(self) -> None:
        movements: Dict[Assign, Statement] = OrderedDict()

        for var_name, assign_stmts in self.scope_assigns[-1].items():
            if len(assign_stmts) == 1:
                assign = assign_stmts[0]
                if len(get_nodes(assign.targets)) == 1 and not isinstance(
                    assign.value, Await
                ):
                    usage = self.find_variable_usage(var_name, assign)
                    if usage.parent != assign.parent:
                        movements[assign] = usage

        if movements:
            self.propose(MoveAssignProposal(self.ast, movements))

    def find_variable_usage(self, var_name: str, assignment: Assign) -> Statement:
        # Check all variables used in the assignment

        current_node: Statement = assignment
        previous_node: Statement = assignment

        while True:
            current_node_deps = self.node_dependencies[current_node]

            if (
                isinstance(previous_node, Statement)
                and isinstance(current_node, Statement)
                and not self.can_be_moved_ahead_of(previous_node, current_node)
            ):
                return previous_node

            if (
                current_node != assignment
                and isinstance(current_node, Statement)
                and not self.can_be_moved_past(assignment, current_node)
            ):
                return self.find_elif_start(current_node)

            outgoing_nodes = [
                dep.node
                for dep, edge in current_node_deps.outgoing.items()
                if var_name in edge.from_vars()
            ]

            if outgoing_nodes and outgoing_nodes[0] == current_node.parent:
                return current_node
            elif outgoing_nodes and isinstance(
                outgoing_nodes[0], (For, While, Try, With)
            ):
                return outgoing_nodes[0]
            elif len(outgoing_nodes) == 1 and (
                outgoing_nodes[0].is_statement or isinstance(outgoing_nodes[0], Block)
            ):
                previous_node = current_node
                current_node = outgoing_nodes[0]  # type: ignore
            elif len(outgoing_nodes) > 1 and isinstance(current_node, Block):
                assert isinstance(outgoing_nodes[0], Statement)
                return outgoing_nodes[0]
            else:
                return self.find_elif_start(current_node)

    def find_elif_start(self, node: Statement) -> Statement:
        """Returns enclosing if statement for elifs else the node.

        When the node is an if statement within an elif, then the assignment can
        only be moved before the start of the elif. Find the initial If
        """
        return node.parent if isinstance(node, Elif) else node


class MoveAssignProposal(Proposal):
    def __init__(self, ast: AST, movements: Dict[Assign, Statement]) -> None:
        self.ast = ast
        self.movements = movements

    def description(self):
        return MOVE_ASSIGN_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return tuple(self.movements.keys())

    def execute(self) -> None:
        for assign, var_usage in self.movements.items():
            assign.parent.remove(assign)
            var_usage.parent.insert(var_usage.parent.index(var_usage), assign)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {ReturnValuesChangedOnException, ExceptionRemoved}
