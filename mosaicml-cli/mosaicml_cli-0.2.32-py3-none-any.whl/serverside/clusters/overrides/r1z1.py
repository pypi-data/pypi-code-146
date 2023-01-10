""" R1Z1 Cluster Definition """
from typing import Dict, List, Optional

from mcli import config
from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import (ClusterInstanceGPUConfiguration, ClusterInstances,
                                                        LocalClusterInstances, create_cpu_instances)
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.clusters.instance_type import InstanceType
from mcli.utils.utils_kube_labels import label

MAX_CPUS = 60

R1Z1_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'low': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'high': 'mosaicml-internal-research-emergency-priority'
}

a100_config = ClusterInstanceGPUConfiguration(
    gpu_type=GPUType.A100_80GB,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.A100_80G_1},
    cpus=64,
    cpus_per_gpu=8,
    memory=512,
    memory_per_gpu=64,
    storage=6400,
    storage_per_gpu=800,
)

cpu_instances = create_cpu_instances(max_cpu=64,
                                     max_memory=512,
                                     max_storage=2000,
                                     instance_cpus=[8, 16, 32, 64],
                                     selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.CPU})

R1Z1_INSTANCES = LocalClusterInstances(instance_types=cpu_instances, gpu_configurations=[a100_config])


class R1Z1Cluster(GenericK8sCluster):
    """ R1Z1 Cluster Overrides """

    allowed_instances: ClusterInstances = R1Z1_INSTANCES
    priority_class_labels = R1Z1_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'
    pod_group_scheduler: Optional[str] = 'scheduler-plugins-scheduler'

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        del instance_type
        tolerations = []
        mcli_config = config.MCLIConfig.load_config()
        if mcli_config.feature_enabled(feature=config.FeatureFlag.USE_DEMO_NODES):
            tolerations.append({
                'effect': 'NoSchedule',
                'key': label.mosaic.demo.DEMO_NODE,
                'operator': 'Equal',
                'value': 'true'
            })

        return tolerations

    def get_selectors(self,
                      instance_type: InstanceType,
                      partitions: Optional[List[str]] = None) -> Dict[str, List[str]]:
        selectors = super().get_selectors(instance_type, partitions=partitions)
        mcli_config = config.MCLIConfig.load_config()
        if mcli_config.feature_enabled(feature=config.FeatureFlag.USE_DEMO_NODES):
            selectors[label.mosaic.demo.DEMO_NODE] = ['true']
        return selectors
