"""Global Singleton Config Store"""
from __future__ import annotations

import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Set

import ruamel.yaml
import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from mcli.api.exceptions import MCLIConfigError
from mcli.models import Cluster, MCLIEnvVar
from mcli.utils.utils_modules import check_if_module_exists
from mcli.utils.utils_serializable_dataclass import SerializableDataclass
from mcli.utils.utils_yaml import StringDumpYAML

logger = logging.getLogger(__name__)


def env_path_override_config(config_value: str):
    if config_value in os.environ:
        globals()[config_value] = Path(os.environ[config_value])


def env_str_override_config(config_value: str):
    if config_value in os.environ:
        globals()[config_value] = os.environ[config_value]


MCLI_CONFIG_DIR: Path = Path(os.path.expanduser('~/.mosaic'))
env_path_override_config('MCLI_CONFIG_DIR')

MCLI_BACKUP_CONFIG_DIR: Path = Path(os.path.expanduser('~/.mosaic.bak'))
env_path_override_config('MCLI_BACKUP_CONFIG_DIR')

MOSAICML_API_ENDPOINT: str = 'https://api.mosaicml.com/graphql'
MOSAICML_API_ENDPOINT_STAGING: str = 'https://staging.api.mosaicml.com/graphql'
MOSAICML_API_ENDPOINT_DEV: str = 'https://dev.api.mosaicml.com/graphql'
MOSAICML_API_ENDPOINT_LOCAL: str = 'http://localhost:3001/graphql'
MOSAICML_API_ENDPOINT_ENV: str = 'MOSAICML_API_ENDPOINT'
env_str_override_config(MOSAICML_API_ENDPOINT_ENV)

MCLI_CONFIG_PATH: Path = MCLI_CONFIG_DIR / 'mcli_config'
env_path_override_config('MCLI_CONFIG_PATH')

MCLI_KUBECONFIG: Path = MCLI_CONFIG_DIR / 'kube_config'
env_path_override_config('MCLI_KUBECONFIG')

COMPOSER_INSTALLED: bool = check_if_module_exists('composer')

UPDATE_CHECK_FREQUENCY_DAYS: float = 2

PAGER_LIMIT: int = 50  # When `mcli get` returns more than PAGER_LIMIT entries, a pager should be used

JOB_TTL: int = int(timedelta(days=14).total_seconds())
MCLI_MODE_ENV: str = 'MCLI_MODE'
env_str_override_config(MCLI_MODE_ENV)

MCLI_INTERACTIVE_ENV: str = 'MCLI_INTERACTIVE'
env_str_override_config(MCLI_INTERACTIVE_ENV)

# Used for local dev and testing
MOSAICML_API_KEY_ENV: str = 'MOSAICML_API_KEY'

SUPPORT_TOKEN_KEY_ENV: str = 'MOSAICML_SUPPORT_TOKEN_KEY'

MCLOUD_OBSCURE_FALLBACK: str = 'PLEASE_NO_MCLOUD_THANKS'

logging.getLogger('urllib3.connectionpool').disabled = True

logger = logging.getLogger(__name__)


class FeatureFlag(Enum):
    """Enum for mcli feature flags
    """
    ALPHA_TESTER = 'ALPHA_TESTER'
    MLPERF_MODE = 'MLPERF_MODE'
    USE_DEMO_NODES = 'USE_DEMO_NODES'
    USE_MCLOUD = 'USE_MCLOUD'

    def validate_compatibility(self) -> None:
        conf = MCLIConfig.load_config(safe=True)
        if self == FeatureFlag.USE_DEMO_NODES and conf.feature_enabled(FeatureFlag.USE_MCLOUD):
            raise MCLIConfigError(Messages.INVALID_FEATURES_DEMO_NODES_AND_MCLOUD)
        if self == FeatureFlag.USE_MCLOUD and conf.feature_enabled(FeatureFlag.USE_DEMO_NODES):
            raise MCLIConfigError(Messages.INVALID_FEATURES_MCLOUD_AND_DEMO_NODES)

    @staticmethod
    def get_external_features() -> Set[FeatureFlag]:
        return {FeatureFlag.USE_MCLOUD}


class MCLIMode(Enum):
    """Enum for mcli user modes
    """
    PROD = 'PROD'
    DEV = 'DEV'
    INTERNAL = 'INTERNAL'
    LOCAL = 'LOCAL'
    LEGACY = 'LEGACY'
    STAGING = 'STAGING'

    def is_internal(self) -> bool:
        """True if this mode is an internal mode
        """
        internal_modes = {MCLIMode.DEV, MCLIMode.INTERNAL, MCLIMode.LOCAL, MCLIMode.STAGING}
        return self in internal_modes

    def is_mcloud_enabled(self) -> bool:
        """True if this mode is enabled use with mcloud
        """
        mcloud_disabled = {
            MCLIMode.LEGACY,
        }
        return self not in mcloud_disabled

    def available_feature_flags(self) -> List[FeatureFlag]:
        if self.is_internal():
            # All features are available to internal users
            return list(FeatureFlag)

        return list(FeatureFlag.get_external_features())

    @classmethod
    def from_env(cls) -> MCLIMode:
        """If the user's mcli mode is set in the environment, return it
        """
        found_mode = os.environ.get(MCLI_MODE_ENV, None)
        if found_mode:
            for mode in MCLIMode:
                if found_mode == mode.value:
                    return mode

        if os.environ.get('DOGEMODE', None) == 'ON':
            return MCLIMode.INTERNAL

        return MCLIMode.PROD

    @property
    def endpoint(self) -> str:
        """The endpoint value for the given environment
        """
        if self is MCLIMode.DEV:
            return MOSAICML_API_ENDPOINT_DEV
        elif self is MCLIMode.LOCAL:
            return MOSAICML_API_ENDPOINT_LOCAL
        elif self is MCLIMode.STAGING:
            return MOSAICML_API_ENDPOINT_STAGING
        return MOSAICML_API_ENDPOINT

    def is_alternate(self) -> bool:
        """True if the mode is a valid alternate mcloud environment
        """
        alternate_env_modes = {MCLIMode.DEV, MCLIMode.LOCAL, MCLIMode.STAGING}
        return self in alternate_env_modes


def update_user_config():
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        # MCLI hasn't been initialized yet. Don't edit it until then
        return

    # Force upgrade internal users to use MCLOUD (only if they haven't set it before)
    if conf.internal and FeatureFlag.USE_MCLOUD.value not in conf.feature_flags:
        msg = """
As an internal user, you have been selected to use the ✨new✨ MosaicML Cloud.
Minimal setup is required to get an API Key and start submitting jobs:
[blue]https://internal.mcli.docs.mosaicml.com/internal/using_the_cloud.html[/]

If you run into any issues or have questions and feedback, please reach out to
[green]#e-hektar-helpdesk[/] and file an issue in JIRA:
[blue]https://mosaicml.atlassian.net/jira/software/c/projects/HEK/boards/7/backlog[/]

To unblock yourself or if running external demos, you can temporarily revert back:
[bold]mcli unset feature USE_MCLOUD[/]

After the issue is resolved, you can switch the flag back on:
[bold]mcli set feature USE_MCLOUD[/]
"""

        logger.info(msg)
        conf.feature_flags[FeatureFlag.USE_MCLOUD.value] = True
        conf.save_config()


@dataclass
class MCLIConfig(SerializableDataclass):
    """Global Config Store persisted on local disk"""

    # set to default for now to not break existing users' configs
    MOSAICML_API_KEY: str = ''  # pylint: disable=invalid-name Global Stored within Singleton

    feature_flags: Dict[str, bool] = field(default_factory=dict)
    last_update_check: datetime = field(default_factory=datetime.now)

    # Global Environment Variables
    environment_variables: List[MCLIEnvVar] = field(default_factory=list)

    # Registered Clusters
    clusters: List[Cluster] = field(default_factory=list)

    # MCloud environments w/ API keys
    # Most users will be in PROD, so this will likely only be touched internally
    mcloud_envs: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def empty(cls) -> MCLIConfig:
        conf = MCLIConfig()
        return conf

    @property
    def dev_mode(self) -> bool:
        return self.mcli_mode == MCLIMode.DEV

    @property
    def internal(self) -> bool:
        return self.mcli_mode.is_internal()

    @property
    def mcli_mode(self) -> MCLIMode:
        return MCLIMode.from_env()

    @property
    def allow_interactive(self) -> bool:
        interactive_env = os.environ.get(MCLI_INTERACTIVE_ENV, 'false').lower()
        return interactive_env == 'true' or self.internal

    @property
    def endpoint(self) -> str:
        """The user's MCloud endpoint
        """
        env_endpoint = os.environ.get(MOSAICML_API_ENDPOINT_ENV, None)

        return env_endpoint or self.mcli_mode.endpoint

    @property
    def api_key(self):
        """The user's configured MCloud API key
        """
        return self.get_api_key(env_override=True)

    @api_key.setter
    def api_key(self, value: str):
        if self.mcli_mode.is_alternate():
            # If the user is using an alternative mcloud, set that API key
            self.mcloud_envs[self.mcli_mode.value] = value
        else:
            self.MOSAICML_API_KEY = value

    def get_api_key(self, env_override: bool = True):
        """Get the user's current API key

        Args:
            env_override (bool, optional): If True, allow an environment variable to
                override the configured value, otherwise pull only from the user's config
                file. Defaults to True.

        Returns:
            str: The user's API key, if set, otherwise an empty string
        """
        api_key_env = os.environ.get(MOSAICML_API_KEY_ENV, None)
        if api_key_env is not None and env_override:
            return api_key_env
        elif self.mcli_mode.is_alternate():
            return self.mcloud_envs.get(self.mcli_mode.value, '')
        elif self.MOSAICML_API_KEY:
            return self.MOSAICML_API_KEY
        return ''

    @staticmethod
    def _remove_deprecated_cluster_details(clusters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        # pylint: disable-next=import-outside-toplevel
        from mcli.serverside.clusters.cluster import GenericK8sCluster

        valid_clusters: List[Dict[str, str]] = []
        for cluster in clusters:
            if cluster.get('kubernetes_context', '').endswith('research-01'):
                continue
            if 'kubernetes_context' in cluster and cluster[
                    'kubernetes_context'] not in GenericK8sCluster.get_k8s_context_map():
                continue
            if 'environment_overrides' in cluster:
                del cluster['environment_overrides']
            valid_clusters.append(cluster)
        return valid_clusters

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MCLIConfig:
        # TODO: Remove after full deprecation transition
        if 'dev_mode' in data:
            del data['dev_mode']
        if 'internal' in data:
            del data['internal']
        # TODO(END): Remove after full deprecation transition

        # Backwards compatibility: platforms should be synonymous with clusters
        if 'platforms' in data:
            data['clusters'] = data['platforms']
            del data['platforms']
        data['clusters'] = cls._remove_deprecated_cluster_details(data.get('clusters', []))

        return super().from_dict(data)

    @classmethod
    def load_config(cls, safe: bool = False) -> MCLIConfig:
        """Loads the MCLIConfig from local disk


        Args:
            safe (bool): If safe is true, if the config fails to load it will return
                an empty generated config

        Return:
            Returns the MCLIConfig if successful, otherwise raises MCLIConfigError
        """
        try:
            with open(MCLI_CONFIG_PATH, 'r', encoding='utf8') as f:
                data: Dict[str, Any] = yaml.full_load(f)
            conf: MCLIConfig = cls.from_dict(data)
        except FileNotFoundError as e:
            if safe:
                return MCLIConfig.empty()
            raise MCLIConfigError(Messages.MCLI_NOT_INITIALIZED) from e

        # Optional values can get filled in over time. If a new optional value is not
        # present in the config, let it be filled in by the default, if one was set.
        if set(asdict(conf)) != set(data):
            # TODO: Bug on over-saving HEK-452
            conf.save_config()  # pylint: disable=no-member

        return conf

    def save_config(self) -> bool:
        """Saves the MCLIConfig to local disk

        Return:
            Returns true if successful
        """
        if self.dev_mode:
            print('saving config...')

        data = self._get_formatted_dump()
        y = YAML()
        y.explicit_start = True  # type: ignore
        with open(MCLI_CONFIG_PATH, 'w', encoding='utf8') as f:
            y.dump(data, f)
        return True

    def _get_formatted_dump(self) -> CommentedMap:
        """Gets the ruamel yaml formatted dump of the config
        """
        raw_data = self.to_disk()

        # Moves clusters to last item
        clusters = raw_data['clusters']
        del raw_data['clusters']
        raw_data['clusters'] = clusters

        # Remove invalid clusters

        data: CommentedMap = ruamel.yaml.load(
            yaml.dump(raw_data),
            ruamel.yaml.RoundTripLoader,
        )
        data.yaml_set_start_comment('MCLI Config Data\n')
        data.yaml_set_comment_before_after_key(
            key='environment_variables',
            before='\nAll Global Environment variables go here',
        )
        data.yaml_set_comment_before_after_key(
            key='clusters',
            before='\nAll Clusters configured for MCLI',
        )
        return data

    @property
    def mcloud_enabled(self) -> bool:
        if os.environ.get(MCLOUD_OBSCURE_FALLBACK, "FALSE").upper() == "TRUE":
            # Disabled if the obscure fallback env var is on
            return False

        if not self.mcli_mode.is_mcloud_enabled():
            # Disabled if MCloud is disabled for the mode
            return False

        if self.internal:
            # All internal users should otherwise be enabled
            return True

        if self.mcli_mode == MCLIMode.PROD:
            # Prod users check feature flag
            return self.feature_flags.get(FeatureFlag.USE_MCLOUD.value, False)

        return False

    def feature_enabled(self, feature: FeatureFlag) -> bool:
        """Checks if the feature flag is enabled

        Args:
            feature (FeatureFlag): The feature to check
        """
        if feature is FeatureFlag.USE_MCLOUD:
            # Handle complicated mcloud enabling logic elsewhere
            return self.mcloud_enabled

        if not self.internal and feature not in FeatureFlag.get_external_features():
            # Only enable select features for external use
            return False

        if feature.value in self.feature_flags:
            enabled = self.feature_flags.get(feature.value, False)
            return bool(enabled)

        return False

    def __str__(self) -> str:
        data = self._get_formatted_dump()
        y = StringDumpYAML()
        return y.dump(data)


def feature_enabled(feature: FeatureFlag) -> bool:
    conf = MCLIConfig.load_config(safe=True)
    return conf.feature_enabled(feature=feature)


class Messages():
    MCLI_NOT_INITIALIZED = 'MCLI not yet initialized. Please run `mcli init` first.'
    API_KEY_MISSING = 'No API key found. Please create one and set it using `mcli set api-key`.'

    INVALID_FEATURES_DEMO_NODES_AND_MCLOUD = (
        f'{FeatureFlag.USE_DEMO_NODES.value} feature cannot be set when the {FeatureFlag.USE_MCLOUD.value}'
        f' feature is already activated. Run `mcli unset feature {FeatureFlag.USE_MCLOUD.value}` before trying to'
        ' use demo nodes feature')
    INVALID_FEATURES_MCLOUD_AND_DEMO_NODES = (
        f'{FeatureFlag.USE_MCLOUD.value} feature cannot be set when the {FeatureFlag.USE_DEMO_NODES.value}'
        f' feature is already activated. Run `mcli unset feature {FeatureFlag.USE_DEMO_NODES.value}`'
        ' before trying to use MCLOUD')


MESSAGE = Messages()
