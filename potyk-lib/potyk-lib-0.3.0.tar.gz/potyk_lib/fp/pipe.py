__all__ = ['pipe', 'flow']


def pipe(*callables):
    """
    >>> sum_and_str = pipe(sum, str)
    >>> sum_and_str([1, 2])
    '3'
    """

    def _apply(val):
        for callable_ in callables:
            val = callable_(val)
        else:
            return val

    return _apply


flow = pipe
