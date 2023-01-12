from typing import Any, Optional

import requests
from reactivex import Observable, just
from reactivex.abc import ObserverBase, SchedulerBase
from reactivex.scheduler import CurrentThreadScheduler

from bittrade_kraken_rest.connection.nonce import get_nonce

API_URL = "https://api.kraken.com"

_session = requests.Session()


def send_public(
    url: str,
    *,
    session: Optional[requests.Session] = None,
    params: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, Any]] = None,
) -> Observable[requests.Response]:
    """Send request to Kraken public REST API.

    All public endpoints use GET

      Args:
          url (str): should start with a "/" or include the full kraken api domain
          (so you may use beta apis)
          params (dict): Query params
          headers:

      Returns:
          requests.Response:
    """
    request = requests.Request(
        "GET", f"{API_URL}{url}", params=params or {}, headers=headers or {}
    )
    return send(request.prepare(), session_=session)


def prepare_private(
    url: str,
    *,
    data: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, Any]] = None,
) -> Observable[tuple[requests.PreparedRequest, str, dict[str, Any]]]:
    """Prepares a request to be sent to private API.
    Needs to be signed by user's own code

    Returns:
        requests.PreparedRequest:
    """
    data = data or {}
    if "nonce" not in data:
        data = dict(
            nonce=get_nonce(), **{k: v for k, v in data.items() if v is not None}
        )
    headers = headers or {}
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=utf-8"
    request = requests.Request("POST", f"{API_URL}{url}", data=data, headers=headers)
    return just((request.prepare(), url, data))


def send(
    request: requests.PreparedRequest, *, session_: Optional[requests.Session] = None
) -> Observable[requests.Response]:
    session = session_ or _session

    def subscribe(observer: ObserverBase, scheduler: Optional[SchedulerBase] = None):
        scheduler_ = scheduler or CurrentThreadScheduler()

        def action(*_):
            response = session.send(request)
            if response.ok:
                as_json = response.json()
                if not as_json["error"]:
                    observer.on_next(response)
                    observer.on_completed()
                else:
                    observer.on_error(Exception(as_json["error"][0]))
            else:
                try:
                    response.raise_for_status()
                except Exception as exc:
                    observer.on_error(exc)

        return scheduler_.schedule(action)

    return Observable(subscribe)
