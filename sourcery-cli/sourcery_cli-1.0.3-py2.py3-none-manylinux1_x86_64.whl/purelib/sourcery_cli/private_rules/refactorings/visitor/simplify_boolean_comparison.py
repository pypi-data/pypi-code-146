from sourcery.ast import AST, Compare, Constant
from sourcery.ast.ast import invert_condition
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import SIMPLIFY_BOOL_COMP_DESC


class SimplifyBooleanComparisonProposer(Proposer, TypeConditions):
    """AST walker that proposes simplifying Compare nodes."""

    def enter_compare(self, node: Compare):
        if self.is_valid_bool_compare(node):
            self.propose(SimplifyBooleanComparisonProposal(self.ast, node))

    def is_valid_bool_compare(self, node: Compare) -> bool:
        return (
            len(node.ops) == 1
            and node.ops[0] in [Compare.EQ, Compare.NOT_EQ, Compare.IS, Compare.IS_NOT]
            and isinstance(node.comparators[0], Constant)
            and node.comparators[0].type == bool
            and self.has_bool_type(node.left)
        )


class SimplifyBooleanComparisonProposal(Proposal):
    """Simplify if x == True into if x.

    x == True -> x
    x == False -> not x
    x != True -> not x
    x != False -> x
    """

    def __init__(self, ast: AST, node: Compare) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return SIMPLIFY_BOOL_COMP_DESC

    def execute(self) -> None:
        if self.should_invert(self.node):
            self.node.replace(invert_condition(self.node.left))
        else:
            self.node.replace(self.node.left)

    def should_invert(self, node: Compare):
        assert isinstance(node.comparators[0], Constant)
        return (
            node.ops[0] in [Compare.IS_NOT, Compare.NOT_EQ]
            and node.comparators[0].value
        ) or (node.ops[0] in [Compare.IS, Compare.EQ] and not node.comparators[0].value)
