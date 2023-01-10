from decimal import Decimal, ROUND_HALF_UP
from typing import Union

__all__ = ['decimal_round']


def decimal_round(decimal_: Union[Decimal, float]) -> Decimal:
    """
    >>> decimal_round(Decimal("14.4045"))
    Decimal('14.40')
    >>> decimal_round(14.4045)
    Decimal('14.4')
    """
    if isinstance(decimal_, float):
        return Decimal(str(round(decimal_, 2)))

    return Decimal(decimal_.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
