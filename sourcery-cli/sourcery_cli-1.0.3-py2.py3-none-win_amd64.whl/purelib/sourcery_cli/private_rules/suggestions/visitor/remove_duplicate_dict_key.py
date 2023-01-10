import typing

from sourcery.ast import AST, Dict
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.engine.rule_type import RuleType
from sourcery.rules.private.suggestions.visitor.helpers import (
    find_duplicate_key_indices,
)


class RemoveDuplicateDictKeyProposer(Proposer, DependencyConditions):
    """Proposer that removes duplicate keys from dicts."""

    def enter_dict(self, node: Dict):
        if not self.writes_any_variables(node) and (
            redundant_indices := find_duplicate_key_indices(node.keys, node.values)
        ):
            self.propose(
                RemoveDuplicateDictKeyProposal(self.ast, node, redundant_indices)
            )

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION


class RemoveDuplicateDictKeyProposal(Proposal):
    """Removes duplicate keys in dicts instantiation."""

    def __init__(self, ast: AST, node: Dict, indices: typing.List[int]) -> None:
        self.ast = ast
        self.node = node
        self.indices = indices

    def description(self) -> str:
        return "Remove duplicate keys when instantiating dicts"

    def execute(self) -> None:
        # pylint: disable=cell-var-from-loop
        for i in sorted(self.indices, reverse=True):
            self.node.edit_tuple("keys", lambda keys: keys.pop(i))
            self.node.edit_tuple("values", lambda values: values.pop(i))

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION
