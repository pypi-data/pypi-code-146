""" Type Helper Objects """
from typing import Any, Generic, TypeVar

# pylint: disable-next=invalid-name
T = TypeVar('T')


class FutureType(Generic[T]):
    """Typing for a `concurrent.futures.Future` response wrapper
    """

    def result(self, timeout: float) -> T:  # pylint: disable=unused-argument
        ...

    def set_exception(self, exc_info: BaseException):  # pylint: disable=unused-argument
        ...

    def set_result(self, result: Any):  # pylint: disable=unused-argument
        ...
