"""Filter expression parsing and evaluation."""
import abc
import operator
import re
import typing as t
from datetime import datetime
from functools import partial

from .datetime import get_datetime
from .dicts import get_field
from .parsers import parse_hrsize

__all__ = [
    "BaseFilter",
    "ExpressionFilter",
    "Filters",
    "IncludeExcludeFilter",
    "NumberFilter",
    "SetFilter",
    "SizeFilter",
    "StringFilter",
    "TimeFilter",
]


def eq_tilde(value: str, pattern: t.Pattern) -> bool:
    """Return True if the regex pattern matches the value."""
    return bool(pattern.search(value))


def ne_tilde(value: str, pattern: t.Pattern) -> bool:
    """Return True if the regex pattern does not match the value."""
    return not eq_tilde(value, pattern)


OPERATORS: t.Dict[str, t.Callable] = {
    "=~": eq_tilde,
    "!~": ne_tilde,
    "<=": operator.le,
    ">=": operator.ge,
    "!=": operator.ne,
    "=": operator.eq,
    "<": operator.lt,
    ">": operator.gt,
}

STRING_OPS = list(OPERATORS)
COMMON_OPS = list(OPERATORS)[2:]


Filters = t.List[str]


class BaseFilter(abc.ABC):
    """Base filter class defining the filter interface."""

    @abc.abstractmethod
    def match(self, value) -> bool:
        """Return True if the filter matches value."""


class ExpressionFilter(BaseFilter):
    """Expression filter tied to a field, operator and value."""

    operators: t.ClassVar[t.List[str]] = COMMON_OPS

    def __init__(self, field: str, op: str, value: str) -> None:
        """Initialize an expression filter."""
        if op not in self.operators:
            expected = "|".join(self.operators)
            raise ValueError(f"invalid operator: {op} (expected {expected})")
        self.field = field
        self.op = op
        self.value = value

    def __str__(self) -> str:
        """Return human-readable stringification (the original expression)."""
        return f"{self.field}{self.op}{self.value}"

    def __repr__(self) -> str:
        """Return the filter's string representation."""
        cls_args = self.field, self.op, self.value
        return f"{self.__class__.__name__}{cls_args!r}"

    def getval(self, value):
        """Return attribute of the value."""
        return get_field(value, self.field)


class IncludeExcludeFilter(BaseFilter):
    """Filter supporting multiple include- and exclude expressions."""

    def __init__(
        self,
        factory: t.Dict[str, t.Type[ExpressionFilter]],
        *,
        include: Filters = None,
        exclude: Filters = None,
        validate: t.Callable[[str], str] = None,
    ) -> None:
        """Init a complex filter from multiple include- and exclude expressions.

        Args:
            factory: Field name to filter class mapping used as a factory.
            include: List of include exprs - if given, at least one must match.
            exclude: List of exclude exprs - if given, none are allowed to match.
            validate: Field name validator callback.
        """
        parse = partial(parse_filter_expression, factory=factory, validate=validate)
        self.include = [parse(expr) for expr in (include or [])]
        self.exclude = [parse(expr) for expr in (exclude or [])]

    # pylint: disable=arguments-differ
    def match(self, value, exclude_only: t.List[str] = None) -> bool:
        """Return whether value matches all includes but none of the excludes.

        If `exclude_only` is given, only evaluate the exclude filters on those.
        """
        include = self.include
        exclude = self.exclude
        if exclude_only:
            include = []
            exclude = [filt for filt in exclude if filt.field in exclude_only]
        include_match = (i.match(value) for i in include)
        exclude_match = (e.match(value) for e in exclude)
        return (not include or any(include_match)) and not any(exclude_match)

    def __repr__(self) -> str:
        """Return string representation of the filter object."""
        cls_name = self.__class__.__name__
        include = ",".join(f"'{filt}'" for filt in self.include)
        exclude = ",".join(f"'{filt}'" for filt in self.exclude)
        return f"{cls_name}(include=[{include}], exclude=[{exclude}])"


class NumberFilter(ExpressionFilter):
    """Number filter."""

    operators = COMMON_OPS

    def __init__(self, field: str, op: str, value: str) -> None:
        """Initialize number filter from str value."""
        super().__init__(field, op, value)
        self.num = float(value)

    def match(self, value: t.Union[int, float, t.Any]) -> bool:
        """Compare number to the filter value."""
        value = value if isinstance(value, (int, float)) else self.getval(value)
        if value is None:
            return False
        return OPERATORS[self.op](value, self.num)


class SetFilter(ExpressionFilter):
    """Set filter."""

    operators = ["=", "!="]  # ie. in / not in

    def __init__(self, field: str, op: str, value: str) -> None:
        """Initialize set filter from str value."""
        super().__init__(field, op, value.lower())

    def match(self, value: t.Union[list, set, t.Any]) -> bool:
        """Return that the given item is in the given list/set."""
        values = value if isinstance(value, (list, set)) else self.getval(value)
        if not values:
            return False
        return OPERATORS[self.op](self.value in [v.lower() for v in values], True)


class StringFilter(ExpressionFilter):
    """String filter."""

    operators = STRING_OPS
    string: t.Union[str, t.Pattern]

    def __init__(self, field: str, op: str, value: str) -> None:
        """Initialize string filter from a literal or regex pattern."""
        super().__init__(field, op, value)
        if "~" not in op:
            self.string = value
            return
        try:
            self.string = re.compile(value)
        except re.error as exc:
            raise ValueError(f"Invalid pattern: {value} - {exc}") from exc

    def match(self, value: t.Union[str, t.Any]) -> bool:
        """Match str with the filter's regex pattern."""
        string = value if isinstance(value, str) else self.getval(value)
        if string is None:
            return False
        return OPERATORS[self.op](string, self.string)


class SizeFilter(ExpressionFilter):
    """Size filter."""

    operators = COMMON_OPS

    def __init__(self, field: str, op: str, value: str) -> None:
        """Initialize size filter from a human-readable size."""
        super().__init__(field, op, value)
        self.size = parse_hrsize(value)

    def match(self, value: t.Union[int, t.Any]) -> bool:
        """Compare size to the filter value."""
        size = value if isinstance(value, int) else self.getval(value)
        if size is None:
            return False
        return OPERATORS[self.op](size, self.size)


class TimeFilter(ExpressionFilter):
    """Time filter."""

    operators = COMMON_OPS
    timestamp_re = re.compile(
        r"(?P<year>\d\d\d\d)([-_/]?"
        r"(?P<month>\d\d)([-_/]?"
        r"(?P<day>\d\d)([-_/T ]?"
        r"(?P<hour>\d\d)([-_:]?"
        r"(?P<minute>\d\d)([-_:]?"
        r"(?P<second>\d\d)?)?)?)?)?)?"
    )

    def __init__(self, field: str, op: str, value: str) -> None:
        """Initialize time filter from an iso-format timestamp."""
        super().__init__(field, op, value)
        match = self.timestamp_re.match(value)
        if not match:
            raise ValueError(f"invalid time: {value!r} (expected YYYY-MM-DD HH:MM:SS)")
        if match.group("second"):
            self.time = get_datetime(value).strftime("%Y%m%d%H%M%S")
        else:
            self.time = "".join(part or "" for part in match.groupdict().values())

    def match(self, value: t.Union[int, str, datetime, t.Any]) -> bool:
        """Compare timestamp to the filter value."""
        if not isinstance(value, (str, int, datetime)):
            value = self.getval(value)
        if value is None:
            return False
        time_str = get_datetime(value).strftime("%Y%m%d%H%M%S")
        return OPERATORS[self.op](time_str[: len(self.time)], self.time)


def parse_filter_expression(
    expression: str,
    factory: t.Dict[str, t.Type[ExpressionFilter]],
    validate: t.Callable[[str], str] = None,
) -> ExpressionFilter:
    """Parse and return filter from expression string (factory)."""
    expr_split = re.split(rf"({'|'.join(OPERATORS)})", expression, maxsplit=1)
    if len(expr_split) != 3:
        raise ValueError(f"invalid filter expression: {expression}")
    field, op, value = expr_split
    field = validate(field) if validate else field
    filter_cls: t.Type[ExpressionFilter] = StringFilter
    for k, filter_cls in factory.items():
        if field == k or k.endswith("*") and field.startswith(k[:-1]):
            break
    return filter_cls(field, op, value)
