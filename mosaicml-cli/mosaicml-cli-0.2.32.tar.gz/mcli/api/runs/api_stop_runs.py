""" Stop a run. """
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.run import Run

__all__ = ['stop_runs']

QUERY_FUNCTION = 'stopRuns'
VARIABLE_DATA_NAME = 'getRunsData'
QUERY = f"""
mutation StopRuns(${VARIABLE_DATA_NAME}: GetRunsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    runInput
    status
    createdAt
    startedAt
    completedAt
    updatedAt
    reason
  }}
}}"""


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


def stop_runs(runs: Union[List[str], List[Run]], timeout: Optional[float] = 10, future: bool = False):
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
    # Extract run names
    run_names = [r.name if isinstance(r, Run) else r for r in runs]

    filters = {}
    if run_names:
        filters['name'] = {'in': run_names}

    variables = {VARIABLE_DATA_NAME: {'filters': filters}}

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )
    if not future:
        return response.result(timeout=timeout)
    else:
        return response
