import functools
import itertools
import typing

from typing_extensions import TypeGuard

from sourcery import ast
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class HoistRepeatedIfConditionProposer(DSLProposer, DependencyConditions):
    def create_code_changes(self) -> typing.List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    if ${a | not self.writes_any_variables(a)}:
                        ${statements_a+}
                    if ${b | self.is_and_boolop_starting_with(b, a)}:
                        ${statements_b+}
                """,
                replacement="""
                    if ${a}:
                        ${statements_a}
                        if ${self.boolop_without(b, a)}:
                            ${statements_b}
                """,
                top_level_condition=self.not_first_statement_writes_first_condition,
            ),
            CodeChange(
                pattern="""
                    if ${a | is_and_boolop_without_writes}:
                        ${statements_a+}
                    if ${b | self.is_and_boolop_starting_with(a, b)}:
                        ${statements_b+}
                """,
                replacement="""
                    if ${b}:
                        if ${self.boolop_without(a, b)}:
                            ${statements_a}
                        ${statements_b}
                """,
                top_level_condition=self.not_first_statement_writes_first_condition,
            ),
            CodeChange(
                pattern="""
                    if ${a | is_and_boolop_without_writes}:
                        ${statements_a+}
                    if ${b | self.are_intersecting_and_boolops(a, b)}:
                        ${statements_b+}
                """,
                replacement="""
                    if ${self.boolop_initial_intersection(a, b)}:
                        if ${self.boolop_initial_diff(a, b)}:
                            ${statements_a}
                        if ${self.boolop_initial_diff(b, a)}:
                            ${statements_b}
                """,
                top_level_condition=self.not_first_statement_writes_first_condition,
            ),
        ]

    def description(self) -> str:
        return "Hoist a repeated condition into a parent condition"

    def not_first_statement_writes_first_condition(
        self, node: ast.Node
    ) -> TypeGuard[ast.If]:
        assert isinstance(node, ast.If)
        return not self.writes_any_variables(node, node.test)

    def are_intersecting_and_boolops(self, left: ast.Node, right: ast.Node) -> bool:
        return (
            is_and_boolop(left)
            and is_and_boolop(right)
            and self.is_and_boolop_starting_with(left, right.values[0])
        )

    def is_and_boolop_without_writes(self, node: ast.Node) -> TypeGuard[ast.BoolOp]:
        """True if `node` is a "pure" boolop."""
        return is_and_boolop(node) and not any(
            self.writes_any_variables(v) for v in node.values
        )

    def is_and_boolop_starting_with(self, node: ast.Node, other: ast.Node) -> bool:
        """True if `node` is a boolop whose first value is `other`."""
        assert isinstance(other, ast.Expression)

        if not is_and_boolop(node):
            return False

        if is_and_boolop(other):
            return nodes_equivalent(
                other, self.boolop_initial_intersection(node, other)
            )
        else:
            return value_is_first_boolop_value(other, node)

    def boolop_without(self, node: ast.BoolOp, other: ast.Expression) -> ast.Expression:
        """Return a boolop, skipping `other` if it's the first value."""
        if not self.is_and_boolop_starting_with(node, other):
            return node

        values = (
            node.values[len(other.values) :]
            if is_and_boolop(other)
            else node.values[1:]
        )

        if len(values) == 1:
            return values[0]

        return ast.BoolOp(ast.BoolOp.AND, values=values)

    @staticmethod
    def boolop_initial_intersection(
        left: ast.BoolOp, right: ast.BoolOp
    ) -> ast.Expression:
        """Return a boolop of values that are initial values of `left` and `right`."""
        common_values = get_common_values(left, right)
        if len(common_values) == 1:
            return common_values[0]
        return ast.BoolOp(ast.BoolOp.AND, values=common_values)

    @staticmethod
    def boolop_initial_diff(left: ast.BoolOp, right: ast.BoolOp) -> ast.Expression:
        """Return a boolop of `left`'s values that are not initial values of `right`."""
        left_unique_values = get_unique_values(left, right)

        if len(left_unique_values) == 1:
            return left_unique_values[0]

        return ast.BoolOp(ast.BoolOp.AND, values=left_unique_values)

    def kind(self) -> RuleType:
        return RuleType.REFACTORING


def get_common_values(
    left: ast.BoolOp, right: ast.BoolOp
) -> typing.Tuple[ast.Expression, ...]:
    """Return values from `left` while they are in `right`."""
    value_in_right_values = functools.partial(value_in_boolop_values, boolop=right)
    return tuple(itertools.takewhile(value_in_right_values, left.values))


def get_unique_values(
    left: ast.BoolOp, right: ast.BoolOp
) -> typing.Tuple[ast.Expression, ...]:
    """Return values from `left` after skipping common values with `right`."""
    value_in_right_values = functools.partial(value_in_boolop_values, boolop=right)
    return tuple(itertools.dropwhile(value_in_right_values, left.values))


def value_in_boolop_values(value: ast.Expression, boolop: ast.BoolOp) -> bool:
    """True if `value` is equivalent to any value of `boolop`."""
    return any(nodes_equivalent(value, v) for v in boolop.values)


def value_is_first_boolop_value(value: ast.Expression, boolop: ast.BoolOp) -> bool:
    """True if `value` is equivalent to the first value of `boolop`."""
    return nodes_equivalent(value, boolop.values[0])


def nodes_equivalent(left: ast.Node, right: ast.Node) -> bool:
    """True if `left` is equivalent to `right`."""
    return hash(left) == hash(right)


def is_and_boolop(node: ast.Node) -> TypeGuard[ast.BoolOp]:
    """True if `node` is a boolop."""
    return isinstance(node, ast.BoolOp) and node.op == ast.BoolOp.AND
