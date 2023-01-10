""" mcli unset Entrypoint """
import argparse

from mcli.cli.m_use.m_use import use_feature_flag


def unset_entrypoint(**kwargs):
    del kwargs
    mock_parser = configure_argparser(parser=argparse.ArgumentParser())
    mock_parser.print_help()
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=unset_entrypoint)

    feature_parser = subparsers.add_parser('feature', help='Deactivate a feature flag')
    feature_parser.add_argument('feature', nargs='?', help='The name of the feature flag')
    feature_parser.set_defaults(func=use_feature_flag, activate=False)

    return parser


def add_unset_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the unset parser to a subparser

    Args:
        subparser: the Subparser to add the Use parser to
    """
    unset_parser: argparse.ArgumentParser = subparser.add_parser(
        'unset',
        help='Unset local configuration variables',
    )
    unset_parser = configure_argparser(parser=unset_parser)
    return unset_parser
