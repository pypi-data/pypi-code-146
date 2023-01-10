import typing

from sourcery.analysis.typing.exception_types import exception_tree
from sourcery.ast import AST
from sourcery.ast.nodes import ExceptHandler, Expression, Name, Node, Try, Tuple
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import MERGE_EXCEPT_HANDLERS_DESC


class MergeExceptHandlerProposer(Proposer):
    def enter_try(self, node: Try):
        index = 0
        for h1, h2 in zip(node.handlers, node.handlers[1:]):
            if h1.type is None or h2.type is None:
                # skip bare-except
                continue

            if self.contains_unknown_exception(h1) or self.contains_unknown_exception(
                h2
            ):
                # skip all unknown names (custom-exceptions and named-tuples)
                continue

            if (
                hash(h1.body) == hash(h2.body)
                and getattr(h1.name, "id", None) == getattr(h2.name, "id", None)
                and h1.body.unparse() == h2.body.unparse()
            ):
                self.propose(MergeExceptHandlerProposal(self.ast, node, index))

            index += 1

    def contains_unknown_exception(self, handler: ExceptHandler):
        if isinstance(handler.type, Tuple):
            return any(
                not (isinstance(h, Name) and exception_tree().get(h.id))
                for h in handler.type.elts
            )
        elif isinstance(handler.type, Name):
            return not exception_tree().get(handler.type.id)
        else:
            return True


class MergeExceptHandlerProposal(Proposal):
    def __init__(self, ast: AST, node: Try, index: int) -> None:
        self.ast = ast
        self.node = node
        self.index = index

    def description(self) -> str:
        return MERGE_EXCEPT_HANDLERS_DESC

    def target_nodes(self) -> typing.Tuple[Node, ...]:
        return tuple(self.node.handlers[self.index : self.index + 2])

    def execute(self) -> None:
        new_handler: typing.Tuple[Expression, ...] = ()

        for handler in self.node.handlers[self.index : self.index + 2]:
            if isinstance(handler.type, Tuple):
                new_handler += handler.type.elts
            else:
                new_handler += (handler.type,)  # type: ignore

        self.node.edit_tuple("handlers", lambda handlers: handlers.pop(self.index + 1))
        self.node.handlers[self.index].type = Tuple(new_handler)
