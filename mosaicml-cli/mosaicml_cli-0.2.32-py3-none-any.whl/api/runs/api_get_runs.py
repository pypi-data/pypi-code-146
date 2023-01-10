"""get_runs SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.run import Run
from mcli.models.mcli_cluster import Cluster
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.utils.utils_run_status import RunStatus

__all__ = ['get_runs']

QUERY_FUNCTION = 'getRuns'
VARIABLE_DATA_NAME = 'getRunsData'
QUERY = f"""
query GetRuns(${VARIABLE_DATA_NAME}: GetRunsInput!) {{
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
def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[Run]:
    ...


@overload
def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[Run]]:
    ...


def get_runs(
    runs: Optional[Union[List[str], List[Run]]] = None,
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """List runs that have been launched in the MosaicML Cloud

    The returned list will contain all of the details stored about the requested runs.

    Arguments:
        runs: List of runs on which to get information
        clusters: List of clusters to filter runs. This can be a list of str or
            :type Cluster: objects. Only runs submitted to these clusters will be
            returned.
        gpu_types: List of gpu types to filter runs. This can be a list of str or
            :type GPUType: enums. Only runs scheduled on these GPUs will be returned.
        gpu_nums: List of gpu counts to filter runs. Only runs scheduled on this number
            of GPUs will be returned.
        statuses: List of run statuses to filter runs. This can be a list of str or
            :type RunStatus: enums. Only runs currently in these phases will be returned.
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :type concurrent.futures.Future:. If True, the
            call to `get_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of runs, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    filters = {}
    if runs:
        filters['name'] = {'in': [r.name if isinstance(r, Run) else r for r in runs]}
    if statuses:
        filters['status'] = {'in': [s.value if isinstance(s, RunStatus) else s for s in statuses]}
    if clusters:
        filters['cluster'] = {'in': [c.name if isinstance(c, Cluster) else c for c in clusters]}
    if gpu_types:
        filters['gpuType'] = {'in': [gt.value if isinstance(gt, GPUType) else gt for gt in gpu_types]}
    if gpu_nums:
        filters['gpuNum'] = {'in': gpu_nums}

    variables = {
        VARIABLE_DATA_NAME: {
            'filters': filters,
            'includeDeleted': False,
        },
    }

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
