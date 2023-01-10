"""Implements the stop_runs API for Kubernetes"""
from __future__ import annotations

from concurrent.futures import Future, as_completed
from http import HTTPStatus
from typing import Dict, List, Optional, Union, cast, overload

from kubernetes.client.exceptions import ApiException
from typing_extensions import Literal

from mcli.api.engine.engine import run_kube_in_threadpool
from mcli.api.exceptions import KubernetesException
from mcli.api.kube.runs.api_delete_runs import _get_cluster_runs
from mcli.api.model import Run
from mcli.utils.utils_kube import ClusterRun, delete_pod_tombstone, get_rank0_pod, use_context
from mcli.utils.utils_run_status import RunStatus


def _threaded_stop_runs(runs: Union[List[str], List[Run]]):
    """Threaded function for stopping a list of runs

    Args:
        runs: List of runs to stop

    Returns:
        A list of :type Run: that were stopped

    Raises:
        KubernetesException: Raised if stopping any of the requested runs failed.
    """
    if not runs:
        return []

    if not all(isinstance(r, Run) for r in runs):
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.kube.runs import get_runs
        runs = get_runs(runs=[r.name if isinstance(r, Run) else r for r in runs])
    runs = cast(List[Run], runs)

    run_dict: Dict[str, Run] = {r.name: r for r in runs}
    cluster_runs = _get_cluster_runs(runs)
    futures: Dict[Future[bool], str] = {run_kube_in_threadpool(_get_and_stop_pods, pr): pr.name for pr in cluster_runs
                                       }  # type: ignore
    failed_runs: List[str] = []
    failed_status: Optional[HTTPStatus] = None
    for fs in as_completed(futures):
        run_name = futures[fs]
        run = run_dict[run_name]
        try:
            _ = fs.result()  # Succeeded if it didn't error
            run.status = RunStatus.STOPPED
        except (KubernetesException, ApiException) as e:
            failed_runs.append(run_name)
            # Keep the last failure status for the error raised below
            failed_status = e.status if isinstance(e, KubernetesException) else HTTPStatus(e.status)
    if failed_runs:
        raise KubernetesException(status=failed_status or HTTPStatus.INTERNAL_SERVER_ERROR,
                                  message=f'Failed to stop {len(failed_runs)} runs. Please try again. '
                                  f'The runs that failed to stop were:\n{failed_runs}')

    return list(run_dict.values())


def _get_and_stop_pods(cluster_run: ClusterRun) -> bool:
    """Stop a single run by first getting the rank 0 pod and then deleting its tombstone
    file

    NOTE: Since the run will error if the rank 0 pod goes down, we only need to stop it
    explicitly.
    """

    namespace = cluster_run.context.namespace
    assert namespace is not None, 'Invalid cluster: namespace should never be None'

    with use_context(cluster_run.context.name):
        try:
            # Get the rank 0 pod. If it doesn't exist, then return True since the run has likely failed
            rank0_pod = get_rank0_pod(cluster_run.name, namespace)
        except RuntimeError:
            return True
        return delete_pod_tombstone(rank0_pod, namespace)


@overload
def stop_runs(runs: Union[List[str], List[Run]],
              timeout: Optional[float] = 10,
              future: Literal[False] = False) -> List[Run]:
    ...


@overload
def stop_runs(runs: Union[List[str], List[Run]],
              timeout: Optional[float] = None,
              future: Literal[True] = True) -> Future[List[Run]]:
    ...


def stop_runs(runs: Union[List[str], List[Run]],
              timeout: Optional[float] = 10,
              future: bool = False) -> Union[List[Run], Future[List[Run]]]:
    """Stop a list of runs

    Stop a list of runs currently running in the MosaicML Cloud.

    Args:
        runs (``Optional[List[str] | List[``:class:`~mcli.api.model.run.Run` ``]]``):
            A list of runs or run names to stop. Using :class:`~mcli.api.model.run.Run`
            objects is most efficient. See the note below.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`stop_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        KubernetesException: Raised if stopping any of the requested runs failed. All
            successfully stopped runs will have the status ```RunStatus.STOPPED```. You can
            freely retry any stopped and unstopped runs if this error is raised due to a
            connection issue.

    Returns:
        If future is False:
            A list of stopped :class:`~mcli.api.model.run.Run` objects
        Otherwise:
            A :class:`~concurrent.futures.Future` for the list

    Note:
        The Kubernetes API requires the cluster for each run. If you provide ``runs`` as a
        list of names, we will get this by calling :func:`~mcli.sdk.get_runs`. Since
        a common way to get the list of runs is to have already called
        :func:`~mcli.sdk.get_runs`, you can avoid a second call by passing
        the output of that call in directly.

    Warning:
        Stopping runs does not occur immediately. You may see up to a 40 second delay
        between your request and the run actually stopping.
    """

    response = run_kube_in_threadpool(_threaded_stop_runs, runs)

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
