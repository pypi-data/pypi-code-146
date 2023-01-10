import math
from typing import Any, Dict, Generic, Optional, TypeVar

import pydantic
from pydantic.generics import GenericModel

RangeType = TypeVar("RangeType", int, float)

# math.isclose is symmetric and well equipped to avoid unwanted scenarios while numpy's isn't
# see https://github.com/numpy/numpy/issues/10161
# however math's default values are not good for comparing against zeros
DEF_ATOL: float = 1e-08
DEF_RTOL: float = 1e-05


class Range(GenericModel, Generic[RangeType]):
    lower_bound: Optional[RangeType] = None
    upper_bound: Optional[RangeType] = None

    class Config:
        frozen = True

    @pydantic.root_validator()
    def _validate_bounds_order(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        lower_bound = values.get("lower_bound")
        upper_bound = values.get("upper_bound")

        if (
            lower_bound is not None
            and upper_bound is not None
            and lower_bound > upper_bound
        ):
            raise ValueError("lower bound must not be greater than upper bound")

        return values

    def is_lower_bound_sat_by(
        self, value: float, atol: float = DEF_ATOL, rtol: float = DEF_RTOL
    ) -> bool:
        return (
            value >= self.lower_bound
            or math.isclose(value, self.lower_bound, abs_tol=atol, rel_tol=rtol)
            if self.lower_bound is not None
            else True
        )

    def is_upper_bound_sat_by(
        self, value: float, atol: float = DEF_ATOL, rtol: float = DEF_RTOL
    ) -> bool:
        return (
            value <= self.upper_bound
            or math.isclose(value, self.upper_bound, abs_tol=atol, rel_tol=rtol)
            if self.upper_bound is not None
            else True
        )

    def is_range_sat_by(self, value: float) -> bool:
        return self.is_upper_bound_sat_by(value) and self.is_lower_bound_sat_by(value)


NonNegativeIntRange = Range[pydantic.NonNegativeInt]
NonNegativeFloatRange = Range[pydantic.NonNegativeFloat]
