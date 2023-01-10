"""Implementation of secrets for a Kubernetes backend"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union

from kubernetes import client

from mcli.models import Cluster, Secret
from mcli.objects.secrets import SECRET_CLASS_MAP, SecretType
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.utils import utils_kube
from mcli.utils.utils_kube_labels import label

logger = logging.getLogger(__name__)


class ClusterSecretError(Exception):
    """Error in handling cluster secrets"""


@dataclass
class ClusterSecret:
    """Cluster-dependent secret backed by Kubernetes
    Attributes:
        secret: The secret whose data was imported from Kubernetes
    """

    secret: Secret

    def create(self, namespace: str) -> bool:
        """Create the secret in the current cluster
        Args:
            namespace: Namespace in which the secret should be created
        Returns:
            True if secret was created successfully
        """
        return utils_kube.create_secret(self.to_kube_spec(), namespace)

    def delete(self, namespace: str):
        """Delete the secret from the current cluster
        Args:
            namespace: Namespace in which the secret exists
        Returns:
            True if secret was deleted successfully
        """
        return utils_kube.delete_secret(self.secret.name, namespace)

    def to_kube_spec(self) -> Dict[str, Any]:
        """Convert the secret to a Kubernetes spec
        Returns:
            Kubernetes spec dictionary
        """
        labels = self.secret.kubernetes_labels or {}
        annotations = self.secret.kubernetes_annotations or {}

        secret = client.V1Secret(type=self.secret.kubernetes_type, data=self.secret.pack())
        secret.metadata = client.V1ObjectMeta(name=self.secret.name, labels=labels, annotations=annotations)
        return client.ApiClient().sanitize_for_serialization(secret)

    @classmethod
    def from_kube_spec(cls: Type[ClusterSecret], spec: Dict[str, Any]) -> ClusterSecret:
        """Import a secret from a Kubernetes spec
        Args:
            spec: Kubernetes spec for an MCLI generated secret
        Raises:
            ClusterSecretError: Raised if the provided secret is not a valid MCLI secret
        Returns:
            A ClusterSecret
        """
        name = spec['metadata']['name']
        logger.debug(f'Attempting to create secret from Kubernetes secret {name}')

        # Get the secret type label
        labels = spec['metadata'].get('labels', {})
        if label.mosaic.SECRET_TYPE not in labels:
            raise ClusterSecretError(f'Secret named {name} is not a valid MCLI secret.')

        secret_type_string = labels[label.mosaic.SECRET_TYPE].replace('-', '_')
        try:
            secret_type = SecretType.ensure_enum(secret_type_string)
        except ValueError as e:
            raise ClusterSecretError(
                f'Secret named {name} has an unknown type: {labels[label.mosaic.SECRET_TYPE]}') from e
        logger.debug(f'Secret {name} is of type: {secret_type.value}')

        try:
            created_at = datetime.fromisoformat(spec['metadata'].get('creationTimestamp', ''))
        except ValueError:
            created_at = None

        secret_class = SECRET_CLASS_MAP[secret_type]
        secret = secret_class(
            name=name,
            secret_type=secret_type,
            created_at=created_at,
        )
        secret.unpack(spec['data'])

        return ClusterSecret(secret=secret)


class SecretManager:
    """Secrets manager for Kubernetes-backed secrets
    Arguments:
        cluster: The cluster where secrets are stored
    """

    def __init__(self, mcli_cluster: Cluster):
        self.cluster = mcli_cluster

    def get_secrets(self) -> List[ClusterSecret]:
        """Get a list of secrets on the cluster
        Returns:
            List of secrets
        """
        labels: Dict[str, Optional[Union[str, List[str]]]] = {label.mosaic.SECRET_TYPE: None}
        with Cluster.use(self.cluster):
            secrets = utils_kube.list_secrets(self.cluster.namespace, labels=labels)
            logger.debug(f'Found {len(secrets["items"])} secrets in cluster {self.cluster.name}')
        return [ClusterSecret.from_kube_spec(spec) for spec in secrets['items']]

    def add_secrets_to_job(self, kubernetes_job: MCLIK8sJob) -> None:
        """Add all of the cluster's secrets to the provided job
        Args:
            job_spec: MCLIK8sJob spec that should be modified by each managed secret
        """
        cluster_secrets = self.get_secrets()
        for cluster_secret in cluster_secrets:
            logger.debug(f'Adding secret {cluster_secret.secret.name} from {self.cluster.name} to job')
            cluster_secret.secret.add_to_job(kubernetes_job)
