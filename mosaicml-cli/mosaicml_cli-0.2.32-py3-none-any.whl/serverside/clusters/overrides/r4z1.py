""" R4Z1 Cluster Definition """
from mcli.serverside.clusters import GenericK8sCluster, GPUType, InstanceType
from mcli.serverside.clusters.cluster_instances import ClusterInstances
from mcli.serverside.job.mcli_k8s_resource_requirements_typing import MCLIK8sResourceRequirements
from mcli.utils.utils_kube_labels import label

AWS_T4_G1 = InstanceType(gpu_type=GPUType.T4,
                         gpu_num=1,
                         resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                             cpus=8,
                             memory=32,
                             storage=200,
                         ),
                         selectors={
                             label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_T4_G1,
                         })

AWS_T4_G4 = InstanceType(gpu_type=GPUType.T4,
                         gpu_num=4,
                         resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                             cpus=48,
                             memory=192,
                             storage=840,
                         ),
                         selectors={
                             label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_T4_G4,
                         })

AWS_T4_G8 = InstanceType(gpu_type=GPUType.T4,
                         gpu_num=8,
                         resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                             cpus=96,
                             memory=384,
                             storage=1680,
                         ),
                         selectors={
                             label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_T4_G8,
                         })

AWS_K80_24G_G1 = InstanceType(gpu_type=GPUType.K80,
                              gpu_num=1,
                              resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                                  cpus=4,
                                  memory=61,
                                  storage=100,
                              ),
                              selectors={
                                  label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_K80_24G_G1,
                              })

AWS_K80_24G_G8 = InstanceType(gpu_type=GPUType.K80,
                              gpu_num=8,
                              resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                                  cpus=32,
                                  memory=488,
                                  storage=160,
                              ),
                              selectors={
                                  label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_K80_24G_G8,
                              })

AWS_V100_16G_G1 = InstanceType(gpu_type=GPUType.V100_16GB,
                               gpu_num=1,
                               resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                                   cpus=8,
                                   memory=61,
                                   storage=100,
                               ),
                               selectors={
                                   label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_V100_16G_G1,
                               })

AWS_V100_16G_G8 = InstanceType(gpu_type=GPUType.V100_16GB,
                               gpu_num=8,
                               resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                                   cpus=64,
                                   memory=488,
                                   storage=160,
                               ),
                               selectors={
                                   label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_V100_16G_G8,
                               })

AWS_V100_32G_G8 = InstanceType(gpu_type=GPUType.V100_32GB,
                               gpu_num=8,
                               resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                                   cpus=96,
                                   memory=768,
                                   storage=1600,
                               ),
                               selectors={
                                   label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_V100_32G_G8,
                               })

AWS_A100_G8 = InstanceType(gpu_type=GPUType.A100_40GB,
                           gpu_num=8,
                           resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
                               cpus=96,
                               memory=1152,
                               storage=7200,
                           ),
                           selectors={
                               label.kubernetes_node.INSTANCE_TYPE: label.aws.AWS_A100_G8,
                           })

R4Z1_INSTANCES = ClusterInstances(instance_types=[
    AWS_T4_G1,
    AWS_T4_G4,
    AWS_T4_G8,
    AWS_K80_24G_G1,
    AWS_K80_24G_G8,
    AWS_V100_16G_G1,
    AWS_V100_16G_G8,
    AWS_V100_32G_G8,
    AWS_A100_G8,
])


class R4Z1Cluster(GenericK8sCluster):
    """ R4Z1 Cluster Overrides """

    allowed_instances: ClusterInstances = R4Z1_INSTANCES
