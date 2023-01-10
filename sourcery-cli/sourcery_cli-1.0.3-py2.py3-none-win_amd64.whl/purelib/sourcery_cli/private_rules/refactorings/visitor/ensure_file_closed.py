"""Use `with` when opening file to ensure closure."""

from sourcery.analysis.variable_usage import VariableUsage, possible_assignments
from sourcery.ast import (
    AST,
    Assign,
    Attribute,
    Block,
    Call,
    Expr,
    Name,
    Node,
    With,
    Withitem,
    is_single_target_assign,
)
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import FILE_CLOSURE_DESC


class EnsureFileClosedProposer(Proposer):
    """Opens files using the with context manager syntax."""

    var_usages: VariableUsage

    def enter_assign(self, node: Assign):
        if (
            is_single_target_assign(node)
            and isinstance(node.targets[0], Name)
            and isinstance(node.value, Call)
            and node.value.func.unparse() == "open"
        ):
            file_name = node.targets[0].id
            open_index = node.parent.index(node)
            self.propose_if_file_closed(file_name, node, open_index)

    def propose_if_file_closed(
        self, file_name: str, node: Assign, open_index: int
    ) -> None:
        for index, statement in enumerate(node.parent.statements[open_index + 1 :]):
            if (
                isinstance(statement, Expr)
                and _is_attribute_call(statement.value, "close", file_name)
                and index > 0
            ):
                self.propose(
                    EnsureFileClosedProposal(
                        self.ast, node, open_index, open_index + index + 1
                    )
                )
            elif file_name in possible_assignments(self.var_usages[statement]):
                break


class EnsureFileClosedProposal(Proposal):
    """Convert file open into open using with syntax."""

    def __init__(
        self, ast: AST, node: Assign, open_index: int, close_index: int
    ) -> None:
        self.ast = ast
        self.node = node
        self.open_index = open_index
        self.close_index = close_index

    def description(self):
        return FILE_CLOSURE_DESC

    def execute(self) -> None:
        new_with = With(
            (Withitem(self.node.value, self.node.targets[0]),),
            Block(self.node.parent.statements[self.open_index + 1 : self.close_index]),
            is_async=False,
        )
        self.node.parent[self.open_index : self.close_index + 1] = (new_with,)


def _is_attribute_call(node: Node, call: str, value: str) -> bool:
    return (
        isinstance(node, Call)
        and isinstance(node.func, Attribute)
        and node.func.attr.id == call
        and node.func.value.unparse() == value
    )
