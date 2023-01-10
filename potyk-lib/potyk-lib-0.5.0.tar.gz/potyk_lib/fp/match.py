# coding=utf-8
from operator import itemgetter

from typing import TypeVar, Tuple, Any

__all__ = ['match', 'match_str']

MatchT = TypeVar('MatchT')


def match(
    obj_to_match,  # type: MatchT
    *matchers  # type: Tuple[MatchT, Any]
):
    """
    >>> match('ass',('ass', 'tities'), ('beer', 'bitches'),)
    'tities'
    """
    for matcher, on_match in matchers:
        if matcher == obj_to_match:
            return on_match
    else:
        raise LookupError(
            u'Не нашлось совпадения: obj_to_match = {}, matchers = {}',
            obj_to_match,
            list(map(itemgetter(0), matchers)),
        )


def match_str(str_to_match, **matchers):
    """
    >>> match_str('ass',ass='tities', beer='bitches')
    'tities'
    """
    return match(str_to_match, *matchers.items())
