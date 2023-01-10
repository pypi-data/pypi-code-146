"""CLI getter for clusters"""
import logging
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, Generator, List

from mcli.api.cluster import get_clusters as api_get_cluster
from mcli.api.exceptions import MAPIErrorMessages, MAPIException, cli_error_handler
from mcli.api.model.cluster_details import ClusterDetails
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import FeatureFlag, MCLIConfig
from mcli.models import Cluster
from mcli.serverside.clusters.cluster_instances import UserInstanceRegistry
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.utils.utils_logging import WARN

logger = logging.getLogger(__name__)


@dataclass
class ClusterDisplayItem(MCLIDisplayItem):
    name: str
    context: str
    namespace: str
    gpu_types_and_nums: Dict[str, List[int]]


class ClusterDisplay(MCLIGetDisplay):
    """`mcli get cluster` display class
    """

    def __init__(self, cluster: List[ClusterDetails]):
        self.cluster = sorted(cluster)

    def __iter__(self) -> Generator[ClusterDisplayItem, None, None]:
        for c in self.cluster:
            yield ClusterDisplayItem(name=c.name,
                                     context=c.kubernetes_context,
                                     namespace=c.namespace,
                                     gpu_types_and_nums={i.gpu_type.value: i.gpu_nums for i in c.cluster_instances})


class KubeClusterDisplay(MCLIGetDisplay):
    """`mcli get cluster` display class that talks to kubernetes
    """

    def __init__(self, cluster: List[Cluster]):
        self.cluster = cluster

    def __iter__(self) -> Generator[ClusterDisplayItem, None, None]:
        gpu_registry = _get_gpu_registry(self.cluster)
        for cluster in self.cluster:
            yield ClusterDisplayItem(name=cluster.name,
                                     context=cluster.kubernetes_context,
                                     namespace=cluster.namespace,
                                     gpu_types_and_nums=gpu_registry[cluster.name])


def _get_gpu_registry(clusters: List[Cluster]) -> Dict[str, Dict[str, List[int]]]:
    user_registry = UserInstanceRegistry(clusters=clusters)
    gpu_info: Dict[str, Dict[str, List[int]]] = {}
    for cluster, gpu_dict in user_registry.registry.items():
        gpu_info[cluster] = {}
        for gpu_type, gpu_nums in gpu_dict.items():
            if gpu_type == GPUType.NONE:
                gpu_type_str = 'none (CPU only)'
            else:
                gpu_type_str = gpu_type.value
            gpu_info[cluster][gpu_type_str] = gpu_nums
    return gpu_info


@cli_error_handler('mcli get clusters')
def get_clusters(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    conf = MCLIConfig.load_config()
    if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
        try:
            clusters = api_get_cluster()
        except MAPIException as e:
            if e.status == HTTPStatus.NOT_FOUND:
                e.message = MAPIErrorMessages.NOT_FOUND_CLUSTER.value
            raise e

        display = ClusterDisplay(clusters)
        display.print(output)

    else:
        if conf.clusters:
            display = KubeClusterDisplay(conf.clusters)
            display.print(output)
        else:
            logger.warning(f'{WARN} No clusters found.\n\nTo create a cluster, run:\n\n[bold]mcli create cluster[/]')
    return 0
