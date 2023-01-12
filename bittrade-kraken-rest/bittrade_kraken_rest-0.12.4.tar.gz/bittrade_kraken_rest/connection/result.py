from typing import TYPE_CHECKING, Any, Callable, Type, TypeVar

from reactivex import Observable, compose, operators
from requests.models import PreparedRequest, Response

from .observable import send

if TYPE_CHECKING:
    pass


_T = TypeVar("_T")
# _T = TypeVar("_T", bound="Dataclass")
# Need to look into this: All our @dataclass are not compatible with Dataclass


def map_to_result(
    result_class: Type[_T],
) -> Callable[[Observable[Response]], Observable[_T]]:
    def to_json(x: Response) -> dict[str, Any]:
        return x.json()

    return compose(
        operators.map(to_json),
        operators.map(lambda x: x["result"]),
        operators.map(lambda x: result_class(**x)),
    )


def send_and_map_to_result(
    result_class: Type[_T],
) -> Callable[[Observable[PreparedRequest]], Observable[_T]]:
    def log_me(x):
        print(x.json())

    return compose(
        operators.flat_map(send),
        operators.do_action(log_me),
        map_to_result(result_class),
    )


__all__ = [
    "map_to_result",
]
