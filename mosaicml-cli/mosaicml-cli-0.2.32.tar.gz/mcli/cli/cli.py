#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

""" MCLI Entrypoint """

import argparse
import itertools
import logging
import sys
from string import ascii_lowercase
from typing import Tuple

import argcomplete

from mcli.api.exceptions import MCLIConfigError
from mcli.cli.m_clean.m_clean import clean_mcli
from mcli.cli.m_create.m_create import add_create_argparser
from mcli.cli.m_delete.m_delete import add_delete_argparser
from mcli.cli.m_get.m_get import add_get_argparser
from mcli.cli.m_init.m_init import initialize_mcli
from mcli.cli.m_init.m_init_kube import add_init_kube_parser
from mcli.cli.m_interactive.m_interactive import add_interactive_argparser
from mcli.cli.m_log.m_log import add_log_parser
from mcli.cli.m_root.m_config import m_get_config
from mcli.cli.m_run.m_run import add_run_argparser
from mcli.cli.m_set_unset.m_set import add_set_argparser
from mcli.cli.m_set_unset.m_unset import add_unset_argparser
from mcli.cli.m_stop.m_stop import add_stop_parser
from mcli.cli.m_use.m_use import add_use_argparser
from mcli.cli.m_util.m_util import add_util_argparser
from mcli.config import FeatureFlag, MCLIConfig, update_user_config
from mcli.utils.utils_cli import MCLIArgumentParser
from mcli.utils.utils_logging import console_handler
from mcli.utils.utils_pypi import NeedsUpdateError, check_new_update_available
from mcli.version import get_formatted_version, print_version

logger = logging.getLogger('mcli')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


def add_clean_argparser(subparser: argparse._SubParsersAction) -> None:
    clean_parser: argparse.ArgumentParser = subparser.add_parser('clean', aliases=['cl'], help='Clean MCLI')
    clean_parser.set_defaults(func=clean_mcli)


def add_root_commands(subparser: argparse._SubParsersAction) -> None:
    """Adds root level commands to the CLI

    Args:
        subparser: The subparser to add commands to
    """
    config_parser: argparse.ArgumentParser = subparser.add_parser(
        'config', aliases=['c'], help='Printout details on the current mcli configuration')
    config_parser.set_defaults(func=m_get_config)

    init_parser: argparse.ArgumentParser = subparser.add_parser('init', aliases=['i'], help='Initialize MCLI')
    mcloud_mode = init_parser.add_mutually_exclusive_group()
    mcloud_mode.add_argument(
        '--mcloud',
        action='store_true',
        dest='mcloud_mode',
        default=None,
        help='Setup user for MCloud clusters',
    )
    mcloud_mode.add_argument(
        '--legacy',
        action='store_false',
        dest='mcloud_mode',
        default=None,
        help='Setup user for Legacy clusters',
    )
    init_parser.add_argument('--no-input', action='store_true', help='Do not query for user input')
    init_parser.set_defaults(func=initialize_mcli)

    version_parser: argparse.ArgumentParser = subparser.add_parser('version', help='MCLI Version')
    version_parser.set_defaults(func=print_version)


def get_mcli_root() -> Tuple[argparse.ArgumentParser, argparse._SubParsersAction]:
    """Common `mcli` root to be used by all subparsers

    This doesn't assume any local setup has been done yet
    """
    common = MCLIArgumentParser(add_help=False)
    common.add_argument('-v', '--verbose', action='count', help='Increase CLI verbosity', default=0)
    common.add_argument('--version', action='version', help='MCLI version', version=get_formatted_version())
    parents = [common]

    parser = MCLIArgumentParser(prog='mcli', parents=parents)
    subparser = parser.add_subparsers(title='MCLI Commands',
                                      description='The table below shows the commands that are available',
                                      help='DESCRIPTION',
                                      metavar='COMMAND')

    def print_help(**kwargs):
        del kwargs
        parser.print_help()

    parser.set_defaults(func=print_help)

    add_root_commands(subparser=subparser)
    return parser, subparser


def get_parser() -> argparse.ArgumentParser:
    parser, subparser = get_mcli_root()
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        # If MCLIConfig has not been initialized, we skip
        # adding any subcommands that are gated behind
        # setup or feature flags
        pass
    else:
        use_mcloud = conf.feature_enabled(FeatureFlag.USE_MCLOUD)
        if not use_mcloud:
            add_init_kube_parser(subparser=subparser)

        if conf.internal:
            add_use_argparser(subparser=subparser)
            add_clean_argparser(subparser=subparser)

        if conf.allow_interactive:
            add_interactive_argparser(subparser=subparser)

    add_create_argparser(subparser=subparser)
    add_delete_argparser(subparser=subparser)
    add_get_argparser(subparser=subparser)
    add_log_parser(subparser=subparser)
    add_run_argparser(subparser=subparser)
    add_stop_parser(subparser=subparser)
    add_util_argparser(subparser=subparser)
    add_set_argparser(subparser=subparser)
    add_unset_argparser(subparser=subparser)

    return parser


def main() -> int:
    """The main entrypoint
    """
    parser = get_parser()

    aliases = list(ascii_lowercase) + [''.join(i) for i in itertools.product(ascii_lowercase, repeat=2)]
    argcomplete.autocomplete(
        parser,
        exclude=aliases,
        always_complete_options='long',  # type: ignore
    )

    try:
        check_new_update_available()
    except NeedsUpdateError:
        return 1

    try:
        update_user_config()
    except MCLIConfigError:
        return 1

    args = parser.parse_args()

    if len(vars(args)) == 0:
        parser.print_help()
        return 0

    if args.verbose >= 1:
        logger.setLevel(logging.DEBUG)

    console_handler.markup = True

    var_args = vars(args)
    # Need to delete the custom args from the dict because they are added to `args` Namespace by default
    del var_args['verbose']
    try:
        return args.func(**var_args)
    except KeyboardInterrupt as k:
        del k
        logger.info('\nExiting with Keyboard Interrupt')
        return 1
    except Exception as e:
        raise e


if __name__ == '__main__':
    sys.exit(main())
