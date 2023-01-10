""" Microk8s Cluster Definition """
from typing import Optional, Set

from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import ClusterInstances, LocalClusterInstances
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.clusters.instance_type import InstanceType

MICROK8S_INSTANCES = LocalClusterInstances(instance_types=[InstanceType(
    gpu_type=GPUType.NONE,
    gpu_num=0,
)])


class Microk8sCluster(GenericK8sCluster):
    """ Microk8s Cluster Overrides """
    partitions: Optional[Set[str]] = {"1"}
    allowed_instances: ClusterInstances = MICROK8S_INSTANCES
