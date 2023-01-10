from functools import reduce

from typing_extensions import TypeGuard

from sourcery.ast import Constant, Expression, FormattedValue, JoinedStr, Node
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class SimplifyFstringFormattingProposer(DSLProposer):
    def create_code_changes(self) -> list[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${fstring | (
                            self.is_fstring(fstring)
                            and self.contains_formatted_value(fstring)
                            and self.is_ascii(fstring)
                        )
                    }
                """,
                replacement="${simplify_fstring(fstring)}",
            )
        ]

    def contains_formatted_value(self, fstring: JoinedStr) -> bool:
        return any(
            isinstance(n, FormattedValue) and _is_reducible_formatted_value(n)
            for n in fstring.values
        )

    def is_ascii(self, fstring: JoinedStr) -> bool:
        return fstring.unparse().isascii()

    def is_fstring(self, fstring: Node) -> TypeGuard[JoinedStr]:
        return isinstance(fstring, JoinedStr)

    def description(self) -> str:
        return "Simplify unnecessary nesting, casting and constant values in f-strings"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING


def simplify_fstring(fstring: JoinedStr) -> JoinedStr:
    fstring.values = tuple(
        reduce(
            collapse_node_value,  # type: ignore
            fstring.values,
            (),
        )
    )
    return fstring


def collapse_node_value(
    values: tuple[Expression, ...], value: Expression
) -> tuple[Expression, ...]:
    """Add a new expression to the values tuple for a formatted value.

    - if it's a constant, and the previous value is a constant, merge them
    - if it's a formatted value, and its sub-value is a formatted value,
      expand the values
    - if it's a formatted value, and its sub-value is a constant, and the
      previous value is a constant, merge the constants
    - otherwise, add the new value to the tuple of values

    Examples:
        >>> collapse_node_value((Constant("foo"), ), Constant("bar"))
        (Constant("foobar"),)
        >>> collapse_node_value((Constant("foo"),), FormattedValue(Constant("bar")))
        (Constant("foobar"),)
        >>> collapse_node_value(
        ...     (FormattedValue(Constant("foo")), ),
        ...     FormattedValue(Constant("bar"))
        ... )
        (FormattedValue(Constant("foo")), FormattedValue(Constant("bar")))
    """
    if not values:
        if (
            isinstance(value, FormattedValue)
            and isinstance(value.value, Constant)
            and _is_simple_formatted_value(value)
        ):
            return (value.value,)
        return (value,)

    *body, tail = values

    if isinstance(value, Constant) and isinstance(tail, Constant):
        return (*body, Constant(str(tail.value) + str(value.value)))

    if isinstance(value, FormattedValue):
        if isinstance(value.value, JoinedStr):
            return (*body, tail, *value.value.values)

        if (
            isinstance(value.value, Constant)
            and isinstance(tail, Constant)
            and _is_simple_formatted_value(value)
        ):
            return (*body, Constant(str(tail.value) + str(value.value.value)))

    return (*body, tail, value)


def _is_reducible_formatted_value(node: FormattedValue) -> bool:
    node_value = node.value
    return (
        # nested fstring
        (isinstance(node_value, JoinedStr) and not node.format_spec)
        # constant
        or (isinstance(node_value, Constant) and _is_simple_formatted_value(node))
    )


def _is_simple_formatted_value(formatted_value: FormattedValue):
    return formatted_value.conversion == -1 and not formatted_value.format_spec
