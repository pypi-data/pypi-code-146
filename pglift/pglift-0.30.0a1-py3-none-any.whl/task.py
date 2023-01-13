import collections
import contextlib
import functools
import inspect
import logging
from typing import (
    Any,
    Callable,
    ClassVar,
    Deque,
    Dict,
    Generic,
    Iterator,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    cast,
)

import pydantic

from . import __name__ as pkgname
from . import exceptions
from ._compat import TypeAlias

A = TypeVar("A", bound=Callable[..., Any])
RA: TypeAlias = Callable[..., Any]

Call = Tuple["Task", Tuple[Any, ...], Dict[str, Any]]

logger = logging.getLogger(pkgname)


class Displayer(Protocol):
    def handle(self, msg: str) -> None:
        ...


class Task(Generic[A]):

    _calls: ClassVar[Optional[Deque[Call]]] = None
    displayer: ClassVar[Optional[Displayer]] = None

    def __init__(self, title: str, action: A) -> None:
        assert title, "expecting a non-empty title"
        self.title = title
        self.action = action
        self.signature = inspect.signature(action)
        self.revert_action: Optional[RA] = None
        functools.update_wrapper(self, action)

    def __repr__(self) -> str:
        return f"<Task '{self.action.__name__}' at 0x{id(self)}>"

    def _call(self, *args: Any, **kwargs: Any) -> Any:
        if self._calls is not None:
            self._calls.append((self, args, kwargs))
        b = self.signature.bind(*args, **kwargs)
        b.apply_defaults()
        self.display(self.title.format(**b.arguments))
        return self.action(*args, **kwargs)

    __call__ = cast(A, _call)

    def display(self, title: str) -> None:
        if self.displayer is not None:
            self.displayer.handle(title)

    def revert(self, title: Optional[str] = None) -> Callable[[RA], RA]:
        """Decorator to register a 'revert' callback function.

        The revert function must accept the same arguments than its respective
        action.
        """

        def decorator(revertfn: RA) -> RA:
            s = inspect.signature(revertfn)
            assert s.parameters == self.signature.parameters, (
                f"Parameters of function {self.action.__module__}.{self.action.__name__}({self.signature}) "
                f"differ from related revert function {revertfn.__module__}.{revertfn.__name__}({s})"
            )

            @functools.wraps(revertfn)
            def wrapper(*args: Any, _rolling_back: bool = False, **kwargs: Any) -> Any:
                b = s.bind(*args, **kwargs)
                b.apply_defaults()
                if _rolling_back:
                    logger.warning("reverting: %s", self.title.format(**b.arguments))
                if title is not None:
                    self.display(title.format(**b.arguments))
                return revertfn(*args, **kwargs)

            w = cast(RA, wrapper)
            self.revert_action = w
            return w

        return decorator


def task(title: str) -> Callable[[A], Task[A]]:
    def mktask(fn: A) -> Task[A]:
        return functools.wraps(fn)(Task(title, fn))

    return mktask


@contextlib.contextmanager
def displayer_installed(displayer: Optional[Displayer]) -> Iterator[None]:
    if displayer is None:
        yield
        return
    assert Task.displayer is None
    Task.displayer = displayer
    try:
        yield
    finally:
        Task.displayer = None


@contextlib.contextmanager
def transaction(revert_on_error: bool = True) -> Iterator[None]:
    """Context manager handling revert of run tasks, in case of failure."""
    if Task._calls is not None:
        raise RuntimeError("inconsistent task state")
    Task._calls = collections.deque()
    try:
        yield
    except BaseException as exc:
        # Only log internal errors, i.e. those not coming from user
        # cancellation or invalid input data.
        if isinstance(exc, KeyboardInterrupt):
            if Task._calls:
                logger.warning("%s interrupted", Task._calls[-1][0])
        elif not isinstance(exc, (pydantic.ValidationError, exceptions.Cancelled)):
            logger.warning(str(exc))
        assert Task._calls is not None
        while True:
            try:
                t, args, kwargs = Task._calls.pop()
            except IndexError:
                break
            if revert_on_error and t.revert_action:
                t.revert_action(*args, _rolling_back=True, **kwargs)
        raise exc
    finally:
        Task._calls = None
