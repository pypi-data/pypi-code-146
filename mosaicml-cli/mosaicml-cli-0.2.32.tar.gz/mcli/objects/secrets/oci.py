"""OCI Credentials Secret Type"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from kubernetes import client

from mcli.models import Secret
from mcli.models.mcli_secret import SECRET_MOUNT_PATH_PARENT
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob, MCLIVolume


@dataclass
class MCLIOCISecret(Secret):
    """
    Secret class for OCI config and pem filew.
    """
    mount_directory: Optional[str] = None
    key_file: Optional[str] = None
    config: Optional[str] = None

    def __post_init__(self):
        if self.mount_directory is None:
            self.mount_directory = str(SECRET_MOUNT_PATH_PARENT / self.name)

    @property
    def disk_skipped_fields(self) -> List[str]:
        return ['key_file', 'config']

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields + ['mount_directory'])

    @property
    def mapi_data(self) -> Dict[str, Any]:
        raise NotImplementedError("OCI secret creation is not implemented for MAPI yet.")

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        assert self.mount_directory is not None
        path = Path(self.mount_directory)
        secret_volume = client.V1Volume(
            name=self.name,
            secret=client.V1SecretVolumeSource(
                secret_name=self.name,
                items=[
                    client.V1KeyToPath(key='config', path='config'),
                    client.V1KeyToPath(key='key_file', path='key.pem'),
                ],
            ),
        )
        secret_mount = client.V1VolumeMount(
            name=self.name,
            mount_path=str(path),
            read_only=True,
        )
        mcli_volume = MCLIVolume(volume=secret_volume, volume_mount=secret_mount)
        kubernetes_job.add_volume(mcli_volume)

        # Add config file env var
        config_var = client.V1EnvVar(
            name='OCI_CONFIG_FILE',
            value=f'{self.mount_directory}/config',
        )
        kubernetes_job.add_env_var(config_var)

        # Add key file env var
        cli_key_var = client.V1EnvVar(
            name='OCI_CLI_KEY_FILE',
            value=f'{self.mount_directory}/key.pem',
        )
        kubernetes_job.add_env_var(cli_key_var)

        # Add CLI config env var (same as config file but used for CLI)
        cli_config_var = client.V1EnvVar(
            name='OCI_CLI_CONFIG_FILE',
            value=f'{self.mount_directory}/config',
        )
        kubernetes_job.add_env_var(cli_config_var)
        return True
