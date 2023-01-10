from __future__ import annotations

from typing import Any, Dict, Optional

import pydantic

from classiq.interface.generator.arith.fix_point_number import FixPointNumber
from classiq.interface.helpers.custom_pydantic_types import PydanticFloatTuple


class RegisterUserInput(pydantic.BaseModel):
    size: pydantic.PositiveInt
    name: str = pydantic.Field(default="")
    is_signed: bool = pydantic.Field(default=False)
    fraction_places: pydantic.NonNegativeInt = pydantic.Field(default=0)
    bounds: PydanticFloatTuple = pydantic.Field(default=None)

    def is_boolean_register(self) -> bool:
        return (not self.is_signed) and (self.size == 1) and (self.fraction_places == 0)

    @property
    def is_frac(self) -> bool:
        return self.fraction_places > 0

    @pydantic.validator("bounds", always=True)
    def _validate_bounds(
        cls, bounds: Optional[PydanticFloatTuple], values: Dict[str, Any]
    ) -> PydanticFloatTuple:
        if bounds is not None:
            if min(bounds) < 0:
                assert values.get("is_signed")
            return tuple(bounds)  # type: ignore[return-value]
        size = values.get("size")
        if not isinstance(size, int):
            raise ValueError("RegisterUserInput must have an integer size")
        is_signed: bool = values.get("is_signed", False)
        lb = 0 if not is_signed else -(2 ** (size - 1))
        ub = 2**size - 1 if not is_signed else 2 ** (size - 1) - 1
        fraction_factor = float(2 ** -values.get("fraction_places", 0))
        return (lb * fraction_factor, ub * fraction_factor)

    @property
    def integer_part_size(self) -> pydantic.NonNegativeInt:
        return self.size - self.fraction_places

    def revalued(self, **kwargs) -> RegisterUserInput:
        kwargs_dict = self.dict()
        kwargs_dict.update({**kwargs})
        return RegisterUserInput(**kwargs_dict)

    @staticmethod
    def bounds_to_integer_part_size(lb: float, ub: float) -> int:
        lb, ub = min(lb, ub), max(lb, ub)
        ub_integer_part_size = FixPointNumber(float_value=ub).integer_part_size
        lb_integer_part_size = FixPointNumber(float_value=lb).integer_part_size
        if lb == 0:
            return ub_integer_part_size
        if ub == 0:
            return lb_integer_part_size
        is_extra_bit_needed = (
            lb < 0 < ub and ub_integer_part_size >= lb_integer_part_size
        )
        return max(ub_integer_part_size + 1 * is_extra_bit_needed, lb_integer_part_size)

    class Config:
        frozen = True
