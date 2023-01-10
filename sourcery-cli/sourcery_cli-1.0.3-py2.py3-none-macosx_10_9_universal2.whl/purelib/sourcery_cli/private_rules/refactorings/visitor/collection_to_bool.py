import typing

from sourcery.ast import AST
from sourcery.ast.ast import parent_coerces_to_bool
from sourcery.ast.nodes import Constant, Dict, List, Node, Set, Tuple
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    FunctionCallsOnException,
    LocalChangeOnException,
    SemanticDifference,
)


class CollectionToBoolProposer(Proposer, DependencyConditions):
    def enter_dict(self, node: Dict) -> None:
        self.enter_collection(node, len(node.values))

    def enter_list(self, node: List) -> None:
        self.enter_collection(node, len(node.elts))

    def enter_set(self, node: Set) -> None:
        self.enter_collection(node, len(node.elts))

    def enter_tuple(self, node: Tuple) -> None:
        self.enter_collection(node, len(node.elts))

    def enter_collection(
        self, node: typing.Union[Dict, List, Set, Tuple], length: int
    ) -> None:
        if parent_coerces_to_bool(node) and not self.writes_any_variables(node):
            self.propose(CollectionToBoolProposal(self.ast, node, length > 0))


class CollectionToBoolProposal(Proposal):
    def __init__(self, ast: AST, node: Node, truthy: bool):
        self.ast = ast
        self.node = node
        self.truthy = truthy

    def description(self):
        return "Replace constant collection with boolean in boolean contexts"

    def execute(self) -> None:
        self.node.replace(Constant(self.truthy))

    @classmethod
    def expected_semantic_differences(
        cls,
    ) -> typing.Set[typing.Type[SemanticDifference]]:
        # this refactoring may remove the `TypeError("unhashable type: <...>")`
        # exception by e.g. replacing `{[], []}` with `True`
        return {ExceptionRemoved, FunctionCallsOnException, LocalChangeOnException}
