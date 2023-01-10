import collections
import typing

from sourcery.ast import AST, ExceptHandler, Name, Node, Raise
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.engine.rule_type import RuleType

exception_names = [
    "e",
    "exc",
    "err",
    "exception",
    "error",
    "an_exception",
    "an_error",
    "some_exception",
    "some_error",
]


class RaiseFromPreviousErrorProposer(Proposer, DependencyConditions):
    excepthandler_stack: collections.OrderedDict[ExceptHandler, typing.List[Raise]]

    def __init__(self) -> None:
        self.excepthandler_stack = collections.OrderedDict()

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION

    @property
    def last_excepthandler(self):
        return next(reversed(self.excepthandler_stack))

    @property
    def active_raise_statement_list(self):
        return self.excepthandler_stack[self.last_excepthandler]

    def reset(self, ast: AST) -> None:
        super().reset(ast)
        self.excepthandler_stack = collections.OrderedDict()

    def enter_excepthandler(self, excepthandler: ExceptHandler):
        self.excepthandler_stack[excepthandler] = []

    def leave_excepthandler(self, excepthandler: ExceptHandler):
        raise_statements = self.excepthandler_stack[excepthandler]
        causeless_raise_statements = [
            raise_statement
            for raise_statement in raise_statements
            if raise_statement.exc
            and not raise_statement.cause
            and not (
                # make sure that we avoid suggesting `raise e from e` by checking if the
                # raise statement's exception is not equal to the exception handler's
                # name
                excepthandler.name
                and raise_statement.exc.unparse() == excepthandler.name.id
            )
        ]

        exception_name = next(  # pragma: no cover
            (
                exception_name
                for exception_name in exception_names
                if not self.is_in_scope_of(exception_name, excepthandler)
            ),
            "e",
        )

        if causeless_raise_statements:
            self.propose(
                RaiseFromPreviousErrorProposal(
                    self.ast,
                    excepthandler=excepthandler,
                    causeless_raise_statements=causeless_raise_statements,
                    exception_name=exception_name,
                )
            )
        self.excepthandler_stack.popitem()

    def leave_raise(self, raise_statement: Raise):
        if (
            self.excepthandler_stack  # we're in an exception
            and self.last_excepthandler.type  # it's a specific exception
        ):
            self.active_raise_statement_list.append(raise_statement)


class RaiseFromPreviousErrorProposal(Proposal):
    def __init__(
        self,
        ast: AST,
        excepthandler: ExceptHandler,
        causeless_raise_statements: typing.List[Raise],
        exception_name: str,
    ):
        self.ast = ast
        self.excepthandler = excepthandler
        self.causeless_raise_statements = causeless_raise_statements
        self.exception_name = exception_name

    def description(self) -> str:
        return "Explicitly raise from a previous error"

    def target_nodes(self) -> typing.Tuple[Node, ...]:
        return (self.excepthandler,)

    def execute(self) -> None:
        if not self.excepthandler.name:
            self.excepthandler.name = Name(self.exception_name)

        for raise_statement in self.causeless_raise_statements:
            raise_statement.cause = self.excepthandler.name

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION
