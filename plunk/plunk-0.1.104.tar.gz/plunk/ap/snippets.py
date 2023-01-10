import timeit
from functools import partial
from collections import deque


def prefill_deque_with_value(value=None, maxlen: int = 10) -> deque:
    """Initialize deque prefilled with selected value

    >>> prefill_deque_with_value(-1, 10)
    deque([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], maxlen=10)

    :param value: Any value
    :param maxlen: Integer greater than zero
    :return:
    """

    d = deque((value,) * maxlen, maxlen=maxlen)
    return d


def _run_and_test_prefill_deque_with_value():
    print(f'{prefill_deque_with_value(0, 10)=}')
    t_prefill_deque_with_value = timeit.Timer(
        partial(prefill_deque_with_value, 0, int(1e6))
    )
    print(f'{t_prefill_deque_with_value.timeit(100)=}')


if __name__ == '__main__':
    _run_and_test_prefill_deque_with_value()
