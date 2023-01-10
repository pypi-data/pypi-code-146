from sourcery.ast.ast import AST
from sourcery.ast.nodes import Constant, FormattedValue, JoinedStr
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import (
    REMOVE_REDUNDANT_FSTRING_DESC,
)


class RemoveRedundantFstringProposer(Proposer):
    def enter_joinedstr(self, node: JoinedStr):
        if (
            len(node.values) == 1
            and isinstance(node.values[0], Constant)
            and not isinstance(node.parent, FormattedValue)
            # A quick fix, so that we don't incorrectly refactor f-strings containing
            # escaped curly braces.
            # For example:
            # f"{{I want curly braces.}}"
            # A better solution would be:
            # If the f-string is redundant, replace:
            # {{ => {
            # }} => }
            and "{{" not in node.unparse()
            and "\\" not in node.unparse()
        ):
            self.propose(RemoveRedundantFstringProposal(self.ast, node))


class RemoveRedundantFstringProposal(Proposal):
    """Alter constant only fstrings to be normal strings."""

    def __init__(self, ast: AST, node: JoinedStr):
        self.ast = ast
        self.node = node

    def description(self) -> str:
        return REMOVE_REDUNDANT_FSTRING_DESC

    def execute(self) -> None:
        self.node.replace(self.node.values[0])
