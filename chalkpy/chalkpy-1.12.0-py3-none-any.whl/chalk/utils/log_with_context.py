"""
Adds thread-local context to a Python logger. Taken from neocrym/log-with-context
"""
import collections.abc
import contextlib
import contextvars
import logging
from typing import Any, List, Mapping, Optional

_LOGGING_CONTEXT_STACK: contextvars.ContextVar[List[Mapping[str, Any]]] = contextvars.ContextVar(
    "_LOGGING_CONTEXT_STACK"
)


def _recursive_merge(a: Mapping[str, Any], b: Mapping[str, Any]):
    ans: Mapping[str, Any] = {**a}
    for k, v in b.items():
        if k not in ans or not (isinstance(ans[k], collections.abc.Mapping) and isinstance(v, collections.abc.Mapping)):
            ans[k] = v
            continue
        ans[k] = _recursive_merge(ans[k], v)
    return ans


def get_logging_context() -> Mapping[str, Any]:
    """
    Retrieve the log context for the current python context.
    This initializes the thread-local variable if necessary.
    """
    return _LOGGING_CONTEXT_STACK.get([{}])[-1]


def set_logging_context(_merge: bool = True, **extra: Any):
    """
    Sets the context-local log context to a new value.

    Args:
        merge: If true, the new context will be merged with the current context. Otherwise, the new context will overwrite the existing context.
    """
    log_context_stack = _LOGGING_CONTEXT_STACK.get([{}])
    if _merge:
        extra = _recursive_merge(
            log_context_stack[-1],
            extra,
        )
    log_context_stack.append(extra)
    _LOGGING_CONTEXT_STACK.set(log_context_stack)


def pop_logging_context():
    """Pop the latest log context off of the log context stack, and reset it to its previous value.

    Raises:
        RuntimeError, if there is no current context from set_logging_context()
    """
    stack = _LOGGING_CONTEXT_STACK.get([])
    if len(stack) == 0:
        raise RuntimeError("Log context stack is empty")
    stack.pop()
    _LOGGING_CONTEXT_STACK.set(stack)


class LogWithContextFilter(logging.Filter):
    """Filter to append the ``extras`` onto the LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        for k, v in get_logging_context().items():
            if not hasattr(record, k):
                setattr(record, k, v)
        return True


def get_logger(name: Optional[str]):
    logger = logging.getLogger(name)
    logger.addFilter(LogWithContextFilter())
    return logger


# Backwards compatibility
Logger = get_logger


@contextlib.contextmanager
def add_logging_context(_merge: bool = True, **extra: Any):
    """
    A context manager to push and pop "extra" dictionary keys.

    Args:
        _merge: Whether to merge the new context with the existing log context.
        kwargs: Contextual information to add to the log record
    """
    set_logging_context(_merge, **extra)
    try:
        yield
    finally:
        pop_logging_context()
