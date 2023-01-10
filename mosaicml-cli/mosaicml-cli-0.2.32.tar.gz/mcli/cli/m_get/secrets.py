"""CLI getter for secrets"""
import logging
from dataclasses import dataclass
from http import HTTPStatus
from typing import Generator, List, Union

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.secrets.api_get_secrets import get_secrets as api_get_secrets
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.models import Secret, SecretType
from mcli.objects.secrets.cluster_secret import SecretManager
from mcli.utils.utils_date import get_human_readable_date
from mcli.utils.utils_logging import FAIL, WARN, console

logger = logging.getLogger(__name__)


@dataclass
class SecretDisplayItem(MCLIDisplayItem):
    name: str
    type: SecretType
    created_at: str


class SecretDisplay(MCLIGetDisplay):
    """`mcli get secrets` display class
    """

    def __init__(self, secrets: List[Secret]):
        self.secrets = secrets

    def __iter__(self) -> Generator[SecretDisplayItem, None, None]:
        for secret in self.secrets:
            yield SecretDisplayItem(
                name=secret.name,
                type=secret.secret_type,
                created_at=get_human_readable_date(secret.created_at) if secret.created_at else 'Unknown',
            )


def _get_secrets(secret_type: str = "all") -> list:
    conf: MCLIConfig = MCLIConfig.load_config()
    if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
        secret_types: Union[List[str], List[SecretType]]
        if secret_type == 'all':
            secret_types = [s for s in SecretType if s not in {SecretType.generic}]
        else:
            secret_types = [secret_type]

        try:
            mcli_secrets = api_get_secrets(secret_types=secret_types, timeout=None)
        except MAPIException as e:
            if e.status == HTTPStatus.NOT_FOUND:
                return []
            else:
                raise e
    else:
        if not conf.clusters:
            logger.warning(f'{WARN} No clusters found. Secrets require at least one cluster to be configured.')
            return []

        ref_platform = conf.clusters[0]
        manager = SecretManager(ref_platform)
        mcli_secrets = [ps.secret for ps in manager.get_secrets()]
        if secret_type != "all":
            mcli_secrets = [s for s in mcli_secrets if s.secret_type.name == secret_type]

    return mcli_secrets


def get_secrets(output: OutputDisplay = OutputDisplay.TABLE, secret_type: str = "all", **kwargs) -> int:
    """Get currently configured secrets from the reference cluster

    Args:
        output: Output display type. Defaults to OutputDisplay.TABLE.
        secret_type: Filter for secret type. Defaults to 'all' (no filter).

    Returns:
        0 if call succeeded, else 1
    """
    del kwargs

    try:

        with console.status('Retrieving requested secrets...'):
            found_secrets = _get_secrets(secret_type)
        display = SecretDisplay(found_secrets)
        display.print(output)
    except (KubernetesException, MAPIException) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    return 0
