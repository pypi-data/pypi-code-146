""" MCLI Abstraction for Clusters """
from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generator, Union

from mcli.utils.utils_kube import KubeContext, use_context
from mcli.utils.utils_serializable_dataclass import SerializableDataclass

if TYPE_CHECKING:
    from mcli.api.model.cluster_details import ClusterDetails

logger = logging.getLogger(__name__)


class ClusterKubernetesError(Exception):
    """Error in cluster kubernetes conversion """


@dataclass
class Cluster(SerializableDataclass):
    """Configured MCLI cluster relating to specific kubernetes context
    """
    name: str
    kubernetes_context: str
    namespace: str

    @classmethod
    @contextmanager
    def use(cls, cluster: Union[Cluster, str]) -> Generator[Cluster, None, None]:
        """Temporarily set the cluster to use for all Kubernetes API calls

        Args:
            cluster (Cluster): The cluster to use

        Yields:
            Cluster: The provided cluster
        """
        if isinstance(cluster, str):
            mcli_cluster = cls.get_by_name(cluster)
        else:
            mcli_cluster = cluster

        with use_context(mcli_cluster.kubernetes_context):
            yield mcli_cluster

    def to_kube_context(self) -> KubeContext:
        """Get the corresponding KubeContext for this cluster

        Returns:
            KubeContext with cluster details
        """
        return KubeContext(name=self.kubernetes_context, namespace=self.namespace)

    @classmethod
    def from_kube_context(cls, context: KubeContext, cluster_name: str) -> Cluster:
        """Create an Cluster from a KubeContext object

        Args:
            context: KubeContext containing cluster details

        Returns:
            Cluster with context details
        """
        if context.namespace is None:
            raise RuntimeError('Context must have a declared namespace')

        return cls(name=cluster_name, kubernetes_context=context.name, namespace=context.namespace)

    @staticmethod
    def get_by_name(cluster_name: str) -> Cluster:
        """Get a cluster from the user's config by its name

        Args:
            cluster_name: Name of the cluster

        Raises:
            KeyError: Raised if the requested cluster does not exist

        Returns:
            The requested cluster
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.config import FeatureFlag, MCLIConfig

        conf = MCLIConfig.load_config(safe=True)
        for cluster in conf.clusters:
            if cluster.name == cluster_name:
                return cluster

        if not conf.feature_enabled(FeatureFlag.USE_MCLOUD):
            names = ', '.join(sorted([pl.name for pl in conf.clusters]))
            raise KeyError(f'Nonexistent cluster: No cluster named {cluster_name}. Valid names are: {names}')
        else:
            # TODO: Update this with a MAPI call to get available clusters for the user (HEK-1307)
            return Cluster(name=cluster_name, kubernetes_context='unused', namespace='unused')

    def to_cluster_details(self) -> ClusterDetails:
        # pylint: disable=import-outside-toplevel
        from mcli.api.model.cluster_details import ClusterDetails, ClusterInstance
        from mcli.serverside.clusters import GenericK8sCluster

        k8s_cluster = GenericK8sCluster.from_mcli_cluster(self)
        cluster_instances = k8s_cluster.allowed_instances.available_instances
        instances = ClusterInstance.from_available_instances(cluster_instances)
        return ClusterDetails(name=self.name, cluster_instances=instances)
