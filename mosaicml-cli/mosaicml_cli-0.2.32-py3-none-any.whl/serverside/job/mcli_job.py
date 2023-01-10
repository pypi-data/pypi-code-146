""" Kubernetes Intermediate Job Abstraction """

from __future__ import annotations

import logging
import os
import uuid
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, cast

import yaml
from kubernetes import client

from mcli import config
from mcli.models import Cluster, FinalRunConfig, MCLIEnvVar, MCLIIntegration
from mcli.models.mcli_integration import IntegrationType
from mcli.objects.integrations.mosaicml_agent import MCLIMosaicMLAgentIntegration
from mcli.serverside.clusters import GenericK8sCluster, GPUType, InstanceType
from mcli.serverside.clusters.cluster_instances import InstanceTypeUnavailable
from mcli.serverside.job.mcli_k8s_config_map_typing import MCLIK8sConfigMap
from mcli.serverside.job.mcli_k8s_job import MCLIConfigMap, MCLIK8sJob, MCLIVolume
from mcli.serverside.job.mcli_k8s_service_typing import MCLIK8sService
from mcli.utils.utils_kube_labels import label

logger = logging.getLogger(__name__)

COMPOSER_RUN_NAME_KEY = 'COMPOSER_RUN_NAME'
COMPSOSER_YAHP_RUN_NAME_KEY = 'RUN_NAME'
PARTITIONS_KEY = 'MCLOUD_PARTITIONS'

PARAMETERS_MOUNT_PATH = '/mnt/config'
PARAMETERS_FILE_NAME = 'parameters.yaml'
RUN_CONFIG_FILE_NAME = 'run_config.yaml'

TOMBSTONE_FILE = '/tmp/tombstone'


class MCLIJobType(Enum):
    RUN = 'run'
    INTERACTIVE = 'interactive'


@dataclass
class MCLIJob():
    """ Kubernetes Intermediate Job Abstraction """

    run_id: str
    run_name: str
    instance_type: InstanceType
    cluster: GenericK8sCluster
    image: str
    optimization_level: int
    integrations: List[MCLIIntegration]
    env_variables: List[MCLIEnvVar]

    command: str
    parameters: Dict[str, Any]

    config: FinalRunConfig

    partitions: Optional[List[str]] = None

    @property
    def unique_name(self) -> str:
        """Gets a unique name from user set name and run_id"""
        return self.run_name + '-' + self.run_id

    @classmethod
    def from_final_run_config(cls, run_config: FinalRunConfig) -> MCLIJob:
        mcli_config: config.MCLIConfig = config.MCLIConfig.load_config()

        env_variables: List[MCLIEnvVar] = []
        env_variables += mcli_config.environment_variables
        env_variables += [MCLIEnvVar.from_dict(x) for x in run_config.env_variables]

        integrations: List[MCLIIntegration] = []
        for integration_data in run_config.integrations:
            integrations.append(MCLIIntegration.from_dict(integration_data))
        integrations.reverse()  # Since commands are prepended, add them in reverse order

        found_cluster: Optional[Cluster] = None
        for candidate_cluster in mcli_config.clusters:
            if candidate_cluster.name == run_config.cluster:
                found_cluster = candidate_cluster
                break
        clusters_available_str = ', '.join([x.name for x in mcli_config.clusters])
        assert found_cluster, (f'Unable to find cluster: {run_config.cluster}'
                               f' in registered clusters: {clusters_available_str}')
        cluster = GenericK8sCluster.from_mcli_cluster(found_cluster)

        gpu_type = GPUType.from_string(run_config.gpu_type)
        try:
            instance_type = cluster.get_instance_type(
                gpu_type=gpu_type,
                gpu_num=run_config.gpu_num,
                cpus=run_config.cpus,
            )
        except InstanceTypeUnavailable as it_unavailable_exception:
            it_unavailable_exception.current_cluster_name = cluster.mcli_cluster.name
            other_clusters = [
                GenericK8sCluster.from_mcli_cluster(x) for x in mcli_config.clusters if x.name != run_config.cluster
            ]
            other_clusters_aits: Dict[str, Dict[GPUType, List[int]]] = {
                x.mcli_cluster.name: x.allowed_instances.available_instances for x in other_clusters
            }
            it_unavailable_exception.all_cluster_available_instances = other_clusters_aits
            raise it_unavailable_exception

        if run_config.entrypoint:
            command = f"""
            if [ -f "{run_config.entrypoint}" ];
            then
                composer {run_config.entrypoint} -f {os.path.join(PARAMETERS_MOUNT_PATH, PARAMETERS_FILE_NAME)}
            else
                echo "[ERROR] {run_config.entrypoint} not found.
                Please make sure that the entrypoint starts with the top level folder of a git repo.
                The current working directory has the following in it:" $(ls)
            fi
            """
            run_config.command = command

        data = {
            'run_id': run_config.run_id,
            'run_name': run_config.name,
            'instance_type': instance_type,
            'cluster': cluster,
            'image': run_config.image,
            'optimization_level': run_config.optimization_level,
            'integrations': integrations,
            'env_variables': env_variables,
            'command': run_config.command,
            'parameters': run_config.parameters,
            'config': run_config,
            'partitions': run_config.partitions,
        }

        return MCLIJob(**data)

    def _get_multinode_env_vars(self) -> List[client.V1EnvVar]:
        local_world_size = self.instance_type.local_world_size
        namespace = self.cluster.namespace

        if local_world_size is None:
            raise ValueError('Multi-node jobs are not currently supported on this instance type.')

        simple_env_vars = [
            client.V1EnvVar(k, v) for (k, v) in ({
                'WORLD_SIZE': str(self.instance_type.num_nodes * local_world_size),
                'MASTER_ADDR': f'{self.unique_name}-0.svc-{self.unique_name}.{namespace}.svc.cluster.local',
                'MASTER_PORT': str(7501),
            }).items()
        ]

        node_rank_env_var = client.V1EnvVar(
            name='NODE_RANK',
            value_from=client.V1EnvVarSource(
                field_ref={'fieldPath': f"metadata.annotations['{label.kube_batch.POD_RANK}']"}))

        return [*simple_env_vars, node_rank_env_var]

    def get_kubernetes_job(self, kubernetes_cluster: GenericK8sCluster) -> MCLIK8sJob:
        kubernetes_job = cast(MCLIK8sJob, MCLIK8sJob.empty(name=self.unique_name))
        assert isinstance(kubernetes_job, MCLIK8sJob)
        kubernetes_job.container.image = self.image
        kubernetes_job.container.command = ['bash', '-c']
        kubernetes_job.container.command_string = self.command
        kubernetes_job.container.image_pull_policy = 'Always'
        kubernetes_job.metadata = client.V1ObjectMeta(name=self.unique_name)

        kubernetes_job.pod_spec.security_context = client.V1PodSecurityContext(
            run_as_user=0,
            run_as_group=0,
        )

        kubernetes_job.spec.ttl_seconds_after_finished = config.JOB_TTL

        for env_item in self.env_variables:
            kubernetes_job.add_env_var(client.V1EnvVar(
                name=env_item.key,
                value=env_item.value,
            ))

        kubernetes_job.add_env_var(client.V1EnvVar(
            name=COMPOSER_RUN_NAME_KEY,
            value=self.unique_name,
        ))
        kubernetes_job.add_env_var(client.V1EnvVar(
            name=COMPSOSER_YAHP_RUN_NAME_KEY,
            value=self.unique_name,
        ))

        # if partition provided, add it as an env var
        if self.partitions:
            kubernetes_job.add_env_var(
                client.V1EnvVar(name=PARTITIONS_KEY, value=",".join([str(p) for p in self.partitions])))

        if self.instance_type.num_nodes > 1:
            kubernetes_job.spec.completion_mode = 'Indexed'
            kubernetes_job.spec.completions = self.instance_type.num_nodes
            kubernetes_job.spec.parallelism = self.instance_type.num_nodes

            kubernetes_job.pod_spec.subdomain = 'svc-' + self.unique_name

            kubernetes_job.set_privileged(True)

            kubernetes_job.pod_spec.host_network = True
            kubernetes_job.pod_spec.dns_policy = 'ClusterFirstWithHostNet'

            if kubernetes_cluster.pod_group_scheduler is not None:
                pod_group_label = {'pod-group.scheduling.sigs.k8s.io': self.unique_name}
                pod_template_spec = cast(client.V1PodTemplateSpec, kubernetes_job.spec.template)
                pod_template_spec.metadata = client.V1ObjectMeta(labels=pod_group_label)
                kubernetes_job.pod_spec.scheduler_name = kubernetes_cluster.pod_group_scheduler

            assert isinstance(kubernetes_job.container.args, List) and len(kubernetes_job.container.args) == 1
            kubernetes_job.add_command(
                command='ulimit -l unlimited',
                error_message='Unable to set ulimit. Please ensure you are running as root.',
                required=True,
            )

            for env_var in self._get_multinode_env_vars():
                kubernetes_job.add_env_var(env_var)

        for integration in self.integrations:
            success = integration.add_to_job(kubernetes_job=kubernetes_job)
            if not success:
                logger.warning(f'Unable to add integration: \n{integration}')

        # Add the mosaicml agent which is flagged only for internal users right now
        mosaicml_agent = MCLIMosaicMLAgentIntegration(
            integration_type=IntegrationType.mosaicml_agent,
            optimization_level=self.optimization_level,
        )
        mosaicml_agent.add_to_job(kubernetes_job=kubernetes_job)

        # Add tombstone for stopping a run
        self.apply_run_tombstone(kubernetes_job)

        # Configure for instance
        kubernetes_job.container.resources = self.instance_type.resource_requirements
        if isinstance(kubernetes_job.container.resources.limits, dict) and \
            kubernetes_job.container.resources.limits.get(label.nvidia.GPU, 0) == 0:
            # If no GPUs requested, limit the container visibility with this envvar.
            # see: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#gpu-enumeration
            kubernetes_job.add_env_var(client.V1EnvVar(
                name='NVIDIA_VISIBLE_DEVICES',
                value='void',
            ))

        # Apply feature-flag changes
        self.apply_feature_flag_modifications(kubernetes_job)
        return kubernetes_job

    def apply_feature_flag_modifications(self, kubernetes_job: MCLIK8sJob):
        """Apply any modifications to the job that are required by they user's feature flags
        """

        conf = config.MCLIConfig.load_config()

        if conf.feature_enabled(config.FeatureFlag.USE_DEMO_NODES) and conf.feature_enabled(
                config.FeatureFlag.MLPERF_MODE):
            kubernetes_job.set_privileged(True)

    def apply_run_tombstone(self, kubernetes_job: MCLIK8sJob):
        """Add a 'tombstone' file that can be used to signal a job to stop without deleting it

        This adds a file at `TOMBSTONE_FILE` that indicates a run should continue to leave. To mark the job for
        failure, simply delete the `TOMBSTONE_FILE` using the kubernetes API. When the file is deleted, the liveness
        probe will fail, causing the pod to be evicted but not deleted from etcd.

        Args:
            kubernetes_job: The job object to add the TOMBSTONE file to
        """
        # Add the tombstone file as a part of the command
        kubernetes_job.add_command(
            f'touch {TOMBSTONE_FILE}',
            'Could not create tombstone file',
            required=True,
        )

        # Probe will use `cat` to determine file's existence
        cmd = client.V1ExecAction(command=['cat', TOMBSTONE_FILE])

        # Add a startup probe
        # Startup probe makes sure the file is created so we don't get any race conditions
        # with the readiness probe. Let this be fairly tolerant
        startup = client.V1Probe(_exec=cmd, failure_threshold=10, period_seconds=1)
        kubernetes_job.container.startup_probe = startup

        # Add a liveness probe
        liveness = client.V1Probe(_exec=cmd, failure_threshold=3, period_seconds=10, timeout_seconds=10)
        kubernetes_job.container.liveness_probe = liveness

    def get_config_map(self) -> MCLIConfigMap:
        data = yaml.dump({k: v for k, v in self.parameters.items() if not k.startswith('_')})
        config_data = yaml.dump(asdict(self.config))
        cm = MCLIK8sConfigMap(
            api_version='v1',
            kind='ConfigMap',
            data={
                PARAMETERS_FILE_NAME: data,
                RUN_CONFIG_FILE_NAME: config_data,
            },
        )
        cm.metadata = client.V1ObjectMeta(name=self.unique_name)
        cm_volume = client.V1Volume(
            name='config',
            config_map=client.V1ConfigMapVolumeSource(name=self.unique_name),
        )
        cm_mount = client.V1VolumeMount(
            name='config',
            mount_path=PARAMETERS_MOUNT_PATH,
        )

        return MCLIConfigMap(
            config_map=cm,
            config_volume=MCLIVolume(
                volume=cm_volume,
                volume_mount=cm_mount,
            ),
        )

    def get_service(self) -> Optional[MCLIK8sService]:
        if self.instance_type.num_nodes == 1:
            return None

        svc = MCLIK8sService(
            api_version='v1',
            kind='Service',
            metadata=client.V1ObjectMeta(name="svc-" + self.unique_name),
            spec=client.V1ServiceSpec(
                selector={label.mosaic.JOB: self.unique_name},
                cluster_ip='None',
                ports=[client.V1ServicePort(port=7500)],  # This port won't be used, but it still must be valid.
            ))

        return svc

    def get_pod_group(self, kubernetes_cluster: GenericK8sCluster) -> Optional[Dict[str, Any]]:
        if self.instance_type.num_nodes == 1 or not kubernetes_cluster.pod_group_scheduler:
            return None

        return {
            'apiVersion': 'scheduling.sigs.k8s.io/v1alpha1',
            'kind': 'PodGroup',
            'metadata': client.V1ObjectMeta(
                name=self.unique_name,
                namespace=self.cluster.namespace,
            ),
            'spec': {
                'scheduleTimeoutSeconds': 10,
                'minMember': self.instance_type.num_nodes,
            },
        }

    def get_shared_metadata(self) -> client.V1ObjectMeta:
        labels = {
            label.mosaic.JOB:
                self.unique_name,
            'type':
                'mcli',
            label.mosaic.LAUNCHER_TYPE:
                'mcli',
            **label.mosaic.compute_selectors.get_compute_selection_labels(
                cluster=self.cluster.mcli_cluster.name,
                gpu_type=str(self.instance_type.gpu_type.value),
                gpu_num=self.instance_type.gpu_num,
                cpus=self.instance_type.cpus,
            ),
            **label.mosaic.version.get_version_labels(),
            **label.mosaic.billing.get_billing_labels(
                num_nodes=self.instance_type.num_nodes,
                uuid=str(uuid.uuid4()),
                customer='00000000-0000-0000-0000-000000000000',
                instance_size=self.instance_type.instance_size,
                cluster=self.cluster.mcli_cluster.kubernetes_context,
            ),
        }
        shared_metadata = client.V1ObjectMeta(
            labels=labels,
            namespace=self.cluster.mcli_cluster.namespace,
        )

        return shared_metadata
