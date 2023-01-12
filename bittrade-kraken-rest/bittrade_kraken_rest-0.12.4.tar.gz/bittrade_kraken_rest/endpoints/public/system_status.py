from datetime import datetime
from typing import Literal

from pydantic.dataclasses import dataclass
from reactivex import Observable

from bittrade_kraken_rest.connection.observable import send_public
from bittrade_kraken_rest.connection.result import map_to_result

Status = Literal["online", "maintenance", "cancel_only", "post_only"]


@dataclass
class GetSystemStatusResult:
    status: Status
    timestamp: datetime


def get_system_status_response():
    return send_public(url="/0/public/SystemStatus")


def get_system_status() -> Observable[GetSystemStatusResult]:
    return get_system_status_response().pipe(map_to_result(GetSystemStatusResult))


__all__ = [
    "get_system_status",
    "GetSystemStatusResult",
]
