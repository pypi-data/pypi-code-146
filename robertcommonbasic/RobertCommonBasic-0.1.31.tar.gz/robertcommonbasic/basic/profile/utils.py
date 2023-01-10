from cProfile import Profile
from datetime import datetime
from io import StringIO
from pstats import Stats
from typing import Callable, TypeVar, NamedTuple

T = TypeVar('T')


class ProfilingConfig(NamedTuple):
    sort_by: str = 'cumtime'
    amount: int = 20
    printer: Callable = None


def profile_func(func: Callable[[], T], cfg: ProfilingConfig) -> T:
    if cfg.printer is None:
        printer = print
    else:
        printer = cfg.printer
    pr = Profile()
    pr.enable()
    try:
        return func()
    finally:
        pr.disable()
        s = StringIO()
        try:
            Stats(pr, stream=s).sort_stats(cfg.sort_by).print_stats(cfg.amount)
            printer(s.getvalue())
        finally:
            s.close()


class Stopwatch:
    def __init__(self, name: str = ""):
        self._name = name
        self._laps = []
        self._t_init = datetime.now()

    def lap(self, name):
        t = datetime.now()
        last_t = self._laps[-1][1] if self._laps else self._t_init
        self._laps.append((name, t, t - last_t))

    def dump(self):
        laps_text = ", ".join([f"{lap[0]}={lap[2].total_seconds()}" for lap in self._laps])
        return f"[{self._name}] {laps_text}"
