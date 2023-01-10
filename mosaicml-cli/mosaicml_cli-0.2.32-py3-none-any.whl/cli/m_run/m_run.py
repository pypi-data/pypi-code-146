""" mcli run Entrypoint """
import argparse
import logging
import textwrap
from typing import Optional

from mcli.api.exceptions import KubernetesException, MAPIException, MCLIConfigError, MCLIRunConfigValidationError
from mcli.api.kube.runs import create_run as kube_create_run
from mcli.api.kube.runs import delete_runs
from mcli.api.runs import create_run
from mcli.api.runs.api_watch_run import EpilogSpinner as CloudEpilogSpinner
from mcli.config import FeatureFlag, MCLIConfig
from mcli.models.mcli_cluster import Cluster
from mcli.models.run_config import VALID_OPTIMIZATION_LEVELS
from mcli.sdk import Run, RunConfig, follow_run_logs, wait_for_run_status
from mcli.serverside.clusters.cluster import InvalidPriorityError, PriorityLabel
from mcli.serverside.clusters.cluster_instances import InstanceTypeUnavailable, UserInstanceRegistry
from mcli.serverside.clusters.gpu_type import GPUType
from mcli.utils.utils_epilog import CommonLog, EpilogSpinner, RunEpilog
from mcli.utils.utils_logging import FAIL, INFO, OK, console
from mcli.utils.utils_run_status import RunStatus

logger = logging.getLogger(__name__)


def print_help(**kwargs) -> int:
    del kwargs
    mock_parser = argparse.ArgumentParser()
    _configure_parser(mock_parser)
    mock_parser.print_help()
    return 1


def follow_run(run: Run) -> int:
    final_config = run.config
    conf = MCLIConfig.load_config(safe=True)
    last_status: Optional[RunStatus] = None
    if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
        with CloudEpilogSpinner(run, RunStatus.RUNNING) as watcher:
            run = watcher.follow()
            last_status = run.status
    else:
        with Cluster.use(final_config.cluster) as cluster:
            logger.info(f'{INFO} Run [cyan]{run.name}[/] submitted. Waiting for it to start...')
            logger.info(f'{INFO} You can press Ctrl+C to quit and follow your run manually.')
            epilog = RunEpilog(run.name, cluster.namespace)
            with EpilogSpinner() as spinner:
                state = epilog.wait_until(callback=spinner, timeout=300)
                last_status = state.state if state else None

    # Wait timed out
    common_log = CommonLog(logger)
    if last_status is None:
        common_log.log_timeout()
        return 0
    elif last_status == RunStatus.FAILED_PULL:
        common_log.log_pod_failed_pull(run.name, final_config.image)
        if not conf.feature_enabled(FeatureFlag.USE_MCLOUD):
            with console.status('Deleting failed run...'):
                delete_runs([run])
        return 1
    elif last_status == RunStatus.FAILED:
        common_log.log_pod_failed(run.name)
        return 1
    elif last_status.before(RunStatus.RUNNING):
        common_log.log_unknown_did_not_start()
        logger.debug(last_status)
        return 1

    logger.info(f'{OK} Run [cyan]{run.name}[/] started')
    logger.info(f'{INFO} Following run logs. Press Ctrl+C to quit.\n')

    end = '' if conf.feature_enabled(FeatureFlag.USE_MCLOUD) else '\n'
    for line in follow_run_logs(run, rank=0):
        print(line, end=end)
    if not end:
        print('')

    wait_for_run_status(run, status=RunStatus.COMPLETED, timeout=10)

    return 0


# pylint: disable-next=too-many-statements
def run_entrypoint(
    file: str,
    priority: Optional[PriorityLabel] = None,
    follow: bool = True,
    override_cluster: Optional[str] = None,
    override_gpu_type: Optional[str] = None,
    override_gpu_num: Optional[int] = None,
    override_image: Optional[str] = None,
    override_name: Optional[str] = None,
    override_optimization_level: Optional[int] = None,
    **kwargs,
) -> int:
    del kwargs

    if file is None:
        return print_help()

    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this run
    ------------------------------------------------------
    """))

    cluster_name: Optional[str] = None
    try:
        run_config = RunConfig.from_file(path=file)

        # command line overrides
        # only supports basic format for now and not structured params
        if override_cluster is not None:
            run_config.cluster = override_cluster

        if override_gpu_type is not None:
            run_config.gpu_type = override_gpu_type

        if override_gpu_num is not None:
            run_config.gpu_num = override_gpu_num

        if override_image is not None:
            run_config.image = override_image

        if override_name is not None:
            run_config.name = override_name

        if override_optimization_level is not None:
            run_config.optimization_level = override_optimization_level

        conf = MCLIConfig.load_config(safe=True)

        with console.status('Submitting run...'):
            if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
                run = create_run(run=run_config, timeout=None)
            else:
                run = kube_create_run(run=run_config, _priority=priority, timeout=None)
        cluster_name = run.config.cluster

        if not follow:
            log_cmd = f'mcli logs {run.name}'
            message = f"""
            {OK} Run [cyan]{run.name}[/] submitted.

            To see the run\'s status, use:

            [bold]mcli get runs[/]

            To see the run\'s logs, use:

            [bold]{log_cmd}[/]
            """
            logger.info(textwrap.dedent(message).strip())
            return 0
        else:
            return follow_run(run)

    except (MAPIException, KubernetesException) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except (InstanceTypeUnavailable) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except (MCLIRunConfigValidationError) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except (MCLIConfigError) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except InvalidPriorityError as e:
        e.cluster = cluster_name
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except FileNotFoundError as e:
        logger.error(f'{FAIL} {e}')
        return 1


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Launch a run in the MosaicML Cloud',
    )
    run_parser.set_defaults(func=run_entrypoint)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    parser.add_argument(
        '--priority',
        choices=list(PriorityLabel),
        type=PriorityLabel.ensure_enum,
        help='Priority level at which runs should be submitted. '
        '(default None)',
    )

    parser.add_argument(
        '--no-follow',
        action='store_false',
        dest='follow',
        default=False,
        help='Do not automatically try to follow the run\'s logs. This is the default behavior',
    )

    parser.add_argument('--follow',
                        action='store_true',
                        dest='follow',
                        default=False,
                        help='Follow the logs of an in-progress run.')

    user_registry = UserInstanceRegistry()
    available_clusters = sorted(list(user_registry.registry.keys()))

    parser.add_argument(
        '--cluster',
        '--platform',
        dest='override_cluster',
        choices=available_clusters,
        help='Optional override for MCLI cluster',
    )

    available_types, available_nums = set(), set()
    for instance in user_registry.registry.values():
        for gpu_type, gpu_nums in instance.items():
            if gpu_type != GPUType.NONE:
                available_types.add(str(gpu_type))
            available_nums.update(set(gpu_nums))
    gpu_types = sorted(list(available_types))
    gpu_nums = sorted(list(available_nums))

    parser.add_argument(
        '--gpu-type',
        dest='override_gpu_type',
        choices=gpu_types,
        help='Optional override for GPU type. Valid GPU type depend on'
        ' the cluster and GPU number requested',
    )

    parser.add_argument(
        '--gpus',
        type=int,
        dest='override_gpu_num',
        choices=gpu_nums,
        help='Optional override for number of GPUs. Valid GPU numbers '
        'depend on the cluster and GPU type',
    )

    parser.add_argument(
        '--image',
        dest='override_image',
        help='Optional override for docker image',
    )

    parser.add_argument(
        '--name',
        '--run-name',
        dest='override_name',
        help='Optional override for run name',
    )

    conf = MCLIConfig.load_config(safe=True)
    if conf.internal:
        parser.add_argument(
            '-o',
            '--optimization_level',
            dest='override_optimization_level',
            choices=VALID_OPTIMIZATION_LEVELS,
            type=int,
            help='Optimization level for auto-optimization agent. '
            '0 to disable, 1 for safe system-level speedups, 2 for optimal speed at same accuracy, '
            '3 for optimal accuracy at same speed',
        )
