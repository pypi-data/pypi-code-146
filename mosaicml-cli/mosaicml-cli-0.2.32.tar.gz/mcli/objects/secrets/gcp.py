""" GCP Credentials Secret Type """
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from kubernetes import client

from mcli.objects.secrets.mounted import MCLIMountedSecret
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLIGCPSecret(MCLIMountedSecret):
    """Secret class for GCP credentials
    """

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'gcpSecret': {
                'name': self.name,
                'metadata': {
                    'mountPath': self.mount_path
                },
                'value': self.value,
            }
        }

    def add_to_job(self, kubernetes_job: MCLIK8sJob, permissions: int = 256) -> bool:
        super().add_to_job(kubernetes_job, permissions)
        assert self.mount_path is not None

        # Add credential env vars
        credentials_var = client.V1EnvVar(
            name='GOOGLE_APPLICATION_CREDENTIALS',
            value=f'{Path(self.mount_path) / "secret"}',
        )
        kubernetes_job.add_env_var(credentials_var)
        return True
