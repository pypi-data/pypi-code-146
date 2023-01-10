""" m delete Entrypoint """
import argparse
from typing import List, Optional

from mcli.cli.m_delete.delete import delete_cluster, delete_environment_variable, delete_run, delete_secret
from mcli.config import FeatureFlag, MCLIConfig
from mcli.utils.utils_cli import CLIExample, Description, comma_separated, get_example_text
from mcli.utils.utils_run_status import CLI_STATUS_OPTIONS, RunStatus

# pylint: disable-next=invalid-name
_description = Description("""
The table below shows the objects that you can delete. For each object below, you can
delete or more of them by name. Each object also supports glob-style selection and --all
to delete all.

To view object-specific additional help, run:

mcli delete <object> --help
""")

_cluster_description = Description("""
Remove cluster(s) from your setup. This prevents you from launching runs on any of their
instances.
""")
_cluster_example_all = CLIExample(example='mcli delete clusters rXzX rXzY', description='Delete multiple clusters')
_CLUSTER_EXAMPLES = [
    _cluster_example_all,
    CLIExample(example='mcli delete clusters rXz*', description='Delete clusters that match a pattern'),
    CLIExample(example='mcli delete clusters --all', description='Delete all clusters'),
]

_env_description = Description("""
Delete one or more environment variables from your standard workload setup.
""")
_env_example_all = CLIExample(example='mcli delete env FOO', description='Delete an environment variable FOO')
_env_examples = [
    _env_example_all,
    CLIExample(example='mcli delete envs FOO BAR', description='Delete multiple environment variables'),
    CLIExample(example='mcli delete envs --all', description='Delete all environment variables'),
]

_secret_description = Description("""
Delete one or more secrets from your standard workload setup. These secrets will be
removed completely from the secrets database and no longer added to any subsequent runs.
""")
_secret_example_all = CLIExample(example='mcli delete secrets foo bar', description='Delete secrets foo and bar')
_secret_examples = [
    CLIExample(example='mcli delete secret foo', description='Delete a secret named foo'),
    _secret_example_all,
    CLIExample(example='mcli delete secrets --all', description='Delete all secrets'),
]

_run_description = Description("""
Delete a run or set of runs that match some conditions.
""")
_run_example_simple = CLIExample(example='mcli delete run my-run-1', description='Delete a specific run')
_run_example_status = CLIExample(example='mcli delete runs --status failed,completed',
                                 description='Delete all failed and completed runs')

_run_examples = [
    _run_example_simple,
    CLIExample(example='mcli delete runs --cluster rXzX,rXzY', description='Delete all runs on clusters rXzX and rXzY'),
    _run_example_status,
    CLIExample(example='mcli delete runs --all', description='Delete all runs (Please be careful!)'),
]
_all_examples = [
    _cluster_example_all,
    _env_example_all,
    _secret_example_all,
    _run_example_simple,
    _run_example_status,
]


def delete(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument('-y',
                        '--force',
                        dest='force',
                        action='store_true',
                        help='Skip confirmation dialog before deleting. Please be careful!')


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    conf = MCLIConfig.load_config(safe=True)
    subparsers = parser.add_subparsers(
        title='MCLI Objects',
        help='DESCRIPTION',
        metavar='OBJECT',
    )
    parser.set_defaults(func=delete, parser=parser)

    if not conf.feature_enabled(FeatureFlag.USE_MCLOUD):
        cluster_parser = subparsers.add_parser(
            'cluster',
            aliases=['clusters', 'platform', 'platforms'],
            help='Delete one or more clusters',
            description=_cluster_description,
            epilog=get_example_text(*_CLUSTER_EXAMPLES),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        cluster_parser.add_argument(
            'cluster_names',
            nargs='*',
            metavar='CLUSTER',
            help='The name of the cluster(s) to delete. Also supports glob-style pattern matching')
        cluster_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all clusters')
        cluster_parser.set_defaults(func=delete_cluster)
        add_common_args(cluster_parser)

    environment_parser = subparsers.add_parser(
        'env',
        aliases=['envs'],
        help='Delete one or more environment variables',
        description=_env_description,
        epilog=get_example_text(*_env_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    environment_parser.add_argument(
        'variable_names',
        nargs='*',
        metavar='ENV',
        help='The name(s) of the environment variable(s) to delete. Also supports glob-style pattern matching')
    environment_parser.add_argument('-a',
                                    '--all',
                                    dest='delete_all',
                                    action='store_true',
                                    help='Delete all environment variables')
    environment_parser.set_defaults(func=delete_environment_variable)
    add_common_args(environment_parser)

    secrets_parser = subparsers.add_parser(
        'secret',
        aliases=['secrets'],
        help='Delete one or more secrets',
        description=_secret_description,
        epilog=get_example_text(*_secret_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    secrets_parser.add_argument(
        'secret_names',
        nargs='*',
        metavar='SECRET',
        help='The name(s) of the secret(s) to delete. Also supports glob-style pattern matching.')
    secrets_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all secrets')
    secrets_parser.set_defaults(func=delete_secret)
    add_common_args(secrets_parser)

    run_parser = subparsers.add_parser(
        'run',
        aliases=['runs'],
        help='Delete one or more runs',
        description=_run_description,
        epilog=get_example_text(*_run_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    run_parser.add_argument('name_filter',
                            nargs='*',
                            metavar='RUN',
                            default=None,
                            help='The name(s) of the run(s) to delete')
    run_parser.add_argument('-c',
                            '--cluster',
                            '-p',
                            '--platform',
                            dest='cluster_filter',
                            metavar='PLATFORM',
                            type=comma_separated,
                            default=None,
                            help='Delete runs on the specified cluster(s). If no other arguments are provided, all '
                            'runs on the specified cluster(s) will be deleted. Multiple clusters should be specified '
                            'using a comma-separated list, e.g. "cluster1,cluster2"')

    def status(value: str) -> List[RunStatus]:
        res = comma_separated(value, RunStatus.from_string)
        if res == [RunStatus.UNKNOWN] and value != [RunStatus.UNKNOWN.value]:
            raise TypeError(f'Unknown value {value}')
        return res

    run_parser.add_argument(
        '-s',
        '--status',
        dest='status_filter',
        default=None,
        metavar='STATUS',
        type=status,
        help=f'Delete runs with the specified statuses (choices: {", ".join(CLI_STATUS_OPTIONS)}). '
        'Multiple statuses should be specified using a comma-separated list, e.g. "failed,completed"')
    run_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all runs')
    run_parser.set_defaults(func=delete_run)
    add_common_args(run_parser)

    return parser


def add_delete_argparser(subparser: argparse._SubParsersAction,
                         parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    del parents

    delete_parser: argparse.ArgumentParser = subparser.add_parser(
        'delete',
        aliases=['del'],
        help='Delete one or more MCLI objects',
        description=_description,
        epilog=get_example_text(*_all_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    delete_parser = configure_argparser(parser=delete_parser)
    return delete_parser
