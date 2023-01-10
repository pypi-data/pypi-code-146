""" CLI Get options"""
import argparse
from typing import List, Optional

from mcli.cli.m_get import get_clusters, get_environment_variables, get_secrets
from mcli.cli.m_get.display import OutputDisplay
from mcli.cli.m_get.runs import get_runs_argparser
from mcli.models.mcli_secret import SecretType


def get_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-o',
                        '--output',
                        type=OutputDisplay,
                        choices=list(OutputDisplay),
                        default=OutputDisplay.TABLE,
                        metavar='FORMAT',
                        help=f'Output display format. Should be one of {list(OutputDisplay)}')


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Objects',
                                       description='The table below shows the objects that you can get information on',
                                       help='DESCRIPTION',
                                       metavar='OBJECT')
    parser.set_defaults(func=get_entrypoint, parser=parser)

    cluster_parser = subparsers.add_parser('clusters',
                                           aliases=['cluster', 'platforms', 'platform'],
                                           help='List registered clusters')
    add_common_arguments(cluster_parser)
    cluster_parser.set_defaults(func=get_clusters)

    environment_parser = subparsers.add_parser('env',
                                               aliases=['environment', 'envs'],
                                               help='List registered environment variables')
    add_common_arguments(environment_parser)
    environment_parser.set_defaults(func=get_environment_variables)

    # pylint: disable-next=invalid-name
    SECRET_EXAMPLES = """

Examples:

> mcli get secrets
NAME         TYPE
foo          environment
docker-cred  docker_registry
file         mounted

> mcli get secrets --type environment
NAME         TYPE
foo          environment
    """
    secrets_parser = subparsers.add_parser(
        'secrets',
        aliases=['secret'],
        help='List registered secrets and credentials',
        description='List all of your registered secrets and credentials. Each '
        'listed secret will be added to your run automatically. For details on '
        'exactly how each type of secret is added to your run, look to the '
        'individual secret type docs.',
        epilog=SECRET_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_common_arguments(secrets_parser)
    secrets_parser.set_defaults(func=get_secrets)
    secrets_parser.add_argument('--type',
                                choices=["all"] + [i.name for i in SecretType if i != SecretType.generic],
                                default="all",
                                dest='secret_type',
                                help='Filter and show only secrets of this type')

    runs_parser = get_runs_argparser(subparsers)
    add_common_arguments(runs_parser)

    return parser


def add_get_argparser(subparser: argparse._SubParsersAction,
                      parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    del parents

    get_parser: argparse.ArgumentParser = subparser.add_parser(
        'get',
        aliases=['g'],
        help='Get info about objects created with mcli',
    )
    get_parser = configure_argparser(parser=get_parser)
    return get_parser
