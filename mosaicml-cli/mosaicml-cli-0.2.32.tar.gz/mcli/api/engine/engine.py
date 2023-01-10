""" GraphQL Query Engine """
from __future__ import annotations

import asyncio
import atexit
import json
import logging
import sys
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from http import HTTPStatus
from threading import Event
from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, Generator, List, Optional, Type, TypeVar, cast

import requests
from gql.client import Client, ReconnectingAsyncClientSession
from gql.transport import AsyncTransport
from gql.transport.exceptions import TransportQueryError
from gql.transport.websockets import WebsocketsTransport
from graphql import DocumentNode
from websockets.exceptions import WebSocketException

from mcli.api.exceptions import KubernetesException, MAPIException, MCLIConfigError, MultiMAPIException
from mcli.api.schema.generic_model import DeserializableModel
from mcli.config import MESSAGE

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
THREADPOOL_WORKERS = 10
THREADPOOL: Optional[ThreadPoolExecutor] = None


def _create_threadpool() -> ThreadPoolExecutor:
    """Create a global threadpool for requests
    """
    logger.debug("Creating default threadpool")
    global THREADPOOL
    THREADPOOL = ThreadPoolExecutor(max_workers=THREADPOOL_WORKERS, thread_name_prefix='mosaicml-api')
    return THREADPOOL


def start_background_loop(loop: asyncio.AbstractEventLoop, terminate: Event):
    asyncio.set_event_loop(loop)

    async def wait_for_terminate():
        while not terminate.is_set():
            await asyncio.sleep(0.1)

    loop.run_until_complete(wait_for_terminate())


T = TypeVar("T")  # pylint: disable=invalid-name


class MAPIConnection:
    """Connection to a user's MAPI instance

    Args:
        api_key: The user's API key. If not specified, the value of the $MOSAICML_API_KEY
            environment variable will be used. If that does not exist, the value in the
            user's config file will be used. If that does not exist, a MAPIException will
            be thrown.
        endpoint: The MAPI URL to hit for all requests. If not specified, the value of the
            $MOSAICML_API_ENDPOINT environment variable will be used. If that does not
            exist, the default setting will be used.
        pool: An optional threadpool to use for all connection requests. If not provided,
            a shared pool will be used for all requests.

    Raises:
        MAPIException: Raised if the user does not have an API key set
    """
    api_key: str
    endpoint: str

    def __init__(self,
                 api_key: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 pool: Optional[ThreadPoolExecutor] = None):
        self._load_from_environment(api_key, endpoint)
        self._pool = pool
        self._prev: Optional[MAPIConnection] = None

        # MAPI websocket client connections
        self.connected = False
        self._client: Optional[Client] = None
        self._session: Optional[ReconnectingAsyncClientSession] = None
        self._loop = asyncio.new_event_loop()
        self._terminate = Event()

    def _load_from_environment(self, api_key: Optional[str] = None, endpoint: Optional[str] = None) -> None:
        # pylint: disable-next=import-outside-toplevel
        from mcli import config
        conf = config.MCLIConfig.load_config(safe=True)
        if api_key is None:
            api_key = conf.api_key

        if not api_key:
            api_key = ''

        self.api_key = api_key

        if endpoint is None:
            endpoint = conf.endpoint
        self.endpoint = endpoint

    @staticmethod
    def _set_connection(connection: Optional[MAPIConnection]) -> None:
        """Set the current connection instance

        Args:
            connection: The desired connection instance
        """
        global _CONNECTION
        _CONNECTION = connection

    @property
    def pool(self) -> ThreadPoolExecutor:
        """The ThreadPoolExecutor that will contain all MAPI requests
        """
        if self._pool is None:
            self._pool = THREADPOOL or _create_threadpool()

        return self._pool

    def create_websocket_connection(self) -> Client:
        if self._client is None:
            # Start the event loop if it's not already running
            if not self._loop.is_running():
                logger.debug("Starting threaded asyncio event loop")
                self.pool.submit(start_background_loop, self._loop, self._terminate)

            # Create the graphql client
            logger.debug("Creating websocket client in threaded event loop")
            self._client = asyncio.run_coroutine_threadsafe(self._create_gql_client(), self._loop).result(timeout=10)
            logger.debug("Websocket client created")
            if (sys.version_info.major >= 3 and sys.version_info.minor >= 9) and hasattr(threading, '_register_atexit'):
                # This is only in python >= 3.9, but checking attribute to be extra safe
                # pylint: disable-next=protected-access,no-member
                threading._register_atexit(self.close)  # type: ignore
                logger.debug("Registered threading close")
            else:
                # In python < 3.9, this should work
                atexit.register(self.close)
                logger.debug("Registered exit close")

        self.connected = True
        return self._client

    @property
    def client(self) -> Client:
        return self.create_websocket_connection()

    async def _create_gql_client(self) -> Client:
        ws_endpoint = self.endpoint.replace("http://", "ws://").replace("https://", "wss://")
        headers = {'Authorization': self.api_key, 'Content-Type': 'application/json'}
        logger.debug(f"Connecting to websocket server at endpoint {ws_endpoint}")
        transport = WebsocketsTransport(url=ws_endpoint, init_payload=headers)
        return Client(transport=transport, fetch_schema_from_transport=False)

    def subscribe(
        self,
        query: DocumentNode,
        variables: Dict[str, Any],
        callback: Callable[[Dict[str, Any]], T],
    ) -> Generator[Future[T], None, None]:
        """Subscribe to the given query and return a generator of futures

        Args:
            query (DocumentNode): The GraphQL query document
            variables (Dict[str, Any]): A dictionary of variables to supply with the query

        Yields:
            Generator[Future[Dict[str, Any]], None, None]: A generator of futures for subscription results
        """

        if not self.connected:
            self._client = self.create_websocket_connection()

        gen = self._subscribe(query, variables)

        # get past session connect - if necessary
        asyncio.run_coroutine_threadsafe(gen.__anext__(), self._loop).result()

        try:
            while True:
                yield asyncio.run_coroutine_threadsafe(
                    # Handle errors before they are wrapped in a future so they can be
                    # properly set for the user
                    self._transform_subscription_result(gen.__anext__(), callback),
                    self._loop,
                )
        finally:
            gen.aclose()

    async def _subscribe(self, query: DocumentNode, variables: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """Async version of subscribe that actually does the calling

        If a session connecting to MAPI doesn't exist, one will be created
        """

        if not self._session:
            logger.debug("No websocket session found. Creating initial session")
            session = await self.client.connect_async(reconnecting=True)
            # reconnecting=True should be overloaded by library but isn't
            self._session = cast(ReconnectingAsyncClientSession, session)
            logger.debug("Created reconnecting websocket session")

        # Yield to let caller know session is connected.
        # Yielding an empty dict to preserve typing
        yield {}

        async for result in self._session.subscribe(query, variable_values=variables):
            yield result

    async def _transform_subscription_result(
        self,
        aw: Awaitable[Dict[str, Any]],
        callback: Callable[[Dict[str, Any]], T],
    ) -> T:
        """Awaits the awaitable argument and catches query errors so they can be
        passed as MAPIExceptions

        Args:
            aw (Awaitable[T]): Any awaitable

        Raises:
            MAPIException: Raised when a TransportQueryError is hit

        Returns:
            The awaited result
        """
        try:
            output = await aw
            return callback(output)
        except TransportQueryError as e:
            message = e.errors[0].get('message', str(e)) if e.errors else str(e)
            raise MAPIException(status=HTTPStatus.BAD_REQUEST, message=message) from e
        except WebSocketException as e:
            reason = getattr(e, 'reason', str(e))
            raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                message=f'Error connecting to MAPI service: {reason}') from e

    @staticmethod
    def get_current_connection() -> MAPIConnection:
        """Get the current connection instance
        """
        return _CONNECTION or _create_default_connection()

    @staticmethod
    def reset_connection() -> None:
        """Create a new connection instance
        """
        _create_default_connection()

    def close(self):
        """Close any existing connection to the MAPI service
        """
        if self._loop.is_running():
            if self._session:
                logger.debug("Disconnecting existing websocket session")
                asyncio.run_coroutine_threadsafe(self._session.stop_connecting_task(), self._loop).result()
                logger.debug("Websocket session disconnected")

            if self._client:
                logger.debug("Closing websocket transport")
                transport = cast(AsyncTransport, self._client.transport)
                asyncio.run_coroutine_threadsafe(transport.close(), self._loop).result()
                logger.debug("Websocket transport closed")

            logger.debug("Terminating event loop")
            self._terminate.set()

    def __enter__(self) -> MAPIConnection:
        self._prev = _CONNECTION
        self._set_connection(self)
        return self

    def __exit__(self, type_, value, traceback):
        self.close()
        self._set_connection(self._prev)

    def __del__(self):
        self.close()


_CONNECTION: Optional[MAPIConnection] = None


def _create_default_connection() -> MAPIConnection:
    """Creates the default MAPIConnection object
    """
    global _CONNECTION
    _CONNECTION = MAPIConnection()
    return _CONNECTION


ThreadedOutput = TypeVar('ThreadedOutput')


def run_in_threadpool(
    f: Callable[..., ThreadedOutput],
    *args: Any,
    connection: Optional[MAPIConnection] = None,
    **kwargs: Any,
) -> Future[ThreadedOutput]:
    """Run the provided function in the MAPI threadpool and return a Future

    Args:
        f: An arbitrary function
        *args, **kwargs: Arbitrary arguments with which to call ``f``
        connection: Optional :type MAPIConnection: whose threadpool will be used

    Returns:
        A Future for the return value of ``f``
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()
    return connection.pool.submit(f, *args, **kwargs)


def run_kube_in_threadpool(
    f: Callable[..., ThreadedOutput],
    *args: Any,
    connection: Optional[MAPIConnection] = None,
    **kwargs: Any,
) -> Future[ThreadedOutput]:
    """Wrap a function that calls Kubernetes and returns a :type DeserializableModel: in
    a Future

    Args:
        f: Function that calls Kubernetes
        *args, **kwargs: Arbitrary arguments with which to call ``f``
        connection: Optional :type MAPIConnection: whose threadpool will be used

    Returns:
        A Future for the return value of ``f``
    """
    return run_in_threadpool(KubernetesException.wrap(f), *args, connection=connection, **kwargs)


ModelT = TypeVar('ModelT', bound=DeserializableModel)


def run_plural_mapi_request(
    query: str,
    query_function: str,
    return_model_type: Optional[Type[ModelT]] = None,
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
) -> Future[List[ModelT]]:
    """Run a GraphQL query against MAPI and return a future for a list of items

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        return_model_type: The data type into which the response should be deserialized.
            Required if data is expected to be returned.
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.

    Raises:
        MAPIException: Raised if the request fails. See ``MAPIException`` for details on
        exception status codes
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_plural_mapi_request,
        api_key=connection.api_key,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=return_model_type,
    )
    future = cast('Future[List[ModelT]]', future)

    return future


def _threaded_plural_mapi_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
    model_type: Optional[Type[ModelT]],
) -> List[ModelT]:
    """Run a graphql request in a thread and return a list of items
    """
    if not api_key:
        raise MCLIConfigError(MESSAGE.API_KEY_MISSING)
    try:
        response = _run_graphql_request(api_key, endpoint, query, variables)
    except requests.exceptions.ConnectionError as e:
        mapi_error = MAPIException.from_requests_error(e)
        raise mapi_error from e

    return _deserialize_response(response, query_function, model_type)


def run_singular_mapi_request(
    query: str,
    query_function: str,
    return_model_type: Optional[Type[ModelT]] = None,
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
) -> Future[ModelT]:
    """Run a GraphQL query against MAPI and return a future for a singular item

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        return_model_type: The data type into which the response should be deserialized.
            Required if data is expected to be returned.
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.

    Raises:
        MAPIException: Raised if the request fails. See ``MAPIException`` for details on
        exception status codes
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_singular_mapi_request,
        api_key=connection.api_key,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=return_model_type,
    )
    future = cast('Future[ModelT]', future)

    return future


def _threaded_singular_mapi_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
    model_type: Optional[Type[ModelT]],
) -> ModelT:
    """Run a graphql request in a thread and return a single item

    Raises:
        MAPIException: Raised if no items were found
    """

    items = _threaded_plural_mapi_request(
        api_key=api_key,
        endpoint=endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=model_type,
    )
    if len(items) == 1:
        return items[0]
    else:
        raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message='Request returned no items, but expected 1')


def run_empty_mapi_request(
    query: str,
    query_function: str,
    variables: Optional[Dict[str, Any]] = None,
    connection: Optional[MAPIConnection] = None,
) -> Future[None]:
    """Run a GraphQL query against MAPI a future for the response

    If the result succeeds, ``future.result()`` will return ``None``, otherwise it will
    error with a ``MAPIException``.

    Args:
        query: Query to run
        query_function: GraphQL endpoint for the query (e.g. 'createRun')
        variables: Variables to be passed to the GraphQL endpoint. Defaults to None.
        connection: The MAPI connection that should be used. Defaults to the connection
            returned by `MAPIConnection.get_current_connection()`.

    Returns:
        A `concurrent.futures.Future` for the request. You can retrieve the data using
        `future.result()` with an optional `timeout` argument.
    """
    if not connection:
        connection = MAPIConnection.get_current_connection()

    future = connection.pool.submit(
        _threaded_empty_mapi_request,
        api_key=connection.api_key,
        endpoint=connection.endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
    )

    return future


def _threaded_empty_mapi_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]],
    query_function: str,
) -> None:
    """Run a graphql request in a thread and return None if the request succeeded
    """

    _ = _threaded_plural_mapi_request(
        api_key=api_key,
        endpoint=endpoint,
        query=query,
        variables=variables,
        query_function=query_function,
        model_type=None,
    )


def _run_graphql_request(
    api_key: str,
    endpoint: str,
    query: str,
    variables: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    if variables is None:
        variables = {}
    variables = {key.replace('$', ''): value for key, value in variables.items()}

    headers = {
        'Content-Type': 'application/json',
        'authorization': api_key,
    }
    payload = json.dumps({'query': query, 'variables': variables})

    # Don't want timeout since this will be run in a background thread
    # pylint: disable-next=missing-timeout
    response = requests.request(
        'POST',
        endpoint,
        headers=headers,
        data=payload,
    )
    try:
        return response.json()
    except requests.JSONDecodeError as e:
        mapi_error = MAPIException.from_requests_error(e)
        raise mapi_error from e


def _deserialize_response(
    response: Dict[str, Any],
    query_function: str,
    model_type: Optional[Type[ModelT]],
) -> List[ModelT]:
    """Given response, function, and model object, deserializes data

    raises
        MAPIException: Something on the MAPI side went wrong (400s) or the
            response didn't match the expected format (500)
        MultiMAPIException: Multiple errors encountered in graphql
    """

    # Check response for errors in the header (typically 401/403)
    error_to_raise = [MAPIException.from_mapi_error_response(e) for e in response.get('errors', [])]
    if error_to_raise:
        raise MultiMAPIException(error_to_raise)

    if model_type is None:
        return []

    try:
        data = response['data']
        query_response: List[Any] = data[query_function]
        return [model_type.from_mapi_response(i) for i in query_response]
    except (KeyError, TypeError) as e:
        raise MAPIException(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message='Internal Server Error: Malformed response data') from e
