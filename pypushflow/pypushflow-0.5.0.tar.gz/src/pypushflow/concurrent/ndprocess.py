from . import process
from .non_daemonic import get_context


class NdProcessPool(process.ProcessPool):
    """Pool of non-daemonic processes (they can have sub-processes)."""

    def __init__(self, context: str = None, **kw) -> None:
        if context:
            context = get_context(context)
        super().__init__(context=context, **kw)
