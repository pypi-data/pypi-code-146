import dataclasses
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import irisml.core


class Task(irisml.core.TaskBase):
    """Get a secret from Azure KeyVault."""
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        keyvault_name: str
        secret_name: str

    @dataclasses.dataclass
    class Outputs:
        secret: str = ''

    def execute(self, inputs):
        vault_url = f'https://{self.config.keyvault_name}.vault.azure.net'
        client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())

        secret = client.get_secret(self.config.secret_name)
        assert isinstance(secret.value, str), f"Unexpected secret type: {type(secret.value)}"
        return self.Outputs(secret.value)
