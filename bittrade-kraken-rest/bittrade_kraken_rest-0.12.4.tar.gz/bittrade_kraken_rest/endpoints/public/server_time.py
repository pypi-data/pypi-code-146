import requests
from pydantic.dataclasses import dataclass
from reactivex import Observable

from bittrade_kraken_rest.connection.observable import send_public
from bittrade_kraken_rest.connection.result import map_to_result


@dataclass
class GetServerTimeResult:
    unixtime: int
    rfc1123: str


def get_server_time_response() -> Observable[requests.Response]:
    return send_public(url="/0/public/Time")


def get_server_time() -> Observable[GetServerTimeResult]:
    return get_server_time_response().pipe(map_to_result(GetServerTimeResult))


__all__ = [
    "GetServerTimeResult",
    "get_server_time",
]
