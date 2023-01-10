# pylint: disable=duplicate-code

""" R1Z2 Cluster Definition """

from typing import List

from kubernetes import client

from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import (ClusterInstanceGPUConfiguration, ClusterInstances,
                                                        LocalClusterInstances)
from mcli.serverside.clusters.cluster_pv_setup import NFSVolume, PVDetails, PVSetupMixin
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.utils.utils_kube_labels import label

USER_WORKDISK_SERVER = '10.100.1.242'
USER_WORKDISK_PATH = '/mnt/interactive/r1z2'
USER_WORKDISK_STORAGE_CAPACITY = '10Gi'

a100_config = ClusterInstanceGPUConfiguration(
    gpu_type=GPUType.A100_40GB,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.A100_40G_1},
    cpus=64,
    cpus_per_gpu=8,
    memory=512,
    memory_per_gpu=64,
    storage=6400,
    storage_per_gpu=800,
)

cpu_config = ClusterInstanceGPUConfiguration(
    gpu_type=GPUType.NONE,
    gpu_nums=[0],
)

R1Z2_INSTANCES = LocalClusterInstances(gpu_configurations=[a100_config, cpu_config],)


class R1Z2Cluster(PVSetupMixin, GenericK8sCluster):
    """ R1Z2 Cluster Overrides """

    allowed_instances: ClusterInstances = R1Z2_INSTANCES
    storage_capacity: str = USER_WORKDISK_STORAGE_CAPACITY
    privileged: bool = True
    interactive: bool = True

    @property
    def pv_name(self) -> str:
        return f'workdisk-{self.namespace}'

    @property
    def pvc_name(self) -> str:
        return f'workdisk-{self.namespace}'

    def get_volume_details(self) -> PVDetails:
        """Returns the details of the PV spec
        """
        nfs_details = NFSVolume(USER_WORKDISK_PATH, USER_WORKDISK_SERVER)
        return PVDetails(nfs=nfs_details)

    def get_volumes(self) -> List[MCLIVolume]:
        """Get the volumes for the R1Z2 cluster, including the user's workdisk volume
        """
        volumes = super().get_volumes()

        # Get workdisk mount
        volume = client.V1Volume(
            name='workdisk',
            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                claim_name=self.pvc_name,
                read_only=False,
            ),
        )
        mount = client.V1VolumeMount(name='workdisk', mount_path='/workdisk')
        volumes.append(MCLIVolume(volume=volume, volume_mount=mount))

        return volumes

    def setup(self) -> bool:
        """Setup the cluster for future use.

        Raises:
            ClusterSetupError: Raised if setup failure prevents use of the cluster
        """
        if not self.setup_pv(self.mcli_cluster):
            return False
        return True
