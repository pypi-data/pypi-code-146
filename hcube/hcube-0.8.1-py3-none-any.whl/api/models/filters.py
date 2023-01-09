import abc
from enum import Enum
from typing import Any, Union

from hcube.api.models.dimensions import Dimension


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
