import typing

from sourcery import ast
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class RemoveRedundantBooleanProposer(DSLProposer, DependencyConditions):
    def create_code_changes(self) -> typing.List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    not False
                """,
                replacement="""
                    True
                """,
                top_level_condition=is_in_valid_location,
            ),
            CodeChange(
                pattern="""
                    not True
                """,
                replacement="""
                    False
                """,
                top_level_condition=is_in_valid_location,
            ),
            CodeChange(
                pattern="""
                    $boolop{left*} and True and $boolop{right*}
                """,
                replacement="""
                    ${self.make_boolop(left, right, ast.BoolOp.AND)}
                """,
                top_level_condition=is_in_valid_location,
            ),
            CodeChange(
                pattern="""
                    $boolop{
                        left* | not self.writes_any_variables(left)
                    } or True or $boolop{right* | not self.writes_any_variables(right)}
                """,
                replacement="""
                    True
                """,
                top_level_condition=is_in_valid_location,
            ),
            CodeChange(
                pattern="""
                    $boolop{
                        left* | not self.writes_any_variables(left)
                    } and False and $boolop{
                        right* | not self.writes_any_variables(left)
                    }
                """,
                replacement="""
                    False
                """,
                top_level_condition=is_in_valid_location,
            ),
            CodeChange(
                pattern="""
                    $boolop{left*} or False or $boolop{right*}
                """,
                replacement="""
                    ${self.make_boolop(left, right, ast.BoolOp.OR)}
                """,
                top_level_condition=is_in_valid_location,
            ),
        ]

    def description(self) -> str:
        return "Removes or propagates redundant boolean expressions"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def make_boolop(
        self,
        left_values: typing.Tuple[ast.Expression],
        right_values: typing.Tuple[ast.Expression],
        op: ast.BoolOp.Op,
    ) -> ast.Expression:
        if left_values and right_values:
            return ast.BoolOp(op, left_values + right_values)
        if len(left_values) > 1:
            return ast.BoolOp(op, left_values)
        if len(right_values) > 1:
            return ast.BoolOp(op, right_values)
        if len(left_values) == 1:
            return left_values[0]
        if len(right_values) == 1:
            return right_values[0]
        raise RuntimeError("Logic error.")  # pragma: no cover


Condition = typing.Callable[[ast.Node], bool]


def is_in_valid_location(node: ast.Node) -> bool:
    """Returns True anywhere the parent coerces to boolean...

    Except where it's also an ``If`` node, because that refactoring is handled by
    ``remove-redundant-if``.
    """
    parent_is_not_if = not_(parent_is_if)
    overall_condition = allof(ast.parent_coerces_to_bool, parent_is_not_if)
    return overall_condition(node)


def allof(*conditions: Condition) -> Condition:
    def unified_condition(node: ast.Node) -> bool:
        return all(condition(node) for condition in conditions)

    return unified_condition


def parent_is_if(node: ast.Node) -> bool:
    return isinstance(node.parent, ast.If)


def not_(condition: Condition) -> Condition:
    def inverted_condition(node: ast.Node) -> bool:
        return not condition(node)

    return inverted_condition
