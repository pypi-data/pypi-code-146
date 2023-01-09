"""Decorator versions of functions in monitor.py."""
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from bitfount.federated.monitoring.monitor import task_status_update
from bitfount.federated.monitoring.types import MonitorRecordPrivacy

_F = TypeVar("_F", bound=Callable[..., Any])


def task_status(
    message: str, privacy: MonitorRecordPrivacy = MonitorRecordPrivacy.ALL_PARTICIPANTS
) -> Callable[[_F], _F]:
    """A decorator that will send a TASK_STATUS_UPDATE message at function start."""

    def _wrapper(func: _F) -> _F:
        @wraps(func)
        def _wrapped(*args: Any, **kwargs: Any) -> Any:
            task_status_update(message=message, privacy=privacy)
            return func(*args, **kwargs)

        return cast(_F, _wrapped)

    return _wrapper
