""" MCLI Abstraction for Clusters and Utilization """
from __future__ import annotations

import functools
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from dateutil import parser

from mcli.api.exceptions import MAPI_DESERIALIZATION_ERROR
from mcli.api.schema.generic_model import DeserializableModel
from mcli.models.mcli_cluster import Cluster
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.utils.utils_serializable_dataclass import SerializableDataclass

logger = logging.getLogger(__name__)


def check_response(response: Dict[str, Any], expected: Set[str]) -> None:
    missing = expected - set(response)
    if missing:
        raise MAPI_DESERIALIZATION_ERROR


@dataclass
class ClusterUtilizationByRun:
    """Utilization for a specific run on a cluster
    """

    id: str
    user: str
    run_name: str
    gpu_num: int
    created_at: datetime

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterUtilizationByRun:
        check_response(response, {'id', 'userName', 'runName', 'gpuNum', 'createdAt'})
        return cls(
            id=response['id'],
            user=response['userName'],
            run_name=response['runName'],
            gpu_num=response['gpuNum'],
            created_at=parser.parse(response['createdAt']),
        )


@dataclass
class ClusterInstanceUtilization:
    """Utilization on a cluster instance
    """
    cluster_id: str
    gpu_type: str
    gpus_per_node: int
    num_nodes: int
    gpus_used: int
    gpus_available: int
    gpus_total: int

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterInstanceUtilization:
        check_response(response,
                       {'clusterId', 'gpuType', 'gpusPerNode', 'numNodes', 'gpusUsed', 'gpusAvailable', 'gpusTotal'})
        return cls(
            cluster_id=response['clusterId'],
            gpu_type=response['gpuType'],
            gpus_per_node=response['gpusPerNode'],
            num_nodes=response['numNodes'],
            gpus_used=response['gpusUsed'],
            gpus_available=response['gpusAvailable'],
            gpus_total=response['gpusTotal'],
        )


@dataclass
class ClusterUtilization:
    """Utilization on a cluster
    """
    anonymize_users: bool
    cluster_instance_utils: List[ClusterInstanceUtilization] = field(default_factory=list)
    active_by_user: List[ClusterUtilizationByRun] = field(default_factory=list)
    queued_by_user: List[ClusterUtilizationByRun] = field(default_factory=list)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterUtilization:
        check_response(response, {'clusterInstanceUtils', 'activeByUser', 'queuedByUser', 'anonymizeUsers'})
        return cls(cluster_instance_utils=[
            ClusterInstanceUtilization.from_mapi_response(i) for i in response['clusterInstanceUtils']
        ],
                   active_by_user=[ClusterUtilizationByRun.from_mapi_response(i) for i in response['activeByUser']],
                   queued_by_user=[ClusterUtilizationByRun.from_mapi_response(i) for i in response['queuedByUser']],
                   anonymize_users=response['anonymizeUsers'])


@dataclass
@functools.total_ordering
class ClusterInstance:
    """Instance of a cluster
    """

    gpu_type: GPUType
    gpu_nums: List[int] = field(default_factory=list)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterInstance:
        check_response(response, {'gpuType', 'gpuNums'})
        return cls(gpu_type=GPUType.from_string(response['gpuType']), gpu_nums=response['gpuNums'])

    @classmethod
    def from_available_instances(cls, available_instances: Dict[GPUType, List[int]]) -> List[ClusterInstance]:
        return [ClusterInstance(gpu_type, gpu_nums) for gpu_type, gpu_nums in available_instances.items()]

    def __lt__(self, other: ClusterInstance):
        return self.gpu_type < other.gpu_type


@dataclass
@functools.total_ordering
class ClusterDetails(SerializableDataclass, DeserializableModel):
    """Details of a cluster, including instances and utilization
    """

    name: str
    cluster_instances: List[ClusterInstance] = field(default_factory=list)
    utilization: Optional[ClusterUtilization] = None

    kubernetes_context: str = ''
    namespace: str = ''

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> ClusterDetails:
        check_response(response, {'name'})
        utilization = None if 'utilization' not in response else ClusterUtilization.from_mapi_response(
            response['utilization'])
        return cls(
            name=response['name'],
            cluster_instances=[ClusterInstance.from_mapi_response(i) for i in response.get('allowedInstances', [])],
            utilization=utilization,
        )

    def __lt__(self, other: ClusterDetails):
        return self.name < other.name

    def to_cluster(self) -> Cluster:
        return Cluster(name=self.name, kubernetes_context='', namespace='')
