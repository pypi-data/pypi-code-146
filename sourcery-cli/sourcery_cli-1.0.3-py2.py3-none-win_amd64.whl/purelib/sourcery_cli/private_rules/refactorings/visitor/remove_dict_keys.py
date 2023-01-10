from typing import Optional, Set, Type

from sourcery.ast import AST, Attribute, Call, Compare, Comprehension, For, Node
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import REMOVE_KEYS_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionRemoved,
    ExceptionTypeChanged,
    FunctionCallsOnException,
    ReturnValuesChangedOnException,
    SemanticDifference,
)


class RemoveDictKeysProposer(Proposer, TypeConditions):
    """AST walker that proposes refactorings for dictionaries."""

    def enter_for(self, node: For) -> None:
        if attribute := self.get_keys_attribute(node.iter):
            self.propose(RemoveDictKeysProposal(self.ast, attribute))

    def enter_compare(self, node: Compare) -> None:
        if node.ops == (Compare.IN,) and (
            attribute := self.get_keys_attribute(node.comparators[0])
        ):
            self.propose(RemoveDictKeysProposal(self.ast, attribute))

    def enter_comprehension(self, node: Comprehension) -> None:
        if attribute := self.get_keys_attribute(node.iter):
            self.propose(RemoveDictKeysProposal(self.ast, attribute))

    def get_keys_attribute(self, node: Node) -> Optional[Attribute]:
        if (
            isinstance(node, Call)
            and not node.args
            and isinstance(node.func, Attribute)
            and self.has_dict_type(node.func.value)
        ):
            attribute = node.func
            if attribute.attr.id == "keys":
                return attribute
        return None


class RemoveDictKeysProposal(Proposal):
    """Replace calls to dict.keys() with dict."""

    def __init__(self, ast: AST, node: Attribute) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return REMOVE_KEYS_DESC

    def execute(self) -> None:
        self.node.parent.replace(self.node.value)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {
            FunctionCallsOnException,
            ExceptionRemoved,
            ExceptionTypeChanged,
            ExceptionArgsChanged,
            ReturnValuesChangedOnException,
        }
