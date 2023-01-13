from typing import Awaitable, Callable, Optional


__all__ = ("_global_handler",)


_global_handler: Optional[Callable[[str], Awaitable[None]]] = None
