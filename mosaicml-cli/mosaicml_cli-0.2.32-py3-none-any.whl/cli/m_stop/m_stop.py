""" mcli stop Entrypoint """
import argparse
import logging
from http import HTTPStatus
from typing import List

from kubernetes.client.exceptions import ApiException

from mcli.api.exceptions import KubernetesException, MAPIException
from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.sdk import stop_runs
from mcli.utils.utils_logging import FAIL, INFO, WARN

logger = logging.getLogger(__name__)


def stop_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def stop_run(
    run_names: List[str],
    **kwargs,
) -> int:
    del kwargs

    try:
        _ = MCLIConfig.load_config()
        try:
            stopped_runs = stop_runs(run_names)
        except MAPIException as e:
            if e.status != HTTPStatus.NOT_FOUND:
                raise e
            stopped_runs = []

        found_runs = {r.name for r in stopped_runs}
        missing_runs = [r for r in run_names if r not in found_runs]
        if missing_runs:
            logger.info(f'{WARN} Could not find run with name(s): {", ".join(missing_runs)}. '
                        f'Check that they exist using `mcli get runs`')

        if len(stopped_runs) > 1:
            sep = '\n   - '
            formatted_names = sep.join(r.name for r in stopped_runs)
            logger.info(f'{INFO} Successfully stopped runs: {sep}{formatted_names}')
        elif len(stopped_runs) == 1:
            logger.info(f'{INFO} Successfully stopped run: {stopped_runs[0].name}')

    except (KubernetesException, MAPIException) as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except ApiException as e:
        e = KubernetesException.transform_api_exception(e)
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    return 0


def add_stop_parser(subparser: argparse._SubParsersAction):
    """Add the parser for stop runs
    """

    stop_parser: argparse.ArgumentParser = subparser.add_parser(
        'stop',
        help='Stop objects created with mcli',
    )
    stop_parser.set_defaults(func=stop_entrypoint, parser=subparser)

    subparsers = stop_parser.add_subparsers(
        title='MCLI Objects',
        description='The table below shows the objects that you can stop',
        help='DESCRIPTION',
        metavar='OBJECT',
    )

    stop_run_parser = subparsers.add_parser(
        'run',
        aliases=['runs'],
        help='Stop runs',
    )
    stop_run_parser.set_defaults(func=stop_run)
    stop_run_parser.add_argument(
        'run_names',
        metavar='RUN',
        nargs="+",
        type=str,
        help='The name of the run to stop',
    )

    return stop_parser
