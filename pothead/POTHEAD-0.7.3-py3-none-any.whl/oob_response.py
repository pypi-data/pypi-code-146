from collections import deque
from logging import getLogger
from os import environ, urandom
from threading import Lock, Thread, Timer
from time import monotonic, sleep
from typing import Any, Dict, Optional, Sequence, Tuple, Generic, TypeVar, Callable
from warnings import warn

from werkzeug.serving import make_server

from .wsgi_typing import (
    Environ,
    ExcInfo,
    ResponseStream,
    StartResponse,
    WsgiApplication,
)
from .util import ThreadsTracker

# Interval of how often to attempt cleanup of unclaimed jobs
CLEANUP_INTERVAL_SECONDS = float(environ.get("OOB_CLEANUP_INTERVAL_SECONDS", "5"))

# Maximum time a process is allowed to remain unclaimed before attempting to clean it up
ITEM_EXPIRY_SECONDS = float(environ.get("OOB_ITEM_EXPIRY_SECONDS", "20"))

LOGGER = getLogger("pothead.oob_response")


class Response:
    def __init__(self, headers, body, on_done):
        self.headers = headers
        self.body = body
        self.on_done = on_done

    def close(self):
        if self.on_done:
            self.body.close()
            self.on_done()
            self.on_done = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.close()


class KeyedTransfer:
    """Allows one thread to push a value, and get a (url-safe string) key back.
    At a later time, another thread can retrieve the value by the key.

    With regular intervals, unclaimed keys are purged. If the value has a method
    `close()`, it is called on purging."""

    def __init__(self, cleanup_interval_seconds: float, item_expiry_seconds: float):
        self._cleanup_interval_seconds = cleanup_interval_seconds
        self._item_expiry_seconds = item_expiry_seconds
        self._dict: Dict[str, Tuple[float, Any]] = dict()
        self._lock = Lock()
        self._shutdown = False

        self._cleanup()

    def push(self, value: Any):
        key = urandom(24).hex()
        now = monotonic()
        expires_at = now + self._item_expiry_seconds
        with self._lock:
            assert key not in self._dict
            self._dict[key] = (expires_at, value)

        return key

    def pop(self, key) -> Optional[Any]:
        with self._lock:
            return self._dict.pop(key, (None, None))[1]

    def close(self):
        self._shutdown = True
        with self._lock:
            for (expires_at, job) in self._dict.values():
                if hasattr(job, "close"):
                    job.close()
            self._dict.clear()

    def wait_for_clear(self):
        while True:
            with self._lock:
                if len(self._dict) == 0:
                    return
            sleep(self._cleanup_interval_seconds / 2)

    def _cleanup(self):
        if not self._shutdown:
            t = Timer(self._cleanup_interval_seconds, self._cleanup)
            t.daemon = True
            t.start()
        now = monotonic()
        with self._lock:
            new_dict = dict()
            for key, (expires_at, job) in self._dict.items():
                if expires_at > now:
                    new_dict[key] = (expires_at, job)
                elif hasattr(job, "close"):
                    job.close()
            self._dict = new_dict


class PeekableIterator(object):
    def __init__(self, inner):
        self._inner = iter(inner)
        self._cache = deque()

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._cache):
            return self._cache.popleft()
        else:
            return next(self._inner)

    def peek_next(self):
        if not len(self._cache):
            return self._cache.append(next(self._inner))
        return self._cache[0]

    def close(self):
        getattr(self._inner, "close", lambda: None)()


AtomicReferenceT = TypeVar("AtomicReferenceT")


class AtomicReference(Generic[AtomicReferenceT]):
    def __init__(self):
        self._lock = Lock()

    def is_set(self) -> bool:
        with self._lock:
            return hasattr(self, "data")

    def set(self, data: AtomicReferenceT) -> None:
        with self._lock:
            self.data = data

    def get(self) -> AtomicReferenceT:
        with self._lock:
            return self.data


class OutOfBandResponder:
    def __init__(
        self,
        wrapped_app: WsgiApplication,
        port=0,
        cleanup_interval_seconds: Optional[float] = None,
        item_expiry_seconds: Optional[float] = None,
    ):
        if cleanup_interval_seconds is None:
            cleanup_interval_seconds = CLEANUP_INTERVAL_SECONDS
        if item_expiry_seconds is None:
            item_expiry_seconds = ITEM_EXPIRY_SECONDS

        self._job_transfer = KeyedTransfer(
            cleanup_interval_seconds, item_expiry_seconds
        )
        self.wrapped_app = wrapped_app

        wsgi_app = self._content_response_wsgi
        self._server = make_server("0.0.0.0", port=port, app=wsgi_app, threaded=True)
        responder_service = Thread(target=self._server.serve_forever)
        responder_service.daemon = True
        responder_service.start()
        self._worker_tracker = ThreadsTracker()
        self._service_port = self._server.port

    def _content_response_wsgi(self, environ, start_response):
        with self._worker_tracker:
            path = environ["PATH_INFO"]
            if len(path) < 2 or path[0] != "/":
                start_response("404 Not Found", {})
                return []

            response_key = path[1:]
            response = self._job_transfer.pop(response_key)
            if response is None:
                start_response(
                    f"410 {response_key} is claimed, expired, or never registered", {}
                )
                return []

            with response:
                start_response(
                    "200 OK",
                    response.headers,
                )
                yield b""  # Flush response to client
                for chunk in response.body:
                    yield chunk

    def shutdown(self):
        LOGGER.info("Draining pending redirects")
        self._job_transfer.wait_for_clear()
        self._server.shutdown()
        LOGGER.info("Waiting for jobs to complete")
        self._worker_tracker.drain()
        LOGGER.info("Shutdown complete")

    def __call__(
        self,
        environ: Environ,
        start_response: StartResponse,
        assume_cleanup: Callable[[], Callable[[], None]],
    ) -> ResponseStream:
        start_response_called: AtomicReference[
            Tuple[str, Sequence[Tuple[str, str]], Optional[ExcInfo]]
        ] = AtomicReference()

        def my_start_response(
            status: str,
            headers: Sequence[Tuple[str, str]],
            exc_info: Optional[ExcInfo] = None,
        ):
            if start_response_called.is_set():
                warn("start_response called more than once")
            else:
                start_response_called.set((status, headers, exc_info))

        response = PeekableIterator(self.wrapped_app(environ, my_start_response))

        while not start_response_called.is_set():
            try:
                response.peek_next()
            except StopIteration:
                if start_response_called.is_set():
                    break
                else:
                    msg = "Application Terminated Without Response"
                    LOGGER.error(msg)
                    start_response("500 Internal Error", (), None)
                    return [msg.encode()]

        (status, headers, exc_info) = start_response_called.get()

        if not exc_info and status.startswith("200 "):
            on_done = assume_cleanup()
            key = self._job_transfer.push(Response(headers, response, on_done))
            start_response(
                "303 See Other",
                (
                    (
                        "Location",
                        f"http://{environ['SERVER_NAME']}:{self._service_port}/{key}",
                    ),
                ),
                None,
            )
            return []
        else:
            start_response(status, headers, exc_info)
            return response
