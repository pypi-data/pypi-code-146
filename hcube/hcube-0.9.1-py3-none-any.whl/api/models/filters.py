import abc
from enum import Enum
from typing import Any, Union

from hcube.api.models.dimensions import ArrayDimension, Dimension
from hcube.api.models.transforms import Transform


class Filter(abc.ABC):
    def __init__(self, dimension: Dimension):
        self.dimension = dimension


class EqualityFilter(Filter):
    def __init__(self, dimension: Dimension, value: Union[str, int]):
        super().__init__(dimension)
        self.value = value


class ListFilter(Filter):
    def __init__(self, dimension: Dimension, values: list):
        super().__init__(dimension)
        self.values = values


class NegativeListFilter(Filter):
    def __init__(self, dimension: Dimension, values: list):
        super().__init__(dimension)
        self.values = values


class IsNullFilter(Filter):
    def __init__(self, dimension: Dimension, is_null: bool):
        super().__init__(dimension)
        self.is_null = is_null


class ComparisonType(Enum):
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="


class ComparisonFilter(Filter):
    def __init__(self, dimension: Dimension, comparison: ComparisonType, value: Any):
        super().__init__(dimension)
        self.comparison = comparison
        self.value = value


class SubstringFilter(Filter):
    def __init__(self, dimension: Dimension, value: str, case_sensitive: bool = True):
        super().__init__(dimension)
        self.value = value
        self.case_sensitive = case_sensitive


class SubstringMultiValueFilter(Filter):
    """
    Represents matching a value against a list of values. If any value matches, the filter matches.
    """

    def __init__(self, dimension: Dimension, values: [str], case_sensitive: bool = True):
        super().__init__(dimension)
        self.values = list(values)
        self.case_sensitive = case_sensitive


class OverlapFilter(Filter):
    """
    Describes overlap between two arrays.
    """

    def __init__(self, dimension: Dimension, values: list):
        if not isinstance(dimension, (ArrayDimension, Transform)):
            raise ValueError(
                "OverlapFilter can only be used with ArrayDimension or a Transform, "
                "'{}' given".format(dimension)
            )
        super().__init__(dimension)
        self.values = list(values)


class Wrapper:
    """
    This is helper class wrapping one filter shorthand.
    """

    def __init__(self, **named_filters):
        if len(named_filters) > 1:
            raise ValueError("Wrapper can only wrap one filter")
        for key, value in named_filters.items():
            self.key = key
            self.value = value


class FilterCombinator(abc.ABC):
    def __init__(self, *filters: Union[Filter, Wrapper]):
        self.filters: list[Filter] = list(filters)


class Or(FilterCombinator):
    pass
