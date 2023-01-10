""" R7Z9 Cluster Definition """
from typing import Optional

from mcli.models.mcli_cluster import Cluster
from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import (ClusterInstanceGPUConfiguration, ClusterInstances,
                                                        LocalClusterInstances)
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.utils.utils_kube_labels import label

a100_config = ClusterInstanceGPUConfiguration(
    gpu_type=GPUType.A100_40GB,
    gpu_nums=[8, 16, 24],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.OCI_GB4_8},
    cpus=128,
    cpus_per_gpu=16,
    memory=2048,
    memory_per_gpu=256,
    storage=8000,
    storage_per_gpu=1000,
    multinode_rdma_roce=1,
)

cpu_config = ClusterInstanceGPUConfiguration(
    gpu_type=GPUType.NONE,
    gpu_nums=[0],
)

R7Z9_INSTANCES = LocalClusterInstances(gpu_configurations=[a100_config, cpu_config])


class R7Z9Cluster(GenericK8sCluster):
    """ R7Z9 Cluster Overrides """

    allowed_instances: ClusterInstances = R7Z9_INSTANCES

    pod_group_scheduler: Optional[str] = 'scheduler-plugins-scheduler'
    privileged: bool = True

    def __init__(self, mcli_cluster: Cluster) -> None:
        super().__init__(mcli_cluster)
        self.interactive = True
