__all__ = ['dict_wo_none']


def dict_wo_none(dict_: dict):
    """
    >>> dict_wo_none({'a': None, 'b': 1})
    {'b': 1}
    """
    return {k: v for k, v in dict_.items() if v}
