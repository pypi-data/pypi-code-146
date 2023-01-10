"""get_clusters SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.cluster_details import ClusterDetails
from mcli.models.mcli_cluster import Cluster

__all__ = ['get_clusters']

QUERY_FUNCTION = 'getClusters'
VARIABLE_DATA_NAME = 'getClustersData'
QUERY = f"""
query GetClusters(${VARIABLE_DATA_NAME}: GetClustersInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    name
    allowedInstances {{
      gpuType
      gpuNums
    }}
  }}
}}"""
QUERY_UTILIZATION = f"""
query GetClusters(${VARIABLE_DATA_NAME}: GetClustersInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    name
    utilization {{
      clusterInstanceUtils {{
        clusterId
        gpuType
        gpusPerNode
        numNodes
        gpusUsed
        gpusAvailable
        gpusTotal
      }}
      activeByUser {{
        id
        createdAt
        userName
        runName
        gpuNum
      }}
      queuedByUser {{
        id
        createdAt
        userName
        runName
        gpuNum
      }}
      anonymizeUsers
    }}
  }}
}}"""


@overload
def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    include_utilization: bool = False,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> List[ClusterDetails]:
    ...


@overload
def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    include_utilization: bool = False,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[List[ClusterDetails]]:
    ...


def get_clusters(
    clusters: Optional[Union[List[str], List[Cluster]]] = None,
    include_utilization: bool = False,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Get clusters available in the MosaicML Cloud

    Arguments:
        clusters (:class:`~mcli.models.mcli_cluster.Cluster`): List of
            :class:`~mcli.models.mcli_cluster.Cluster` objects or cluster name
            strings to get.
        include_utilization (``bool``): Include information on how the cluster is currently
            being utilized
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`get_clusters` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.cluster_details.ClusterDetails` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """
    filters = {}
    if clusters:
        cluster_names = [c.name if isinstance(c, Cluster) else c for c in clusters]
        filters['name'] = {'in': cluster_names}

    variables = {
        VARIABLE_DATA_NAME: {
            'filters': filters
        },
    }

    response = run_plural_mapi_request(
        query=QUERY_UTILIZATION if include_utilization else QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=ClusterDetails,
        variables=variables,
    )

    if not future:
        return response.result(timeout=timeout)
    else:
        return response
