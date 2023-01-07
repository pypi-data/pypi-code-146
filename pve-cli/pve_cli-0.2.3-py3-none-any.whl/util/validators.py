import inspect

import typer

from .exceptions import InvalidConfigError
from ..proxmox import Proxmox


def validate_cluster(ctx: typer.Context, cluster: str) -> str:
    config = ctx.obj['config']
    clusters = config.get('clusters', {})
    if cluster not in clusters:
        raise typer.BadParameter(
            f'Config for cluster "{cluster}" could not be found in configured clusters: {", ".join(clusters)}.')

    return cluster


def validate_config(config: dict):
    cluster_config = config.get('clusters', {})
    default_cluster = config.get('defaults', {}).get('cluster', None)
    if default_cluster is not None and default_cluster not in cluster_config:
        raise InvalidConfigError(f'The configured default cluster "{default_cluster}" '
                                 f'has no configuration section in the config. (available: {", ".join(cluster_config)})')

    required_keys = [param.name for param in inspect.signature(Proxmox.__init__).parameters.values()
                     if param.default == inspect.Parameter.empty and param.name != 'self']

    invalid_cluster_config = False
    err_msg = []
    for cluster_name, cluster_config in cluster_config.items():
        missing_keys = [key for key in required_keys if key not in cluster_config]
        if missing_keys:
            err_msg.append(f'  {cluster_name}: {", ".join(missing_keys)}')
            invalid_cluster_config = True

    if invalid_cluster_config:
        raise InvalidConfigError('Missing keys in config for clusters:\n{}'.format('\n'.join(err_msg)))
