""" mcli util command """
import argparse

from mcli.config import FeatureFlag, MCLIConfig


def add_util_argparser(subparser: argparse._SubParsersAction,):
    """Adds the util parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    conf = MCLIConfig.load_config(safe=True)

    util_parser: argparse.ArgumentParser = subparser.add_parser(
        'util',
        aliases=['utilization'],
        help='Get cluster utilization',
    )

    util_parser.add_argument(
        'clusters',
        help='Which cluster would you like to get utilization for?',
        nargs='*',
    )

    if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
        # pylint: disable-next=import-outside-toplevel
        from mcli.cli.m_util.util import get_util

        util_parser.add_argument(
            '--hide-users',
            action='store_true',
            help='Do not show the by user utilization breakdown',
        )

    else:
        # pylint: disable-next=import-outside-toplevel
        from mcli.cli.m_util.kube_util import get_util
    util_parser.set_defaults(func=get_util)
    return util_parser
