"""Implements the API get_run_logs for Kubernetes"""
from __future__ import annotations

import re
from concurrent.futures import Future
from datetime import datetime
from http import HTTPStatus
from typing import Generator, List, NamedTuple, Optional, Union, cast, overload

import arrow
from rich.style import Style
from typing_extensions import Literal

from mcli.api.engine.engine import run_in_threadpool
from mcli.api.exceptions import KubernetesException
from mcli.api.model import Run
from mcli.models.mcli_cluster import Cluster
from mcli.utils.utils_kube import get_pod_rank, list_run_pods, read_pod_logs, stream_pod_logs
from mcli.utils.utils_run_status import RunStatus

# Sometimes Kubernetes garbage collects the logs and you see this line instead
ERROR_LINE = r'unable to retrieve container logs for (containerd|docker).*'
FAILED_WATCH_LINE = r'failed to watch file "/var/lib/docker/containers/.*'

# Ansi-coded bold red warning message
CORRUPTED_WARNING = Style(color='red', bold=True).render('Logs seem to have been corrupted on the server. '
                                                         'Some lines may be missing')


class LogLine(NamedTuple):
    """A single line of a run's logs

    To print a record, use:
    ```python
    # Print the line with timestamp
    print(str(record))

    # Print the line without timestamp
    print(record.text)
    ```

    Attributes:
        text: The text of the line
        timestamp: The timestamp at which the line was written
    """
    text: str
    timestamp: datetime

    def __str__(self) -> str:
        return f'{self.timestamp.isoformat()} {self.text}'

    def __repr__(self) -> str:
        return f'LogRecord({repr(self.text)}, {repr(self.timestamp)})'

    @classmethod
    def splitlines(cls, text: str) -> Generator[LogLine, None, None]:
        """Split logs on lines that start with a timestamp

        Args:
            text: Full Kubernetes log

        Yields:
            LogRecord: A parsed record for each log line
        """
        prev_line: str = ''
        for line in text.splitlines(keepends=True):
            # Check if line startswith a timestamp
            try:
                _ = arrow.get(line.split(' ', 1)[0])
            except arrow.parser.ParserError:
                # No timestamp
                prev_line += line
            else:
                # Line starts with a timestamp, so yield prev_line
                if prev_line:
                    yield LogLine.from_line(prev_line.rstrip('\n'))
                prev_line = line
        if prev_line:
            yield LogLine.from_line(prev_line.rstrip('\n'))

    @classmethod
    def validate_line(cls, text: str) -> Literal[True]:
        """Validate that log text is not corrupted

        Args:
            text: A run's log text

        Raises:
            KubernetesException (HTTPStatus.INTERNAL_SERVER_ERROR): Raised if the log
                text is corrupted

        Returns:
            True if an exception was not raised
        """
        if re.match(ERROR_LINE, text) or re.match(FAILED_WATCH_LINE, text):
            raise KubernetesException(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message='Logs seem to have been corrupted. Unable to retrieve logs for this run',
            )
        return True

    @classmethod
    def from_line(cls, line: str) -> LogLine:
        """Parse a line of logs to extract the timestamp and remaining text

        Args:
            line (str): A line of logs

        Raises:
            KubernetesException (HTTPStatus.INTERNAL_SERVER_ERROR): Raised if the log line
                could not be parsed

        Returns:
            LogRecord: the parsed record for the log line
        """
        cls.validate_line(line)
        ts, text = line.split(' ', 1)
        try:
            timestamp = arrow.get(ts).datetime
        except arrow.parser.ParserError as e:
            raise KubernetesException(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=f'Unable to parse log line because there was no timestamp:\n\n{line}') from e
        return LogLine(text, timestamp)


def _threaded_get_run_logs(run: Union[str, Run], rank: Optional[int] = None, timestamps: bool = False) -> str:
    """Threaded function to provide a the current logs for the given run
    """
    # Refresh run info
    if isinstance(run, str) or run.status.before(RunStatus.RUNNING):
        run = _get_run(run)

    with Cluster.use(run.config.cluster) as cluster:
        pod_name = _get_run_pod_name(run, namespace=cluster.namespace, rank=rank)
        logs = read_pod_logs(pod_name, cluster.namespace, timestamps=timestamps)

        # Validate that the logs weren't corrupted or lost
        try:
            LogLine.validate_line(logs)
        except KubernetesException:
            # Just append so we don't lose many lines if error message occurs at the end
            logs = '\n'.join([logs, CORRUPTED_WARNING])

        return logs


def _threaded_follow_run_logs(run: Union[str, Run],
                              rank: Optional[int] = None,
                              timestamps: bool = False) -> Generator[str, None, None]:
    """Threaded function to provide a generator of lines for the given run
    """
    # Refresh run info
    if isinstance(run, str) or run.status.before(RunStatus.RUNNING):
        run = _get_run(run)

    def _wrapped_log_generator(name: str, cluster: Cluster, timestamps: bool) -> Generator[str, None, None]:
        """Wrap the log line generator. This lets the rest of _threaded_follow_run_logs
        execute when called, otherwise _get_run call would also wait until the first line
        was requested
        """
        with Cluster.use(cluster):
            for line in stream_pod_logs(name, cluster.namespace, timestamps=timestamps):
                # Validate that the line wasn't corrupted or lost
                try:
                    LogLine.validate_line(line)
                except KubernetesException:
                    line = CORRUPTED_WARNING
                yield line

    with Cluster.use(run.config.cluster) as cluster:
        pod_name = _get_run_pod_name(run, namespace=cluster.namespace, rank=rank)
    return _wrapped_log_generator(pod_name, cluster, timestamps)


def _get_run(run: Union[str, Run]) -> Run:
    """Get a run from a run name
    """
    # pylint: disable-next=import-outside-toplevel
    from mcli.api.kube.runs import get_runs

    # Cast to fix typing of List[Union[str, Run]]
    iruns = cast(Union[List[str], List[Run]], [run])

    runs = get_runs(iruns)
    if not runs:
        # Run doesn't exist -> Raise 404
        run_name = run.name if isinstance(run, Run) else run
        raise KubernetesException(status=HTTPStatus.NOT_FOUND, message=f'Could not find run: {run_name}')
    return runs[0]


def _get_run_pod_name(run: Run, namespace: str, rank: Optional[int] = None) -> str:
    """Get the appropriate pod from a run
    """
    if run.status.before(RunStatus.RUNNING):
        # Run hasn't started yet, so error
        raise KubernetesException(status=HTTPStatus.BAD_REQUEST,
                                  message=f'Run {run.name} hasn\'t started running yet. '
                                  f'It currently has a status of: {str(run.status.value).lower()}. '
                                  'Please wait and try again. '
                                  'You can wait using:\n\n'
                                  f'wait_for_run_status("{run.name}", status=RunStatus.RUNNING)')

    # Get all possible pods
    pods = list_run_pods(run.name, namespace)

    # Get the requested rank or error
    rank_dict = {get_pod_rank(pod): pod for pod in pods}
    if rank is None:
        rank = sorted(list(rank_dict))[0]
        pod = rank_dict[rank]
    elif rank in rank_dict:
        pod = rank_dict[rank]
    else:
        raise KubernetesException(status=HTTPStatus.BAD_REQUEST,
                                  message=f'Could not find a node with rank {rank} for run {run.name}. '
                                  f'Valid ranks are: {", ".join(str(i) for i in sorted(list(rank_dict)))}')

    return pod.metadata.name


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timestamps: bool = False,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> str:
    ...


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timestamps: bool = False,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[str]:
    ...


def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timestamps: bool = False,
    timeout: Optional[float] = 10,
    future: bool = False,
) -> Union[str, Future[str]]:
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
        timestamps (``bool``): If ``True``, each log line will also contain the timestamp at
            which it was emitted. If you wish to parse out a line's timestamp and text,
            you can use :meth:`LogLine.from_line`.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`get_run_logs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the log text, use ``return_value.result()`` with an optional
            ``timeout`` argument.

    Raises:
        KubernetesException (HTTPStatus.NOT_FOUND): Raised if the requested run does not exist
        KubernetesException (HTTPStatus.BAD_REQUEST): Raised if the run is not yet running,
            or if the run does not have a node of the requested rank.

    Returns:
        If future is False:
            The full log text for a run at the time of the request as a :obj:`str`
        Otherwise:
            A :class:`~concurrent.futures.Future` for the log text
    """

    future_logs = run_in_threadpool(KubernetesException.wrap(_threaded_get_run_logs),
                                    run,
                                    rank=rank,
                                    timestamps=timestamps)

    if not future:
        return future_logs.result(timeout=timeout)
    else:
        return future_logs


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timestamps: bool = False,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> Generator[str, None, None]:
    ...


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timestamps: bool = False,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[Generator[str, None, None]]:
    ...


def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    timestamps: bool = False,
    timeout: Optional[float] = 10,
    future: bool = False,
) -> Union[Generator[str, None, None], Future[Generator[str, None, None]]]:
    """Follow the logs for an active or completed run in the MosaicML Cloud

    This returns a :obj:`generator` of individual log lines, line-by-line, and will wait until
    new lines are produced if the run is still active. If you are only looking for the
    logs up until the time of the request, consider using :func:`get_run_logs` instead.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with
            :func:`~mcli.sdk.get_runs`.
        rank (``Optional[int]``): Node rank of a run to get logs for. Defaults to the lowest
            available rank. This will usually be rank 0 unless something has gone wrong.
        timestamps (``bool``): If ``True``, each log line will also contain the timestamp at
            which it was emitted. If you wish to parse out a line's timestamp and text,
            you can use :meth:`LogLine.from_line`.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`follow_run_logs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the generator, use ``return_value.result()`` with an optional
            ``timeout`` argument.

    Returns:
        If future is False:
            A line-by-line :obj:`Generator` of the logs for a run
        Otherwise:
            A :class:`~concurrent.futures.Future` of a line-by-line generator of the logs for a run
    """
    # A Future request for a log stream. The stream itself will generate Futures for individual log lines
    log_stream_request = run_in_threadpool(
        _threaded_follow_run_logs,
        run,
        rank=rank,
        timestamps=timestamps,
    )
    if not future:
        return log_stream_request.result(timeout=timeout)
    else:
        return log_stream_request
