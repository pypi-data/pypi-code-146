"""Implementation of the delete_runs API for Kubernetes"""
from __future__ import annotations

import logging
from concurrent.futures import Future
from http import HTTPStatus
from typing import Dict, List, Optional, Set, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_kube_in_threadpool
from mcli.api.exceptions import KubernetesException
from mcli.api.model.run import Run
from mcli.models.mcli_cluster import Cluster
from mcli.utils.utils_kube import ClusterRun, KubeContext
from mcli.utils.utils_kube import delete_runs as _util_delete_runs

__all__ = ['delete_runs']

logger = logging.getLogger(__name__)


def _threaded_delete_runs(runs: Union[List[str], List[Run]]) -> List[Run]:
    """Threaded function for deleting a list of runs

    Args:
        runs: List of runs to delete

    Returns:
        A list of :type Run: that were deleted
    """
    if not runs:
        return []

    if not all(isinstance(r, Run) for r in runs):
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.kube.runs import get_runs
        runs = get_runs(runs=[r.name if isinstance(r, Run) else r for r in runs])
    runs = cast(List[Run], runs)

    cluster_runs = _get_cluster_runs(runs)
    success = _util_delete_runs(cluster_runs)
    if not success:
        # TODO: Figure out what error to throw here
        raise KubernetesException(status=HTTPStatus.INTERNAL_SERVER_ERROR, message='Delete failed!')
    return runs


def _get_cluster_runs(runs: List[Run]) -> List[ClusterRun]:
    """Get a list of ClusterRun tuples so we know where to look for each run
    """

    cluster_runs: List[ClusterRun] = []
    cluster_context_map: Dict[str, KubeContext] = {}
    unknown_clusters: Set[str] = set()
    for run in runs:
        cluster = run.config.cluster
        if cluster not in cluster_context_map:
            try:
                context = Cluster.get_by_name(cluster).to_kube_context()
            except KeyError:
                unknown_clusters.add(cluster)
                continue
            cluster_context_map[cluster] = context
        cluster_runs.append(ClusterRun(run.name, cluster_context_map[cluster]))

    if unknown_clusters:
        names = ', '.join(sorted(list(unknown_clusters)))
        message = f'Some runs could not be deleted because the following clusters are not configured locally: {names}'
        if cluster_runs:
            # Some runs can be deleted, so just throw a warning
            logger.warning(message)
        else:
            # No runs can be deleted. This is likely a full failure, so let's throw an error
            raise RuntimeError(message)
    return cluster_runs


@overload
def delete_runs(
    runs: Union[List[str], List[Run]],
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[Run]:
    ...


@overload
def delete_runs(
    runs: Union[List[str], List[Run]],
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[Run]]:
    ...


def delete_runs(
    runs: Union[List[str], List[Run]],
    timeout: Optional[float] = 10,
    future: bool = False,
) -> Union[List[Run], Future[List[Run]]]:
    """Delete a list of runs

    Delete a list of runs in the MosaicML Cloud. Any runs that are currently running will
    first be stopped.

    Args:
        runs (``Optional[List[str] | List[``:class:`~mcli.api.model.run.Run` ``]]``):
            A list of runs or run names to delete. Using :class:`~mcli.api.model.run.Run`
            objects is most efficient. See the note below.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`delete_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Returns:
        If future is False:
            A list of deleted :class:`~mcli.api.model.run.Run` objects
        Otherwise:
            A :class:`~concurrent.futures.Future` for the list

    Note:
        The Kubernetes API requires the cluster for each run. If you provide ``runs`` as a
        list of names, we will get this by calling :func:`~mcli.sdk.get_runs`. Since
        a common way to get the list of runs is to have already called
        :func:`~mcli.sdk.get_runs`, you can avoid a second call by passing
        the output of that call in directly.
    """

    kube_future = run_kube_in_threadpool(_threaded_delete_runs, runs=runs)

    if not future:
        return kube_future.result(timeout=timeout)
    else:
        return kube_future
