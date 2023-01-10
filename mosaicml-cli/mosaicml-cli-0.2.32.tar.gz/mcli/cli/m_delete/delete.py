""" Functions for deleting MCLI objects """
import fnmatch
import logging
from http import HTTPStatus
from typing import Dict, Generic, List, Optional, Tuple, TypeVar

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.api.secrets import delete_secrets as api_delete_secrets
from mcli.api.secrets import get_secrets as api_get_secrets
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.models import Cluster
from mcli.objects.secrets.cluster_secret import SecretManager
from mcli.sdk import delete_runs, get_runs
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_logging import FAIL, INFO, OK, console, get_indented_list
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_string_functions import is_glob

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
T_NOUN = TypeVar('T_NOUN')


class DeleteGroup(Generic[T_NOUN]):
    """Helper for extracting objects to delete from an existing set
    """

    def __init__(self, requested: List[str], existing: Dict[str, T_NOUN]):
        # Get unique values, with order
        self.requested = list(dict.fromkeys(requested))
        self.existing = existing

        self.chosen: Dict[str, T_NOUN] = {}
        self.missing: List[str] = []
        for pattern in self.requested:
            matching = fnmatch.filter(self.existing, pattern)
            if matching:
                self.chosen.update({k: self.existing[k] for k in matching})
            else:
                self.missing.append(pattern)

        self.remaining = {k: v for k, v in self.existing.items() if k not in self.chosen}


def delete_environment_variable(variable_names: List[str],
                                force: bool = False,
                                delete_all: bool = False,
                                **kwargs) -> int:
    del kwargs
    if not (variable_names or delete_all):
        logger.error(f'{FAIL} Must specify environment variable names or --all.')
        return 1
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if delete_all:
        variable_names = ['*']

    group = DeleteGroup(variable_names, {ev.key: ev for ev in conf.environment_variables})

    # Some environment variables couldn't be found. Throw a warning and continue
    if group.missing:
        if group.remaining:
            suggestion = f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?'
        else:
            suggestion = 'No environment variables exist.'

        logger.warning(
            f'{INFO} Could not find environment variable(s) matching: {", ".join(sorted(group.missing))}. {suggestion}')

    # Nothing to delete, so error
    if not group.chosen:
        logger.error(f'{FAIL} No environment variables to delete')
        return 1

    if not force:
        if len(group.chosen) > 1:
            logger.info(f'{INFO} Ready to delete environment variables:\n'
                        f'{get_indented_list(sorted(list(group.chosen)))}\n')
            confirm = query_yes_no('Would you like to delete the environment variables listed above?')
        else:
            chosen_ev = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the environment variable: {chosen_ev}?')
        if not confirm:
            logger.error('Canceling deletion')
            return 1

    conf.environment_variables = list(group.remaining.values())
    conf.save_config()
    return 0


def _confirm_secret_deletion(secrets):
    if len(secrets) > 1:
        logger.info(f'{INFO} Ready to delete secrets:\n'
                    f'{get_indented_list(sorted(secrets))}\n')
        details = ' listed above'
    else:
        details = f': {list(secrets)[0]}'
    confirm = query_yes_no(f'Would you like to delete the secret{details}?')

    if not confirm:
        raise RuntimeError('Canceling deletion')


def delete_secret(secret_names: List[str], force: bool = False, delete_all: bool = False, **kwargs) -> int:
    """Delete the requested secret(s) from the user's clusters

    Args:
        secret_names: List of secrets to delete
        force: If True, do not request confirmation. Defaults to False.

    Returns:
        True if deletion was successful
    """
    del kwargs

    if not (secret_names or delete_all):
        logger.error(f'{FAIL} Must specify secret names or --all.')
        return 1

    try:
        conf: MCLIConfig = MCLIConfig.load_config()
        if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
            # Get secrets to delete
            to_delete_secrets = api_get_secrets(secret_names) if not delete_all else api_get_secrets()
            if not to_delete_secrets:
                if secret_names:
                    logger.warning(f'{INFO} Could not find secrets(s) matching: {", ".join(secret_names)}')
                else:
                    logger.warning(f'{INFO} Could not find any secrets')
                return 1

            # Confirm and delete
            if not force:
                _confirm_secret_deletion(to_delete_secrets)
            with console.status('Deleting secrets..'):
                deleted = api_delete_secrets(secrets=to_delete_secrets, timeout=None)
            logger.info(f'{OK} Deleted secret(s): {", ".join([s.name for s in deleted])}')
        else:
            if delete_all:
                secret_names = ['*']

            kube_delete_secret(secret_names, conf, force)

    except (KubernetesException, MAPIException) as e:
        if e.status == HTTPStatus.NOT_FOUND:
            logger.error(f'{FAIL} No secrets to delete')
        else:
            logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    return 0


def kube_delete_secret(secret_names: List[str], conf: MCLIConfig, force: bool = False):

    if not conf.clusters:
        raise KubernetesException(
            HTTPStatus.NOT_FOUND,
            'No clusters found. You must have at least 1 cluster added before working with secrets.')

    # Note, we could just attempt to delete and catch the error.
    # I think it's a bit cleaner to first check if the secret exists, but this will be a bit slower
    # This slowness should be OK for secrets since they are generally small in number

    ref_cluster = conf.clusters[0]
    secret_manager = SecretManager(ref_cluster)

    group = DeleteGroup(secret_names, {ps.secret.name: ps for ps in secret_manager.get_secrets()})

    # Some clusters couldn't be found. Throw a warning and continue
    if group.missing:
        if group.remaining:
            suggestion = f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?'
        else:
            suggestion = 'No secrets exist.'

        logger.warning(f'{INFO} Could not find secrets(s) matching: {", ".join(sorted(group.missing))}. {suggestion}')

    if not group.chosen:
        raise KubernetesException(HTTPStatus.NOT_FOUND, 'No secrets to delete')

    if not force:
        _confirm_secret_deletion(group.chosen)

    failures: Dict[str, List[str]] = {}
    with console.status('Deleting secrets...') as status:
        for cluster in conf.clusters:
            with Cluster.use(cluster):
                status.update(f'Deleting secrets from {cluster.name}...')
                for ps in group.chosen.values():
                    success = ps.delete(cluster.namespace)
                    if not success:
                        failures.setdefault(ps.secret.name, []).append(cluster.name)

    deleted = sorted([name for name in group.chosen if name not in failures])
    if deleted:
        logger.info(f'{OK} Deleted secret(s): {", ".join(deleted)}')

    if failures:
        for name, failed_clusters in failures.items():
            logger.error(f'Secret {name} could not be deleted from platform(s): {", ".join(sorted(failed_clusters))}')
        raise KubernetesException(HTTPStatus.INTERNAL_SERVER_ERROR,
                                  f'Could not delete secret(s): {", ".join(sorted(list(failures.keys())))}')


def delete_cluster(cluster_names: List[str], force: bool = False, delete_all: bool = False, **kwargs) -> int:
    del kwargs

    if not (cluster_names or delete_all):
        logger.error(f'{FAIL} Must specify cluster names or --all.')
        return 1

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if delete_all:
        cluster_names = ['*']

    group = DeleteGroup(cluster_names, {pl.name: pl for pl in conf.clusters})

    # Some clusters couldn't be found. Throw a warning and continue
    if group.missing:
        if group.remaining:
            suggestion = f'Maybe you meant one of: {", ".join(sorted(list(group.remaining)))}?'
        else:
            suggestion = 'No clusters exist.'
        logger.warning(f'{INFO} Could not find cluster(s) matching: {", ".join(sorted(group.missing))}. {suggestion}')

    # Nothing to delete, so error
    if not group.chosen:
        logger.error(f'{FAIL} No cluster to delete')
        return 1

    if not force:
        if len(group.chosen) > 1:
            logger.info(f'{INFO} Ready to delete clusters:\n'
                        f'{get_indented_list(sorted(list(group.chosen)))}\n')
            confirm = query_yes_no('Would you like to delete the clusters listed above?')
        else:
            chosen_cluster = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the cluster: {chosen_cluster}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion')
            return 1

    conf.clusters = list(group.remaining.values())
    conf.save_config()

    logger.info(f"{OK} Deleted cluster{'s' if len(group.chosen) > 1 else ''}: {', '.join(list(group.chosen.keys()))}")
    return 0


def _split_glob_filters(filters: List[str]) -> Tuple[List[str], Optional[List[str]]]:
    """Split a list of filters into glob-containing and non-glob-containing filters
    """

    globbers: List[str] = []
    non_globbers: Optional[List[str]] = []
    for f in filters:
        if is_glob(f):
            globbers.append(f)
        else:
            non_globbers.append(f)

    # Glob needs an all-match if all filters are non-glob
    if not globbers:
        globbers = ['*']

    # Non-glob filters needs to be None if all filters are glob
    if not non_globbers:
        non_globbers = None

    return globbers, non_globbers


def delete_run(name_filter: Optional[List[str]] = None,
               cluster_filter: Optional[List[str]] = None,
               status_filter: Optional[List[RunStatus]] = None,
               delete_all: bool = False,
               force: bool = False,
               **kwargs):
    del kwargs

    if not (name_filter or cluster_filter or status_filter or delete_all):
        logger.error(f'{FAIL} Must specify run names or at least one of --cluster, --status, --all.')
        return 1

    if not name_filter:
        # Accept all that pass other filters
        name_filter = ['*']

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    # Use get_runs only for the non-glob names provided. Any globs will be handled by DeleteGroup
    glob_filters, run_names = _split_glob_filters(name_filter)
    if not conf.feature_enabled(FeatureFlag.USE_MCLOUD) and not conf.clusters:
        logger.error(f'{FAIL} No clusters found. You must have at least 1 cluster added before working with runs.')
        return 1
    runs = get_runs(runs=run_names or None, clusters=cluster_filter, statuses=status_filter)
    group = DeleteGroup(glob_filters, {r.name: r for r in runs})

    if not group.chosen:
        if delete_all:
            logger.error(f'{FAIL} No runs found.')
        else:
            logger.error(f'{FAIL} No runs found matching the specified criteria.')
        return 1

    if not force:
        if len(group.chosen) > 1:
            if len(group.chosen) >= 50:
                logger.info(f'Ready to delete {len(group.chosen)} runs')
                confirm = query_yes_no(f'Would you like to delete all {len(group.chosen)} runs?')
            else:
                logger.info(f'{INFO} Ready to delete runs:\n'
                            f'{get_indented_list(sorted(list(group.chosen)))}\n')
                confirm = query_yes_no('Would you like to delete the runs listed above?')
        else:
            chosen_run = list(group.chosen)[0]
            confirm = query_yes_no(f'Would you like to delete the run: {chosen_run}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion')
            return 1

    plural = 's' if len(group.chosen) > 1 else ''
    with console.status(f'Deleting run{plural}...') as console_status:
        runs = list(group.chosen.values())
        try:
            deleted = delete_runs(runs)
        except (KubernetesException, MAPIException, RuntimeError) as e:
            logger.error(f'{FAIL} {e}')
            return 1

        if not deleted:
            console_status.stop()
            logger.error('Run deletion failed in an unknown way')
            return 1

    logger.info(f'{OK} Deleted run{plural}')
    return 0
