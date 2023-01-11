# util_context_managers.py
# -*- coding: utf-8 -*-

"""
Context managers which serve for general purposes
"""

from time import perf_counter


# ______________________________________________________________________________________________________________________


class Timer:
    """
    A context manager to measure start, end and elapsed time of a code block.
    Useage:

    >>> with Timer() as time_stats:
    >>>     '...write code here..'
    >>> print(time_stats.elapsed)
    """

    def __init__(self):
        self.elapsed = 0

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = perf_counter()
        self.elapsed = self.stop - self.start
        return False


# ______________________________________________________________________________________________________________________
