from sourcery.ast import AST, Compare, Constant, List, Set, Tuple
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import CONSTANT_COLL_DESC


class CollectionIntoSetProposer(Proposer, TypeConditions):
    """AST walker that proposes enhancements related to sets."""

    def enter_compare(self, node: Compare) -> None:
        if (
            len(node.ops) == 1
            and node.ops[0] == Compare.IN
            and isinstance(node.comparators[0], (List, Tuple))
            and all(isinstance(elt, Constant) for elt in node.comparators[0].elts)
            and self.has_simple_type(node.left)
        ):
            self.propose(CollectionIntoSetProposal(self.ast, node))


class CollectionIntoSetProposal(Proposal):
    def __init__(self, ast: AST, node: Compare) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return CONSTANT_COLL_DESC

    def execute(self) -> None:
        assert isinstance(self.node.comparators[0], (List, Tuple))
        self.node.comparators = (Set(self.node.comparators[0].elts),)
