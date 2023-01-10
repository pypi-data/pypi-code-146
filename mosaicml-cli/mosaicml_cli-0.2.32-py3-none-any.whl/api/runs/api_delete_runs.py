""" Delete a run. """
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.run import Run

__all__ = ['delete_runs']

QUERY_FUNCTION = 'deleteRuns'
VARIABLE_DATA_NAME = 'getRunsData'
QUERY = f"""
mutation DeleteRuns(${VARIABLE_DATA_NAME}: GetRunsInput!) {{
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
def delete_runs(runs: Union[List[str], List[Run]],
                timeout: Optional[float] = 10,
                future: Literal[False] = False) -> List[Run]:
    ...


@overload
def delete_runs(runs: Union[List[str], List[Run]],
                timeout: Optional[float] = None,
                future: Literal[True] = True) -> Future[List[Run]]:
    ...


def delete_runs(runs: Union[List[str], List[Run]], timeout: Optional[float] = 10, future: bool = False):
    """Delete a list of runs in the MosaicML Cloud

    Any runs that are currently running will first be stopped.

    Args:
        runs: A list of runs or run names to delete
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :type concurrent.futures.Future:. If True, the
            call to `delete_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A list of :type Run: for the runs that were deleted
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
