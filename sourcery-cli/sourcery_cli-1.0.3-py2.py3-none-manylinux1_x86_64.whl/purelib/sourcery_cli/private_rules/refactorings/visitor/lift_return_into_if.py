from typing import List

from sourcery.ast import AST, Assign, If, Name, Node, Return
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import LIFT_RETURN_INTO_IF_DESC


class LiftReturnIntoIfProposer(Proposer, DependencyConditions):
    """Inlines assigns that are in all if branches and then get returned immediately."""

    def enter_if(self, node: If):
        next_sibling = node.next_sibling()
        if (
            node.body
            and node.orelse
            and next_sibling
            and isinstance(next_sibling, Return)
            and next_sibling.value
        ):
            return_value = next_sibling.value
            last_statements = self.last_statements(node)
            if isinstance(return_value, Name) and all(
                self.is_matching_assign(element, return_value)
                for element in last_statements
            ):
                self.propose(
                    LiftReturnIntoIfProposal(
                        self.ast, node, next_sibling, last_statements
                    )
                )

    def last_statements(self, node: If):
        last_elements = [node.body[-1], node.orelse[-1]]
        last_elements.extend(elif_.body[-1] for elif_ in node.elifs)
        return last_elements

    def is_matching_assign(self, element: Node, return_value: Node):
        return (
            isinstance(element, Assign)
            and len(element.targets) == 1
            and hash(element.targets[0]) == hash(return_value)
            and not self.writes_to_global_state(element.targets[0])
        )


class LiftReturnIntoIfProposal(Proposal):
    def __init__(
        self,
        ast: AST,
        node: If,
        return_to_inline: Return,
        last_statements: List[Assign],
    ) -> None:
        self.ast = ast
        self.node = node
        self.return_to_inline = return_to_inline
        self.last_statements = last_statements

    def description(self):
        return LIFT_RETURN_INTO_IF_DESC

    def execute(self) -> None:
        self.node.parent.remove(self.return_to_inline)
        for assign in self.last_statements:
            assign.replace(Return(assign.value))
