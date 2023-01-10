"""Get a run's logs from the MosaicML Cloud"""
from __future__ import annotations

import base64
from concurrent.futures import Future
from typing import Any, Dict, Generator, Optional, Union, overload

import gql
from typing_extensions import Literal

from mcli.api.engine.engine import MAPIConnection
from mcli.api.model.run import Run

QUERY_FUNCTION = 'getRunLogs'
VARIABLE_DATA_NAME = 'getRunLogsInput'
QUERY = f"""
subscription Subscription(${VARIABLE_DATA_NAME}: GetRunLogsInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME})
}}"""


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[False] = False,
) -> Generator[str, None, None]:
    ...


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Generator[Future[str], None, None]:
    ...


def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: bool = False,
) -> Union[Generator[str, None, None], Generator[Future[str], None, None]]:
    """Get the current logs for an active or completed run

    Get the current logs for an active or completed run in the MosaicML Cloud.
    This returns the full logs as a ``str``, as they exist at the time the request is
    made. If you want to follow the logs for an active run line-by-line, use
    :func:`follow_run_logs`.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with :func:`~mcli.sdk.get_runs`.
        rank (``Optional[int]``): Node rank of a run to get logs for. Defaults to the lowest
            available rank. This will usually be rank 0 unless something has gone wrong.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`get_run_logs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the log text, use ``return_value.result()`` with an optional
            ``timeout`` argument.

    Returns:
        If future is False:
            The full log text for a run at the time of the request as a :obj:`str`
        Otherwise:
            A :class:`~concurrent.futures.Future` for the log text
    """
    # Convert to strings
    run_name = run.name if isinstance(run, Run) else run

    variables: Dict[str, Any] = {'name': run_name, 'follow': False}
    if rank is not None:
        variables['nodeRank'] = rank

    variables = {VARIABLE_DATA_NAME: variables}
    for message in _get_logs(QUERY, variables):
        if not future:
            try:
                yield message.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield message


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[False] = False,
) -> Generator[str, None, None]:
    ...


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Generator[Future[str], None, None]:
    ...


def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timeout: Optional[float] = None,
    future: bool = False,
) -> Union[Generator[str, None, None], Generator[Future[str], None, None]]:
    """Follow the logs for an active or completed run in the MosaicML Cloud

    This returns a :obj:`generator` of individual log lines, line-by-line, and will wait until
    new lines are produced if the run is still active.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with
            :func:`~mcli.sdk.get_runs`.
        rank (``Optional[int]``): Node rank of a run to get logs for. Defaults to the lowest
            available rank. This will usually be rank 0 unless something has gone wrong.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`follow_run_logs` will return immediately and the request will be
            processed in the background. The generator returned by the `~concurrent.futures.Future`
            will yield a `~concurrent.futures.Future` for each new log string returned from the cloud.
            This takes precedence over the ``timeout`` argument. To get the generator,
            use ``return_value.result()`` with an optional ``timeout`` argument and
            ``log_future.result()`` for each new log string.

    Returns:
        If future is False:
            A line-by-line :obj:`Generator` of the logs for a run
        Otherwise:
            A :class:`~concurrent.futures.Future` of a line-by-line generator of the logs for a run
    """
    # Convert to strings
    run_name = run.name if isinstance(run, Run) else run

    variables: Dict[str, Any] = {'name': run_name, 'follow': True}
    if rank is not None:
        variables['nodeRank'] = rank

    variables = {VARIABLE_DATA_NAME: variables}
    for message in _get_logs(QUERY, variables):
        if not future:
            try:
                yield message.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield message


def _get_logs(query: str, variables: Dict[str, Any]) -> Generator[Future[str], None, None]:

    gql_query = gql.gql(query)
    connection = MAPIConnection.get_current_connection()
    decoder = MessageDecoder()

    for message in connection.subscribe(gql_query, variables, decoder.parse_message):
        yield message


class MessageDecoder:
    """Decode messages from MAPI getRunLogs
    """

    def __init__(self):
        self.remaining = b''
        # prev can be used to maintain things that come after the final linebreak.
        # Leaving this off for now, but maybe we'd want it?
        self.prev = ''

    def parse_message(self, data: Dict[str, str]) -> str:
        """Get the next message from the GraphQL logging subscription
        """

        # Convert from base64 string to a bytestring
        b64_message = data['getRunLogs']
        b64_bytes = b64_message.encode('utf8')
        message_bytes = base64.b64decode(b64_bytes)

        # Add any previous hanging bytes
        byte_str: bytes = self.remaining + message_bytes
        try:
            decoded = byte_str.decode('utf8')
            self.remaining = b''
        except UnicodeDecodeError as e:
            self.remaining = byte_str[e.start:]
            decoded = byte_str[:e.start].decode('utf8')
        decoded, self.prev = self.prev + decoded, ''

        return decoded
