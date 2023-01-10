import functools
import typing
from typing import List

from lib.version import PythonVersion
from sourcery.ast import Constant, Expression, Node
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.f_string_conditions import FStringConditions
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType

Quote = typing.Literal["'", '"']


# pylint: disable=too-many-ancestors
class UseFstringForFormattingProposer(
    DSLProposer, DependencyConditions, FStringConditions, LiteralConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${s | is_suitable_f_string}.format($arg{
                        args+ | self.is_suitable_args(args, s)
                    })
                """,
                replacement="""
                    ${self.create_fstring(s, args, "{}")}
                """,
            )
        ]

    def description(self) -> str:
        return "Replace call to format with f-string"

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=6)

    def is_suitable_f_string(self, node: Node):
        return (
            self.is_str_literal(node)
            and node.value.isprintable()
            and set(parse_fstring(node.value)) == {"{}"}
        )

    def is_suitable_args(self, args: typing.List[Expression], s: Constant):
        if len(args) < s.value.count("{}"):
            return False

        return self.is_valid_fstring_expression(args)

    def kind(self) -> RuleType:
        return RuleType.REFACTORING


def parse_fstring(fstring: str) -> typing.List[str]:
    """Returns a list of format string groups inside `fstring`.

    Examples:
        >>> parse_fstring("Hello, {}")
        ["{}"]
        >>> parse_fstring("Amount ({currency}): {amount:.{rounding}f}")
        ["{currency}", "{rounding}", "{amount:.{rounding}f}"]
    """
    # make mypy happy
    initial_groups: typing.List[str] = []
    initial_stack: typing.List[str] = []
    groups: typing.List[str]
    groups, _ = functools.reduce(
        _parse_fstring_char, fstring, (initial_groups, initial_stack)
    )
    return groups


def _parse_fstring_char(
    result: typing.Tuple[typing.List[str], typing.List[str]], char: str
) -> typing.Tuple[typing.List[str], typing.List[str]]:
    """Reducer for `parse_fstring`.

    In `result`, `groups` is a list of closed groups, and `group_stack` is a list of
    currently-open groups. The new character `char` is added to each group in the
    currently-open groups. If it is an open brace, a new group is added. If it is a
    closed brace, the closing group is moved from the open groups to the closed groups.

    Examples:
        For the string `"x{y.{z}f}"`, the reducer returns the following in turn:
        ```
            x -> ([], [])
            { -> ([], ["{"])
            y -> ([], ["{y"])
            . -> ([], ["{y."])
            { -> ([], ["{y.{", "{"])
            z -> ([], ["{y.{z", "{z"])
            } -> (["{z}"], ["{y.{z}"])
            f -> (["{z}"], ["{y.{z}f"])
            } -> (["{z}", "{y.{z}f}"], [])
        ```
    """
    groups, group_stack = result
    new_group_stack = [g + char for g in group_stack]
    if char == "{":
        return groups, [*new_group_stack, char]
    if char == "}" and new_group_stack:
        return [*groups, new_group_stack[-1]], new_group_stack[:-1]
    return groups, new_group_stack
