from sourcery.analysis.node_statements import NodeStatements
from sourcery.ast import AST, Block, If
from sourcery.ast.ast import body_breaks_flow
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import REINTRODUCE_ELSE


class ReintroduceElseProposer(Proposer):
    """AST walker that proposes adding the else after a guard condition."""

    node_statements: NodeStatements

    def enter_if(self, node: If):
        if body_breaks_flow(node) and len(node.body) == 1:
            # Check only one statement follows the if so we're not the opposite
            # of remove-unnecessary-else
            next_statement = node.next_sibling()
            if (
                next_statement
                and not next_statement.next_sibling()
                and self.node_statements[next_statement] == 1
            ):
                self.propose(ReintroduceElseProposal(self.ast, node))


class ReintroduceElseProposal(Proposal):
    def __init__(self, ast: AST, node: If) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return REINTRODUCE_ELSE

    def transient(self) -> bool:
        return True

    def execute(self) -> None:
        index = self.node.parent.index(self.node)
        self.node.orelse = Block(self.node.parent.statements[index + 1 :])
        self.node.parent.statements = self.node.parent.statements[: index + 1]
