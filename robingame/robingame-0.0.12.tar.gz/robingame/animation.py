import numpy
from typing import Callable


def ease(
    x: int,
    start: int | float,
    stop: int | float,
    num: int,
    function: Callable,
) -> float:
    """see https://easings.net/ for functions"""
    if x > num:
        raise ValueError(f"{x=} is greater than {num=}")
    distance = stop - start
    progress = x / num
    value = start + function(progress) * distance
    return value


def ease_in(x, start, stop, num, power=3) -> numpy.array:
    f = lambda x: x**power
    return ease(x=x, start=start, stop=stop, num=num, function=f)


def ease_out(x, start, stop, num, power=3) -> numpy.array:
    f = lambda x: 1 - (1 - x) ** power
    return ease(x=x, start=start, stop=stop, num=num, function=f)


def ease_in_out(x, start, stop, num, power=3) -> numpy.array:
    f = lambda x: 4 * x**power if x < 0.5 else 1 - (-2 * x + 2) ** power / 2
    return ease(x=x, start=start, stop=stop, num=num, function=f)


def damping_response(t, amp=0.5, damping=0.4, phase=0, freq=0.3):
    decay = damping * freq
    return amp * numpy.e ** (-decay * t) * numpy.cos(freq * t - phase)
