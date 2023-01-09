from decimal import Decimal, InvalidOperation
from typing import Optional

__all__ = ['try_int', 'try_float', 'try_decimal']

NotSet = object()


def try_int(param, else_=NotSet):
    """
    >>> try_int('0')
    0
    >>> try_int('a')
    'a'
    >>> try_int('a', else_=None) is None
    True
    >>> try_int('a', else_=0)
    0
    >>> try_int(None) is None
    True
    """
    try:
        return int(param)
    except (ValueError, TypeError):
        return else_ if else_ != NotSet else param


def try_float(raw):
    try:
        return float(raw)
    except ValueError:
        return raw


def try_decimal(decimal_str: str) -> Optional[Decimal]:
    try:
        return Decimal(decimal_str)
    except InvalidOperation:
        return None
