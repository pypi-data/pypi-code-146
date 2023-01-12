from dataclasses import dataclass
from typing import Any
from typing import Dict


@dataclass
class AggregationFunction:
    name: str
    params: Dict[str, Any]


# Last N aggregation that doesn't allow duplicates.
def last_distinct(n: int) -> AggregationFunction:
    return AggregationFunction("lastn", {"n": n})


# Last N aggregation that allows duplicates.
def last(n: int) -> AggregationFunction:
    return AggregationFunction("last_non_distinct_n", {"n": n})


# First N aggregation that doesn't allow duplicates.
def first_distinct(n: int) -> AggregationFunction:
    return AggregationFunction("first_distinct_n", {"n": n})


# First N aggregation that allows duplicates.
def first(n: int) -> AggregationFunction:
    return AggregationFunction("first_non_distinct_n", {"n": n})
