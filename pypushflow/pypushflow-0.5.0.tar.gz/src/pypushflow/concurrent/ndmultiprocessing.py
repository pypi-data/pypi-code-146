from . import multiprocessing
from .non_daemonic import get_context


class NProcessPool(multiprocessing.MProcessPool):
    """Pool of non-daemonic processes (they can have sub-processes)."""

    def __init__(self, context: str = None, **kw) -> None:
        context = get_context(context)
        super().__init__(context=context, **kw)
