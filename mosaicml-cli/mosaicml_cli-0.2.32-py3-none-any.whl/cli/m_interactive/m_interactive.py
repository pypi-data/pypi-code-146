""" mcli interactive Entrypoint """
import argparse
import logging
from typing import List, Optional, Set

from mcli.api.exceptions import MCLIRunConfigValidationError
from mcli.api.kube.runs import create_run, delete_runs, get_runs
from mcli.api.model.run import Run
from mcli.config import MESSAGE, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.models.mcli_cluster import Cluster
from mcli.models.run_config import RunConfig
from mcli.serverside.clusters.cluster import GenericK8sCluster
from mcli.serverside.clusters.cluster_instances import (IncompleteInstanceRequest, InstanceRequest,
                                                        InstanceTypeUnavailable, UserInstanceRegistry, ValidInstance)
from mcli.serverside.clusters.instance_type import GPUType
from mcli.serverside.job.mcli_job import MCLIJobType
from mcli.utils.utils_epilog import CommonLog, EpilogSpinner, RunEpilog
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_kube import connect_to_pod, get_pod_rank, list_run_pods
from mcli.utils.utils_logging import FAIL, INFO, OK, WARN, console
from mcli.utils.utils_run_status import PodStatus, RunStatus
from mcli.utils.utils_types import get_hours_type

logger = logging.getLogger(__name__)


def _get_interactive_instance_registry() -> UserInstanceRegistry:

    interactive_clusters = []
    for cluster in MCLIConfig.load_config(safe=True).clusters:
        if GenericK8sCluster.from_mcli_cluster(cluster).interactive:
            interactive_clusters.append(cluster)

    return UserInstanceRegistry(interactive_clusters, allow_mcloud=False)


# pylint: disable-next=invalid-name
INTERACTIVE_REGISTRY = _get_interactive_instance_registry()


def get_min_gpu_option(options: List[ValidInstance]) -> ValidInstance:
    if not options:
        # This should not really be hit, but just in case
        raise RuntimeError('No valid interactive instances available.')

    gpu_options = sorted([option for option in options if option.gpu_num > 0], key=lambda o: o.gpu_num)
    if gpu_options:
        # Return smallest GPU option
        return gpu_options[0]
    else:
        # No GPU options so just return first available CPU option
        return options[0]


def get_valid_interactive_instance(cluster: Optional[str], gpu_type: Optional[str],
                                   gpus: Optional[int]) -> ValidInstance:
    """Get a fully-specified interactive instance from the provided requirements
    """
    request = InstanceRequest(cluster=cluster, gpu_type=gpu_type, gpu_num=gpus)
    options = INTERACTIVE_REGISTRY.lookup(request)
    logger.debug(f'Found {len(options)} potential instances')

    if len(options) == 1:
        return options[0]
    elif len(options) > 1:
        per_cluster_options = {}
        for option in options:
            per_cluster_options.setdefault(option.cluster, []).append(option)

        if len(per_cluster_options) == 1:
            cluster = options[0].cluster
            return get_min_gpu_option(per_cluster_options[cluster])
        elif per_cluster_options.get('r1z2', []):
            return get_min_gpu_option(per_cluster_options['r1z2'])

    raise IncompleteInstanceRequest(request, ValidInstance.to_registry(options), INTERACTIVE_REGISTRY.registry)


def create_interactive_session(name: str, instance: ValidInstance, cpus: int, image: str, hours: float) -> Run:

    command = f'sleep {int(3600 * hours)}'

    config = RunConfig(
        name=name,
        cluster=instance.cluster,
        gpu_type=instance.gpu_type,
        gpu_num=instance.gpu_num,
        cpus=cpus if instance.gpu_num == 0 else None,
        optimization_level=0,
        command=command,
        image=image,
    )
    return create_run(config, timeout=None, _job_type=MCLIJobType.INTERACTIVE)


def get_latest_interactive_session() -> Run:
    """Returns the most recent interactive session. If none exist, raises RuntimeError
    """
    # No session name passed, so get latest session
    # pylint: disable-next=protected-access
    all_runs = [r for r in get_runs() if r._type is MCLIJobType.INTERACTIVE]
    if not all_runs:
        raise RuntimeError('Could not find any existing interactive sessions. Try re-running without -r or --reconnect')
    run = sorted(all_runs, key=lambda s: s.created_at, reverse=True)[0]
    return run


def interactive_entrypoint(
    name: Optional[str] = None,
    cluster: Optional[str] = None,
    gpu_type: Optional[str] = None,
    gpus: Optional[int] = None,
    cpus: int = 1,
    hrs: Optional[float] = None,
    hours: Optional[float] = None,
    image: str = 'mosaicml/pytorch',
    confirm: bool = True,
    connect: bool = True,
    reconnect: Optional[str] = None,
    rank: int = 0,
    **kwargs,
) -> int:
    # pylint: disable=too-many-statements
    del kwargs

    # Hours can be specified as a positional argument (hrs) or named argument (hours)
    if hours and hrs:
        logger.error(f'{FAIL} The duration of your interactive session was specified twice. '
                     'Please use only the positional argument or --hours. '
                     'See mcli interactive --help for more details.')

    hours = hrs or hours
    if hours is None and reconnect is None:
        logger.error(f'{FAIL} Please specify the duration of your interactive session. '
                     'See mcli interactive --help for details.')
        return 1

    # If cluster unknown and in mcloud mode, try submitting it to mcloud interactive
    if MCLIConfig.load_config(safe=True).feature_enabled(FeatureFlag.USE_MCLOUD):
        available_clusters = sorted(list(INTERACTIVE_REGISTRY.registry.keys()))

        # pylint: disable=import-outside-toplevel
        from mcli.cli.m_interactive.mcloud_interactive import mcloud_interactive
        if cluster not in available_clusters:
            return mcloud_interactive(name, cluster, gpu_type, gpus, cpus, hours, image, rank, connect, reconnect)

    exit_code: Optional[int] = None
    try:
        if reconnect:
            # Reconnect to a named session
            all_runs = get_runs([reconnect])
            if not all_runs:
                raise RuntimeError(f'Could not find an interactive session named {reconnect}')
            run = all_runs[0]
            logger.info(f'{INFO} Attempting to connect to session: [cyan]{run.name}[/]')
        elif reconnect == '':
            # No session name passed, so get latest session
            run = get_latest_interactive_session()
            logger.info(f'{INFO} No session name provided. '
                        f'Attempting to connect to latest session: [cyan]{run.name}[/]')
        else:
            # Create a new session
            valid_instance = get_valid_interactive_instance(cluster, gpu_type, gpus)
            logger.debug(f'Chosen instance type: {valid_instance}')
            if not name:
                name = f'interactive-{valid_instance.gpu_type.replace("_", "-")}-{valid_instance.gpu_num}'.lower()

            if valid_instance.gpu_type != str(GPUType.NONE):
                gpu_cpu_string = f'{valid_instance.gpu_num} GPU(s)'
            else:
                gpu_cpu_string = f'{cpus} CPU(s)'

            logger.info(
                f'{OK} Ready to submit a [bold]{gpu_cpu_string}[/] interactive session for [bold]{hours} hour(s)[/] '
                f'to cluster [bold green]{valid_instance.cluster}[/]')
            if confirm:
                confirm = query_yes_no('Do you want to submit?', default=True)
                if not confirm:
                    raise RuntimeError('Canceling!')
            assert hours is not None  # Guard at the top guarantees this
            run = create_interactive_session(name, valid_instance, cpus, image, hours)
            msg = f'{OK} Interactive session [cyan]{run.name}[/] submitted'
            if connect:
                logger.info(msg)
            else:
                logger.info(f'{msg}. To connect to the session, run:\n\n'
                            f'mcli interactive -r {run.name}')

        if connect:
            exit_code = connect_session(run, rank=rank)
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    except (InstanceTypeUnavailable) as e:
        logger.error(e)
        return 1
    except (MCLIRunConfigValidationError) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(e)
        return 1

    return exit_code or 0


def connect_session(run: Run, rank: int = 0) -> int:

    cluster = Cluster.get_by_name(run.config.cluster)
    if run.status.before(RunStatus.RUNNING):
        # Run hasn't started yet, so let's wait with an epilog
        logger.info(f'{INFO} Waiting for session to start...')
        logger.info(f'{INFO} Press Ctrl+C to quit and interact with your session manually.')
        timeout = 300
        try:
            with Cluster.use(run.config.cluster) as cluster:
                # Pod is creating, so let's use an epilog
                epilog = RunEpilog(run.name, cluster.namespace)
                status: Optional[PodStatus] = None
                with EpilogSpinner() as spinner:
                    status = epilog.wait_until(callback=spinner, timeout=timeout)
                if status is None:
                    # Pod epilog timed out
                    logger.info(
                        f'{INFO} Session [cyan]{run.name}[/] did not start within {timeout} seconds. '
                        'The cluster may be under heavy utilization. '
                        'To monitor your session\'s status, run:\n\n'
                        'mcli get runs\n\n'
                        'To monitor the cluster\'s usage, run:\n\n'
                        f'mcli util {run.config.cluster}\n\n'
                        'Once your session is active, you can connect with:\n\n'
                        f'mcli interactive -r {run.name}',)
                    return 1
                run.status = status.state
        except KeyboardInterrupt:
            return 0

    # Wait timed out
    common_log = CommonLog(logger)
    if run.status in {RunStatus.COMPLETED, RunStatus.STOPPED}:
        logger.warning(f'{WARN} Unable to connect to session [cyan]{run.name}[/]. '
                       'It has already completed or been stopped')
        return 1
    if run.status == RunStatus.FAILED_PULL:
        common_log.log_pod_failed_pull(run.name, run.config.image)
        with console.status('Deleting failed session...'):
            delete_runs([run])
        return 1
    elif run.status == RunStatus.FAILED:
        common_log.log_pod_failed(run.name)
        return 1
    elif run.status.before(RunStatus.RUNNING):
        common_log.log_unknown_did_not_start()
        logger.debug(run.status)
        return 1
    logger.info(f'{OK} Session {run.name} started successfully')

    with Cluster.use(run.config.cluster) as cluster:
        pods = list_run_pods(run.name, cluster.namespace)
        pod_ranks = {get_pod_rank(pod): pod.metadata.name for pod in pods}

    if rank not in pod_ranks:
        valid_ranks = ", ".join(str(r) for r in pod_ranks)
        logger.error(f'{FAIL} Could not connect to node rank {rank} for session {run.name}. \n'
                     f'Available node ranks are: {valid_ranks}')

    rank_str = f"node rank [cyan]{rank}[/] of " if rank > 0 else ""
    logger.info(f'{OK} Connecting to {rank_str}interactive session [cyan]{run.name}[/]')
    logger.info(
        f'{INFO} Press Ctrl+C to quit connecting. Once connected, press Ctrl+D or type exit '
        'to leave the session.',)

    connected = connect_to_pod(pod_ranks[rank], cluster.to_kube_context())
    if not connected:
        logger.warning('Interactive session disconnected')
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:

    hrs_grp = parser.add_mutually_exclusive_group()
    hrs_grp.add_argument(
        'hrs',
        metavar='HOURS',
        nargs='?',
        type=get_hours_type(),
        help='Number of hours the interactive session should run',
    )
    hrs_grp.add_argument(
        '--hours',
        nargs='?',
        type=get_hours_type(),
        help='Number of hours the interactive session should run',
    )

    parser.add_argument(
        '--name',
        default=None,
        metavar='NAME',
        type=str,
        help='Name for the interactive session. '
        'Default: "interactive-<gpu type>-<gpu num>"',
    )

    if INTERACTIVE_REGISTRY.registry:
        cluster_descriptions = [
            IncompleteInstanceRequest.get_cluster_description(pl, instances)
            for pl, instances in INTERACTIVE_REGISTRY.registry.items()
        ]
        full_cluster_description = '\nAvailable interactive instances:\n\n'
        full_cluster_description += '\n'.join(cluster_descriptions)
    else:
        full_cluster_description = '\nNo interactive instances available\n\n'

    cluster_arguments = parser.add_argument_group('Instance settings', description=full_cluster_description)
    available_clusters = sorted(list(INTERACTIVE_REGISTRY.registry.keys()))
    cluster_arguments.add_argument(
        '--cluster',
        '--platform',
        default=None,
        metavar='CLUSTER',
        help='Cluster where your interactive session should run. If you '
        'only have one available, that one will be selected by default. '
        'Depending on your cluster, you\'ll have access to different GPU types and counts. '
        'See the available combinations above. '
        f'Choices: {", ".join(available_clusters)}',
    )

    available_types: Set[str] = set()
    available_nums: Set[int] = set()
    for instance in INTERACTIVE_REGISTRY.registry.values():
        for gpu_type, gpu_nums in instance.items():
            available_types.add(str(gpu_type))
            available_nums.update(set(gpu_nums))
    gpu_types = sorted(list(available_types))
    gpu_nums = sorted(list(available_nums))

    cluster_arguments.add_argument(
        '--gpu-type',
        choices=gpu_types,
        metavar='TYPE',
        help=f'Type of GPU to use. Choices: {", ".join(gpu_types)}. '
        'Valid GPU types depend on the cluster and GPU numbers requested. See the available combinations above',
    )
    cluster_arguments.add_argument(
        '--gpus',
        type=int,
        metavar='NGPUs',
        choices=gpu_nums,
        help=f'Number of GPUs to run interactively. Choices: {", ".join(str(x) for x in gpu_nums)}. '
        'Valid GPU numbers depend on the cluster and GPU type. See the available combinations above.',
    )
    cluster_arguments.add_argument(
        '--cpus',
        default=1,
        type=int,
        metavar='NCPUs',
        help='Number of CPUs to run interactively. This will only take effect when --gpu-type is set to "none". '
        'Default: %(default)s',
    )

    parser.add_argument(
        '--image',
        default='mosaicml/pytorch',
        help='Docker image to use',
    )
    parser.add_argument(
        '-y',
        '--no-confirm',
        dest='confirm',
        action='store_false',
        help='Do not request confirmation',
    )
    parser.add_argument(
        '--no-connect',
        dest='connect',
        action='store_false',
        help='Do not connect to the interactive session immediately',
    )
    parser.add_argument(
        '-r',
        '--reconnect',
        const='',
        metavar='NAME',
        nargs='?',
        help='Reconnect to an existing interactive session. '
        'You can provide the name of the session you\'d like to reconnect to, or, '
        'if not provided, your most recent one will be used',
    )
    parser.add_argument('--rank',
                        metavar='N',
                        default=0,
                        type=int,
                        help='Connect to the specified node rank within the run')
    parser.set_defaults(func=interactive_entrypoint)
    return parser


def add_interactive_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    examples = """

Examples:

# Create a 1 hour interactive session
> mcli interactive --hours 1

# Create a 1 hour interactive session with custom name and docker image
> mcli interactive --hours 1 --image my-image --name my-session

# Reconnect to the latest interactive session
> mcli interactive -r

# Reconnect to the interactive session my-session-1234
> mcli interactive -r my-session-1234

# Connect to the rank 1 node from interactive session my-session-1234
> mcli interactive -r my-session-1234 --rank 1
    """

    interactive_parser: argparse.ArgumentParser = subparser.add_parser(
        'interactive',
        help='Create an interactive session',
        description=('Create an interactive session. '
                     'Once created, you can attach to the session. '
                     'Interactive sessions are only allowed in pre-specified clusters.'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=examples,
    )
    get_parser = configure_argparser(parser=interactive_parser)
    return get_parser
