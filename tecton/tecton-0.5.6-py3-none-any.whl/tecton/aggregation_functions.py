from dataclasses import dataclass
from typing import Any
from typing import Dict


@dataclass
class AggregationFunction:
    name: str
    params: Dict[str, Any]


def last_distinct(n: int) -> AggregationFunction:
    return AggregationFunction("lastn", {"n": n})


# TODO(TEC-10550): we should rename the AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N to "lastn" and AGGREGATION_FUNCTION_LAST_DISTINCT_N to "last_distinct_n".
def last(n: int) -> AggregationFunction:
    return AggregationFunction("last_non_distinct_n", {"n": n})
