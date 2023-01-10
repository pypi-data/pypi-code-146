""" R3Z1 Cluster Definition """
from mcli.serverside.clusters import GenericK8sCluster, GPUType, InstanceType
from mcli.serverside.clusters.cluster_instances import ClusterInstances
from mcli.serverside.job.mcli_k8s_resource_requirements_typing import MCLIK8sResourceRequirements
from mcli.utils.utils_kube_labels import label

GCP_T4_G4 = InstanceType(gpu_type=GPUType.T4,
                         gpu_num=4,
                         resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                             cpus=48,
                             memory=196,
                             storage=3000,
                         ),
                         selectors={
                             label.mosaic.com.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_T4_G4,
                         })

GCP_V100_16G_G8 = InstanceType(gpu_type=GPUType.V100_16GB,
                               gpu_num=8,
                               resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                                   cpus=64,
                                   memory=440,
                                   storage=3000,
                               ),
                               selectors={
                                   label.mosaic.com.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_V100_G8,
                               })

GCP_A100_G8 = InstanceType(gpu_type=GPUType.A100_40GB,
                           gpu_num=8,
                           resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                               cpus=96,
                               memory=680,
                               storage=3000,
                           ),
                           selectors={
                               label.mosaic.com.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_A100_G8,
                           })

GCP_A100_G16 = InstanceType(gpu_type=GPUType.A100_40GB,
                            gpu_num=16,
                            resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                                cpus=96,
                                memory=1360,
                                storage=3000,
                            ),
                            selectors={
                                label.mosaic.com.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_A100_G16,
                            },
                            _local_world_size=16)

R3Z1_INSTANCES = ClusterInstances(instance_types=[
    GCP_T4_G4,
    GCP_V100_16G_G8,
    GCP_A100_G8,
    GCP_A100_G16,
])


class R3Z1Cluster(GenericK8sCluster):
    """ R3Z1 Cluster Overrides """

    allowed_instances: ClusterInstances = R3Z1_INSTANCES
