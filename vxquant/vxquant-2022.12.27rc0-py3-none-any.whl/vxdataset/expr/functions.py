import polars as pl
import numpy as np
from collections import deque
from typing import Callable


class ColsRolling:
    def __init__(self, func: Callable, windows: int):
        self._func = func
        self._windows = windows
        self._args = None

    def __call__(self, s: pl.Series):
        if self._args is None:
            cnt = len(s)
            self._args = (
                deque([np.nan for _ in range(self._windows)], maxlen=cnt)
                for _ in range(len(s))
            )

        new_args = []
        for new_arg, args_queue in zip(s, self._args):
            args_queue.append(new_arg)
            new_args.append(np.array(args_queue))

        return self._func(*new_args)


def rolling_apply_cols(exprs, func, windows):
    return pl.concat_list(exprs).apply(ColsRolling(func, windows))
