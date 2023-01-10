import typing

from sourcery.ast import AST, Set
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.engine.rule_type import RuleType
from sourcery.rules.private.suggestions.visitor.helpers import (
    find_duplicate_key_indices,
)
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionTypeChanged,
    SemanticDifference,
)


class RemoveDuplicateSetKeyProposer(Proposer, DependencyConditions):
    """Proposer that removes duplicate keys from sets."""

    def enter_set(self, node: Set):
        if not self.writes_any_variables(node) and (
            redundant_indices := find_duplicate_key_indices(node.elts, node.elts)
        ):
            self.propose(
                RemoveDuplicateSetKeyProposal(self.ast, node, redundant_indices)
            )


class RemoveDuplicateSetKeyProposal(Proposal):
    """Removes duplicate keys in set instantiation."""

    def __init__(self, ast: AST, node: Set, indices: typing.List[int]) -> None:
        self.ast = ast
        self.node = node
        self.indices = indices

    def description(self) -> str:
        return "Remove duplicate keys when instantiating sets"

    def execute(self) -> None:
        # pylint: disable=cell-var-from-loop
        for i in sorted(self.indices, reverse=True):
            self.node.edit_tuple("elts", lambda elts: elts.pop(i))

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    @classmethod
    def expected_semantic_differences(
        cls,
    ) -> typing.Set[typing.Type[SemanticDifference]]:
        return {ExceptionArgsChanged, ExceptionTypeChanged}
