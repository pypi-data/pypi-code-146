from abc import abstractmethod
from typing import Protocol, TypeVar, Iterable


def proper_values(values: Iterable) -> list:
    """
    Tranfrosm given values to proper ones for SQL query.

    :param values: Iterable of Python values.
    :return: list of values configured for SQL query.
    """
    proper_values = []
    for v in values:
        if isinstance(v, str):
            proper_values.append(f'"{v}"')
        elif isinstance(v, list) or isinstance(v, tuple):
            proper_values.append(v)
        elif v is None:
            proper_values.append('NULL')
        else:
            proper_values.append(f'{v}')
    return proper_values