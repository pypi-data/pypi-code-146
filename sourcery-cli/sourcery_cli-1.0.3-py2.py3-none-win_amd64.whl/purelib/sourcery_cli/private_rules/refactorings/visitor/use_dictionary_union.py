import functools
import typing

from lib.version import PythonVersion
from sourcery.ast import AST, Expression, nodes
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.engine.rule_type import RuleType


class UseDictionaryUnionProposer(Proposer, TypeConditions):
    def enter_dict(self, dict_node: nodes.Dict) -> None:
        if len(dict_node.keys) <= 1:
            # Empty dictionaries are not relevant.
            # a = {}  ❌
            # Also don't want to do anything with single-length dicts (it's a copy)
            # a = {**b}  ❌
            return
        if any(key is not None for key in dict_node.keys):
            # Only apply if every value is unpacked.
            # x = {**a, **b}  ✔
            # x = {"foo": "bar", **a}  ❌
            return
        if any(not self.has_dict_type(value) for value in dict_node.values):
            # Don't apply for non-dicts, e.g. defaultdicts, as this changes
            # the result type
            return
        if any(isinstance(value, nodes.Dict) for value in dict_node.values):
            # Don't apply for literal dictionaries
            # x = {"foo": "bar", **{"bar": "foo"}}  ❌
            return

        self.propose(UseDictionaryUnionProposal(self.ast, dict_node, dict_node.values))


class UseDictionaryUnionProposal(Proposal):
    def description(self) -> str:
        return "Applies the dictionary union operator where applicable"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=9)

    def __init__(
        self,
        ast: AST,
        node: nodes.Dict,
        values: typing.Tuple[Expression, ...],
    ):
        self.ast = ast
        self.node = node
        self.values = values

    def execute(self) -> None:
        final = make_unions(*self.values)
        self.node.replace(final)


def make_unions(*expressions: nodes.Expression) -> Expression:
    """Create a "union" operation from the expressions.

    Examples:
        >>> node_list = [nodes.Name(s) for s in "abcde"]
        >>> make_unions(*node_list).unparse()
        a | b | c | d | e
    """
    initial, *remainder = expressions
    return functools.reduce(make_union, remainder, initial)


def make_union(left: nodes.Expression, right: nodes.Expression) -> nodes.BinOp:
    """Create a "union" operation from the left and right expressions.

    Examples:
        >>> left = nodes.Name("a")
        >>> right = nodes.Name("b")
        >>> make_union(left, right).unparse()
        a | b
    """
    return nodes.BinOp(left=left, right=right, op=nodes.BinOp.BIT_OR)
