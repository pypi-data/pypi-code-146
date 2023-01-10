import functools
import inspect
import logging
import os
import platform
import ssl
import sys
import urllib.parse
from typing import Any, Awaitable, Callable, Dict, NoReturn, Optional, Union

import httpx
from packaging.version import Version

from classiq.interface._version import VERSION as _VERSION
from classiq.interface.server import authentication

from classiq._internals import config
from classiq._internals.authentication import token_manager
from classiq._internals.host_checker import HostChecker
from classiq.exceptions import ClassiqAPIError, ClassiqExpiredTokenError

_FRONTEND_VARIANT: str = "classiq-sdk"
_INTERFACE_VARIANT: str = "classiq-interface-sdk"
_USERAGENT_SEPARATOR: str = " "

_logger = logging.getLogger(__name__)

_RETRY_COUNT = 2


@functools.lru_cache()
def _get_python_execution_environment() -> str:
    # Try spyder
    if any("SPYDER" in name for name in os.environ):
        return "Spyder"

    # try ipython and its variants
    try:
        shell = get_ipython().__class__.__name__  # type: ignore[name-defined]
        if shell == "ZMQInteractiveShell":
            return "Jupyter"  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return "IPython"  # Terminal running IPython
        else:
            return "IPython-other"  # Other type (?)
    except NameError:
        pass  # Probably standard Python interpreter

    # Try VSCode
    if "debugpy" in sys.modules:
        return "VSCode"

    # Try pycharm
    if "PYCHARM_HOSTED" in os.environ:
        return "PyCharm"

    return "Python"


@functools.lru_cache()
def _get_user_agent_header() -> Dict[str, str]:
    python_version = (
        f"python({_get_python_execution_environment()})/{platform.python_version()}"
    )
    os_platform = f"{os.name}/{platform.platform()}"
    frontend_version = f"{_FRONTEND_VARIANT}/{_VERSION}"
    interface_version = f"{_INTERFACE_VARIANT}/{_VERSION}"
    return {
        "User-Agent": _USERAGENT_SEPARATOR.join(
            (python_version, os_platform, frontend_version, interface_version)
        )
    }


def refresh_token_on_failure(func: Callable[..., Awaitable[Any]]):
    if not inspect.iscoroutinefunction(func):
        raise TypeError("Must decorate a coroutine function")

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        for i in range(_RETRY_COUNT):
            try:
                return await func(*args, **kwargs)
            except ClassiqExpiredTokenError:
                _logger.info(
                    "Token expired when trying to %s with args %s %s",
                    func,
                    args,
                    kwargs,
                    exc_info=True,
                )
                if i == _RETRY_COUNT - 1:
                    raise
                await client().update_expired_access_token()

    return wrapper


class Client:
    _UNKNOWN_VERSION = HostChecker._UNKNOWN_VERSION
    _LATEST_VERSION_API_PREFIX = "/api/v1"

    def __init__(self, conf: config.Configuration):
        self._config = conf
        self._token_manager = token_manager.TokenManager()
        self._ssl_context = ssl.create_default_context()
        self._HTTP_TIMEOUT_SECONDS = (
            3600  # Needs to be synced with load-balancer timeout
        )
        self._api_prefix = self._make_api_prefix()

    @classmethod
    def _make_api_prefix(cls) -> str:
        if _VERSION == cls._UNKNOWN_VERSION:
            return cls._LATEST_VERSION_API_PREFIX
        parsed_version = Version(_VERSION)
        return f"/api/v{parsed_version.major}-{parsed_version.minor}"

    def make_versioned_url(self, url_postfix: str) -> str:
        return self._api_prefix + url_postfix

    @classmethod
    def _handle_response(cls, response: httpx.Response) -> Union[Dict, str]:
        if response.is_error:
            cls.handle_error(response)
        return response.json()

    @staticmethod
    def handle_error(response: httpx.Response) -> NoReturn:
        expired = (
            response.status_code == httpx.codes.UNAUTHORIZED
            and response.json()["detail"] == authentication.EXPIRED_TOKEN_ERROR
        )

        if expired:
            raise ClassiqExpiredTokenError("Expired token.")

        message = f"Call to API failed with code {response.status_code}"
        try:
            detail = response.json()["detail"]
            message += f": {detail}"
        except Exception:  # nosec B110
            pass
        raise ClassiqAPIError(message)

    def _make_client_args(self) -> Dict[str, Any]:
        return {
            "base_url": self._config.host,
            "timeout": self._HTTP_TIMEOUT_SECONDS,
            "headers": {
                **self._get_authorization_header(),
                **_get_user_agent_header(),
            },
        }

    @refresh_token_on_failure
    async def call_api(
        self, http_method: str, url: str, body: Optional[Dict] = None
    ) -> Union[Dict, str]:
        async with self.async_client() as async_client:
            response = await async_client.request(
                method=http_method, url=self.make_versioned_url(url), json=body
            )
            return self._handle_response(response)

    def sync_call_api(
        self,
        http_method: str,
        url: str,
        body: Optional[Dict] = None,
        use_versioned_url: bool = True,
    ) -> Union[Dict, str]:
        if use_versioned_url:
            url = self.make_versioned_url(url)
        with httpx.Client(**self._make_client_args()) as sync_client:
            response = sync_client.request(method=http_method, url=url, json=body)
            return self._handle_response(response)

    def async_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(**self._make_client_args())

    def _get_authorization_header(self) -> Dict[str, str]:
        access_token = self._token_manager.get_access_token()
        if access_token is None:
            return dict()
        return {"Authorization": f"Bearer {access_token}"}

    def _get_authorization_query_string(self) -> str:
        access_token = self._token_manager.get_access_token()
        if access_token is None:
            return ""
        return urllib.parse.urlencode({"token": access_token})

    async def update_expired_access_token(self) -> None:
        await self._token_manager.update_expired_access_token()

    def get_backend_uri(self) -> str:
        return self._config.host

    def check_host(self) -> None:
        # This function is NOT async (despite the fact that it can be) because it's called from a non-async context.
        # If this happens when we already run in an event loop (e.g. inside a call to asyncio.run), we can't go in to
        # an async context again.
        # Since this function should be called ONCE in each session, we can handle the "cost" of blocking the
        # event loop.

        # Currently, there is a circular (interface) dependency between the Client and the HostChecker.
        # Since this happened once, we'll leave it for now. If it happens again, we should split the Client
        # into a low level client for accessing the server and a high level client.
        checker = HostChecker(self, client_version=_VERSION)
        checker.check_host_version()
        checker.check_deprecated_version()

    async def authenticate(self, overwrite: bool) -> None:
        await self._token_manager.manual_authentication(overwrite=overwrite)

    @property
    def config(self) -> config.Configuration:
        return self._config


DEFAULT_CLIENT: Optional[Client] = None


def client() -> Client:
    global DEFAULT_CLIENT
    if DEFAULT_CLIENT is None:
        # This call initializes DEFAULT_CLIENT
        configure(config.init())
    assert DEFAULT_CLIENT is not None
    return DEFAULT_CLIENT


def configure(conf: config.Configuration) -> None:
    global DEFAULT_CLIENT
    assert DEFAULT_CLIENT is None, "Can not configure client after first usage."

    DEFAULT_CLIENT = Client(conf=conf)
    if conf.should_check_host:
        DEFAULT_CLIENT.check_host()
