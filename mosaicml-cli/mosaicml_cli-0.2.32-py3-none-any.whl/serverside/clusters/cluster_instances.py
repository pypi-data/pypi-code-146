""" Defines what Instance Types a Cluster supports """
from __future__ import annotations

import logging
import textwrap
from typing import TYPE_CHECKING, Dict, List, NamedTuple, Optional, Tuple

from mcli.api.exceptions import MAPIException, MCLIConfigError
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.serverside.clusters.instance_type import InstanceType
from mcli.serverside.job.mcli_k8s_resource_requirements_typing import (SAFETY_MARGIN_CPU, SAFETY_MARGIN_MEMORY,
                                                                       SAFETY_MARGIN_STORAGE,
                                                                       MCLIK8sResourceRequirements)
from mcli.utils.utils_logging import set_indent

if TYPE_CHECKING:
    from mcli.api.model.cluster_details import ClusterDetails
    from mcli.models.mcli_cluster import Cluster

logger = logging.getLogger(__name__)


class InstanceTypeUnavailable(Exception):
    """ Raised if the instance type is not available on a cluster"""
    attempted_instance_type: InstanceTypeLookupData
    current_cluster_name: Optional[str] = None
    current_cluster_available_instances: Dict[GPUType, List[int]] = {}
    all_cluster_available_instances: Dict[str, Dict[GPUType, List[int]]] = {}

    def __init__(
        self,
        attempted_instance_type: InstanceTypeLookupData,
        current_cluster_available_instances: Dict[GPUType, List[int]],
    ) -> None:
        self.attempted_instance_type = attempted_instance_type
        self.current_cluster_available_instances = current_cluster_available_instances
        self.all_cluster_available_instances = {}
        super().__init__()

    @staticmethod
    def get_instances_description(available_dict: Dict[GPUType, List[int]]) -> str:
        gpus = sorted(list(available_dict.keys()))

        def get_num_str(nums: List[int]) -> str:
            return ', '.join([f'{ii}x' for ii in nums])

        descs = [f'{get_num_str(available_dict[gpu])} {gpu}' for gpu in gpus]
        return '\n'.join(descs)

    def __str__(self) -> str:
        ait = self.attempted_instance_type

        if ait.gpu_type == GPUType.NONE:
            instance_desc = f'{ait.cpus or 1} CPU(s) and 0 GPUs'
        else:
            instance_desc = f'{ait.gpu_num}x {ait.gpu_type} GPUs'

        if self.current_cluster_name:
            cluster_desc = f'On cluster {self.current_cluster_name}'
        else:
            cluster_desc = 'On the current cluster'

        error_message = f"""

{cluster_desc}, the requested instance with {instance_desc} is not available.

{self.get_current_clusters_error_message()}
{self.get_other_clusters_error_message()}
"""
        return textwrap.dedent(error_message)

    def get_current_clusters_error_message(self) -> str:
        error_message = ''
        cpai = self.current_cluster_available_instances
        if cpai:
            error_message = f"""\
The instance types available for this cluster are:
{self.get_instances_description(cpai)}
"""
        return error_message

    def get_other_clusters_error_message(self) -> str:
        error_message = ''
        ait = self.attempted_instance_type
        if self.all_cluster_available_instances:
            matching_clusters: List[Tuple[str, List[int]]] = []
            for cluster_name, instance_data in self.all_cluster_available_instances.items():
                if ait.gpu_type in instance_data:
                    matching_clusters.append((cluster_name, instance_data[ait.gpu_type]))

            if matching_clusters:
                found_clusters_str = ', '.join([pt_name for pt_name, _ in matching_clusters])
                error_message += f'Did you mean a different cluster? ({found_clusters_str})\n'
                for pt_name, instance_nums_available in matching_clusters:
                    if ait.gpu_type != GPUType.NONE:
                        gpu_selector_str = f'{ait.gpu_num}x {ait.gpu_type}(s)'
                    else:
                        gpu_selector_str = 'cpu jobs'
                    if ait.gpu_num in instance_nums_available:
                        error_message += f'On: {pt_name}, {gpu_selector_str} can be run'
                    else:

                        quantities_str = ', '.join(f'{ii}x' for ii in sorted(instance_nums_available))
                        error_message += f'On: {pt_name}, only {quantities_str} {ait.gpu_type}(s) can be run'
                    error_message += '\n'
        return error_message


GPUConfig = Dict[GPUType, List[int]]  # Mapping of GPUTypes to a list of gpu counts


class InstanceRequest(NamedTuple):
    """Partially filled-in user's instance request
    """
    cluster: Optional[str]
    gpu_type: Optional[str]
    gpu_num: Optional[int]

    def __str__(self) -> str:
        messages = [
            f'Cluster: {self.cluster or "-"}',
            f'GPU Type: {self.gpu_type or "-"}',
            f'Count: {self.gpu_num if self.gpu_num is not None else "-"}',
        ]
        return ', '.join(messages)


class ValidInstance(NamedTuple):
    """A fully-entered valid instance request
    """
    cluster: str
    gpu_type: str
    gpu_num: int

    def __str__(self) -> str:
        messages = [
            f'Cluster: {self.cluster}',
            f'GPU Type: {self.gpu_type}',
            f'Count: {self.gpu_num}',
        ]
        return ', '.join(messages)

    @classmethod
    def to_registry(cls, instances: List[ValidInstance]) -> Dict[str, GPUConfig]:
        """Convert a list of valid instance requests to a registry

        Args:
            instances: List of valid instance requests

        Returns:
            A registry that maps clusters to gpu types and gpu counts
        """
        registry: Dict[str, GPUConfig] = {}
        for instance in instances:
            instance_configs = registry.setdefault(instance.cluster, {})
            instance_configs.setdefault(GPUType.from_string(instance.gpu_type), []).append(instance.gpu_num)

        return registry


class IncompleteInstanceRequest(Exception):
    """Raised if an instance request could not be completed with the specified parameters

    This can happen for two main reasons:
    1. The request specified an instance that doesn't exist in the user's clusters
    2. The request under-specified which instance to use and multiple could satisfy the constraints

    In either case, an error is raised with a message alerting the user to the possible instance requests they can make
    """
    requested: InstanceRequest
    options: Dict[str, GPUConfig]
    registry: Dict[str, GPUConfig]

    def __init__(self, requested: InstanceRequest, options: Dict[str, GPUConfig], registry: Dict[str, GPUConfig]):
        self.requested = requested
        self.options = options
        self.registry = registry
        super().__init__()

    @staticmethod
    def get_cluster_description(name: str, instances: GPUConfig):
        instances_desc = set_indent(InstanceTypeUnavailable.get_instances_description(instances), 4)
        cluster_desc = f'{name}:\n{instances_desc}'
        return cluster_desc

    def __str__(self) -> str:

        if not self.registry:
            # User doesn't have any instances
            return 'No instances available. Please run `mcli create cluster` to create your first cluster.'

        requested_message = set_indent(
            f"""
        Requested an instance with parameters:
        cluster: {self.requested.cluster or '-'}
        gpu_type: {self.requested.gpu_type or '-'}
        gpu_num:  {self.requested.gpu_num if self.requested.gpu_num is not None else '-'}
        """, 0).lstrip()

        available_message: str
        if self.options:
            # Couldn't narrow down fully, so say that
            cluster_descs = [self.get_cluster_description(name, instances) for name, instances in self.options.items()]
            full_cluster_message = '\n'.join(cluster_descs)
            available_message = f'The following instances match your requested values:\n\n{full_cluster_message}'
        else:
            # No matching values, so give all options
            cluster_descs = [self.get_cluster_description(name, instances) for name, instances in self.registry.items()]
            full_cluster_message = '\n'.join(cluster_descs)
            available_message = ('No instances match your requested values. '
                                 f'Available instances are:\n\n{full_cluster_message}')
        available_message = set_indent(available_message, 0).lstrip()

        error_message = ('Could not select an instance with the parameters provided.\n\n'
                         f'{requested_message}\n\n'
                         f'{available_message}')
        return set_indent(error_message, 0)


class UserInstanceRegistry():
    """Registry of instances that the user has access to

    Args: clusters (List[Cluster]): A list of clusters to search. If not provided, all of the user's clusters
    will be checked

    Attributes:
        registry (Dict[str, GPUConfig]): A registry that maps cluster names to GPU types and GPU counts
    """
    registry: Dict[str, GPUConfig]

    def __init__(self, clusters: Optional[List[Cluster]] = None, allow_mcloud: bool = True):
        self.registry = self.build_registry(clusters=clusters, allow_mcloud=allow_mcloud)

    @staticmethod
    def _get_cluster_instances(cluster_details: ClusterDetails) -> GPUConfig:
        return {inst.gpu_type: inst.gpu_nums for inst in cluster_details.cluster_instances}

    def build_registry(self,
                       clusters: Optional[List[Cluster]] = None,
                       allow_mcloud: bool = True) -> Dict[str, GPUConfig]:
        """Build the user's instance registry

        Args:
            clusters: An optional list of clusters to look for instances. If not provided, all of the user's
                clusters will be checked.

        Returns:
            A registry that maps cluster names to GPU types and GPU counts
        """
        # pylint: disable=import-outside-toplevel
        from mcli.api.cluster import get_clusters
        from mcli.config import FeatureFlag, MCLIConfig

        conf = MCLIConfig.load_config(safe=True)
        cluster_details: List[ClusterDetails]
        if conf.feature_enabled(FeatureFlag.USE_MCLOUD) and allow_mcloud:
            try:
                cluster_details = get_clusters()
            # Don't error out for the user if this fails, this can be called before mcli is initialized
            except MCLIConfigError:
                # API Key hasn't been set yet
                cluster_details = []
            except MAPIException:
                # API Key isn't valid
                cluster_details = []
        else:
            clusters = clusters or conf.clusters
            cluster_details = [cl.to_cluster_details() for cl in clusters]

        registry = {cd.name: self._get_cluster_instances(cd) for cd in cluster_details}
        return registry

    def lookup(
        self,
        request: InstanceRequest,
    ) -> List[ValidInstance]:
        """Look up all instances that match the user's request

        Args:
            request: A (possibly incomplete) user instance request. This will be checked against the registry to
                determine if the request can be fulfilled.

        Returns:
            A list of valid instance requests
        """

        options: List[ValidInstance] = []
        for found_cluster, instances in self.registry.items():
            if request.cluster and request.cluster != found_cluster:
                # Not the right cluster
                continue

            gpu_type = GPUType.from_string(request.gpu_type) if request.gpu_type else None
            if gpu_type and gpu_type not in instances:
                # Incorrect gpu types
                continue

            # Get possibilities with a valid gpu type
            poss_types = [gpu_type] if gpu_type else list(instances)
            for gt in poss_types:
                found_nums = instances[gt]
                # Get only those with a valid gpu num
                valid_nums: List[int] = []
                if request.gpu_num is not None:
                    valid_nums = [request.gpu_num] if request.gpu_num in found_nums else []
                else:
                    valid_nums = found_nums
                options.extend([ValidInstance(found_cluster, str(gt), n) for n in valid_nums])

        return options


class InstanceTypeLookupData(NamedTuple):
    """ Used for looking up instances """
    gpu_type: GPUType
    gpu_num: int
    cpus: Optional[float] = None

    @property
    def _key(self) -> Tuple[GPUType, int, Optional[float]]:
        return (self.gpu_type, self.gpu_num, self.cpus if self.gpu_type == GPUType.NONE else None)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self._key == other._key
        else:
            return False

    def __hash__(self) -> int:
        return hash(self._key)


class ClusterInstances:
    """ How a cluster defines what instances are available to itself """
    instance_type_map: Dict[InstanceTypeLookupData, InstanceType]

    def __init__(
        self,
        instance_types: Optional[List[InstanceType]] = None,
    ) -> None:
        self.instance_type_map = {}
        instance_types = instance_types or []
        for it in instance_types:
            if it.gpu_type == GPUType.NONE:
                key = InstanceTypeLookupData(GPUType.NONE, 0, it.limit_cpus or None)
            else:
                key = InstanceTypeLookupData(it.gpu_type, it.gpu_num)

            self.instance_type_map[key] = it

    @property
    def available_instances(self) -> Dict[GPUType, List[int]]:
        """Used to define what combinations of GPUTypes and numbers of each GPU are available
        """
        available: Dict[GPUType, List[int]] = {}
        for it_data in self.instance_type_map:
            if it_data.gpu_type not in available:
                available[it_data.gpu_type] = []
            if it_data.gpu_num not in available[it_data.gpu_type]:
                available[it_data.gpu_type].append(it_data.gpu_num)
        return available

    @property
    def cpu_instances(self) -> List[InstanceType]:
        """The CPU-only instances defined on the cluster, sorted by CPU cores
        """
        instances = [it for it in self.instance_type_map.values() if it.gpu_type == GPUType.NONE]

        # Sort instances by 'limit_cpus' in ascending order. If limit_cpus is None, put them at the end
        return sorted(instances, key=lambda it: (it.limit_cpus is None, it.limit_cpus))

    def round_up_cpu_request(self, cpus: float) -> Optional[InstanceType]:
        """Find the next largest CPU instance for the requested CPU count

        Args:
            cpus: Minimum CPU cores requested

        Returns:
            Optional[InstanceType]: If a larger CPU instance exists, returns it, otherwise returns None
        """

        for it in self.cpu_instances:
            if it.limit_cpus >= cpus:
                return it

    def get_instance_type(
        self,
        gpu_type: GPUType,
        gpu_num: int,
        cpus: Optional[float] = None,
    ) -> InstanceType:
        """Converts GPUType, GPUNum into an InstanceType given a Clusters
        Availability

        Args:
            gpu_type: The Type of GPU Requested
            gpu_num: The Number of GPUs Requested
            cpus: Optional cpus requested iff GPUType is None

        Returns:
            InstanceType of the requeted Instance

        Throws:
            InstanceTypeUnavailable: if no instance with the specified specs could be found
        """
        if gpu_type == GPUType.NONE:
            if gpu_num:
                logger.warning(f'Ignoring gpu request of {gpu_num} since the GPU type is "none"')
            gpu_num = 0
        else:
            if cpus:
                logger.warning(f'Ignoring cpu request of {cpus} since the value is overridden by the GPU instance type')
            cpus = None

        attempted_it = InstanceTypeLookupData(gpu_type, gpu_num, cpus)
        no_cpu_it = InstanceTypeLookupData(gpu_type, gpu_num, None)
        if attempted_it in self.instance_type_map:
            return self.instance_type_map[attempted_it]
        elif no_cpu_it in self.instance_type_map:
            # Check if ignoring CPU request finds a valid instance
            instance = self.instance_type_map[no_cpu_it]
            if cpus and gpu_type == GPUType.NONE:
                # Some clusters allow arbitrary CPU values, so update the CPU request if necessary
                instance.resource_requirements.cpus = cpus
            return instance
        elif gpu_type == GPUType.NONE:
            # If CPU instance requested, choose next largest, rather than erroring
            instance = self.round_up_cpu_request(cpus or 0)
            if instance:
                return instance

        raise InstanceTypeUnavailable(
            attempted_instance_type=attempted_it,
            current_cluster_available_instances=self.available_instances,
        )

    def validate_all_instance_combinations(self) -> bool:
        """Helper for validating that all InstanceTypes produce selectors
        """
        passed = True
        for gpu_type, gpu_nums in self.available_instances.items():
            for gpu_num in gpu_nums:
                # pylint: disable-next=assignment-from-no-return
                instance_type = self.get_instance_type(gpu_type, gpu_num)
                selectors = instance_type.selectors
                if not selectors:
                    print(f'No selectors found for gpu: {gpu_type}, num: {gpu_num}')
                    passed = False
        return passed


class ClusterInstanceGPUConfiguration(NamedTuple):
    """ A Helper Container to ensure that all possible options for an
    internal GPU cluster are configured
    """
    gpu_type: GPUType
    gpu_nums: List[int]
    gpu_selectors: Optional[Dict[str, str]] = None
    cpus: Optional[float] = None
    cpus_per_gpu: Optional[float] = None
    memory: Optional[int] = None
    memory_per_gpu: Optional[int] = None
    storage: Optional[int] = None
    storage_per_gpu: Optional[int] = None
    multinode_rdma_roce: Optional[int] = None
    gpus_per_node: int = 8


class LocalClusterInstances(ClusterInstances):
    """ A Local Cluster implementation to parameterize different instance types and resources """

    # Maximum machine CPU size for the Cluster (CPU Jobs only)
    MIN_CPU: int = 1
    MAX_CPU: int = 128

    def __init__(
        self,
        instance_types: Optional[List[InstanceType]] = None,
        gpu_configurations: Optional[List[ClusterInstanceGPUConfiguration]] = None,
    ) -> None:
        super().__init__(instance_types=instance_types)

        gpu_configurations = gpu_configurations or []
        for gpu_config in gpu_configurations:
            self.add_cluster_instance_gpu_configuration(gpu_config)

    def add_cluster_instance_gpu_configuration(
        self,
        gpu_configuration: ClusterInstanceGPUConfiguration,
    ):
        """Adds a batch of settings for a single GPU Type

        Args:
            gpu_configuration: The GPU Configuration Batch
        """
        gpu_type = gpu_configuration.gpu_type
        for ngpu in gpu_configuration.gpu_nums:
            rr = MCLIK8sResourceRequirements()

            if ngpu > 0:
                rr.gpus = min(ngpu, gpu_configuration.gpus_per_node)

            if gpu_configuration.gpu_type == GPUType.NONE:
                # If min CPU amount has been set, keep that required amount
                min_cpus = self.MIN_CPU
                if rr.cpus != 0:
                    min_cpus = rr.cpus
                rr.cpus = self.MAX_CPU - SAFETY_MARGIN_CPU
                rr.request_cpus = min_cpus

            # Set CPU cores
            if gpu_configuration.cpus:
                rr.cpus = max(gpu_configuration.cpus - SAFETY_MARGIN_CPU, self.MIN_CPU)
            if gpu_configuration.cpus_per_gpu:
                rr.request_cpus = max(gpu_configuration.cpus_per_gpu * rr.gpus - SAFETY_MARGIN_CPU, self.MIN_CPU)

            # Set memory allotted
            if gpu_configuration.memory_per_gpu:
                rr.memory = int(gpu_configuration.memory_per_gpu * rr.gpus * (1 - SAFETY_MARGIN_MEMORY))
            elif gpu_configuration.memory:
                rr.memory = int(gpu_configuration.memory * (1 - SAFETY_MARGIN_MEMORY))

            # Set ephemeral storage
            if gpu_configuration.storage_per_gpu:
                rr.ephemeral_storage = int(gpu_configuration.storage_per_gpu * rr.gpus * (1 - SAFETY_MARGIN_STORAGE))
            elif gpu_configuration.storage:
                rr.ephemeral_storage = int(gpu_configuration.storage * (1 - SAFETY_MARGIN_STORAGE))

            # Multinode Overrides
            if (ngpu > 0) and (ngpu > gpu_configuration.gpus_per_node) and (gpu_configuration.multinode_rdma_roce
                                                                            is not None):
                rr.rdma_roce = gpu_configuration.multinode_rdma_roce

            key = InstanceTypeLookupData(gpu_type, ngpu, gpu_configuration.cpus)
            instance_type = InstanceType(gpu_type,
                                         ngpu,
                                         resource_requirements=rr,
                                         selectors=gpu_configuration.gpu_selectors or {})
            self.instance_type_map[key] = instance_type


def create_cpu_instances(
    max_cpu: int,
    max_memory: int,
    max_storage: int,
    instance_cpus: List[int],
    selectors: Optional[Dict[str, str]] = None,
) -> List[InstanceType]:
    """Create a list of CPU instances that scale memory and storage

    Args:
        max_cpu: Maximum CPU count for the instance
        max_memory: Maximum memory for the instance
        max_storage: Maximum storage for the instance
        instance_cpus: List of CPU core counts for individual instances
        selectors: Node selectors to add to each instance

    Returns:
        List[InstanceType]: A list of CPU instances
    """
    instances: List[InstanceType] = []
    for icpu in instance_cpus:
        memory = int(max_memory * float(icpu / max_cpu))
        storage = int(max_storage * float(icpu / max_cpu))
        rr = MCLIK8sResourceRequirements.from_simple_resources(cpus=icpu,
                                                               memory=memory,
                                                               storage=storage,
                                                               include_margin=True)
        instance = InstanceType(gpu_type=GPUType.NONE, gpu_num=0, resource_requirements=rr, selectors=selectors or {})
        instances.append(instance)

    return instances
