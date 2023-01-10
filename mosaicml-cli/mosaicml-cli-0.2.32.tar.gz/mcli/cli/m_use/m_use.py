""" mcli use Entrypoint """
import argparse
import logging
from typing import Optional

from mcli import config
from mcli.api.exceptions import cli_error_handler
from mcli.utils.utils_interactive import choose_one
from mcli.utils.utils_logging import FAIL, OK

logger = logging.getLogger(__name__)


def use(**kwargs):
    del kwargs
    mock_parser = configure_argparser(parser=argparse.ArgumentParser())
    mock_parser.print_help()
    return 0


@cli_error_handler('mcli use feature')
def use_feature_flag(feature: Optional[str], activate: bool = True, **kwargs) -> int:
    del kwargs
    conf = config.MCLIConfig.load_config(safe=True)
    available_features = conf.mcli_mode.available_feature_flags()
    available_features_str = [x.value for x in available_features]
    feature_flag: Optional[config.FeatureFlag] = None
    if feature:
        feature = feature.upper()
        if feature not in available_features_str:
            if not available_features_str:
                logger.error(f'{FAIL} You currently do not have access to any feature flags')
            else:
                feature_list = "\n- ".join([""] + available_features_str)
                logger.error(f'{FAIL} Unable to find feature flag: {feature}\n'
                             f'Available feature flags are:{feature_list}')

            return 1
        else:
            feature_flag = config.FeatureFlag[feature]

    if feature_flag is None:
        feature_flag = choose_one(
            f'What feature would you like to {"enable" if activate else "disable"}?',
            options=available_features,
            formatter=lambda x: x.value,
        )

    assert feature_flag is not None
    if activate:
        logger.info(f'{OK} Activating Feature: {feature_flag.value}')
        feature_flag.validate_compatibility()
    else:
        logger.info(f'{OK} Deactivating Feature: {feature_flag.value}')
    conf.feature_flags[feature_flag.value] = activate
    conf.save_config()

    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=use)

    feature_parser = subparsers.add_parser('feature', help='Activate or Deactivate feature flag')
    feature_parser.add_argument('feature', nargs='?', help='The name of the Feature Flag')
    feature_parser.add_argument('--deactivate', action='store_false', dest='activate', help='Deactivate a feature flag')
    feature_parser.add_argument('--activate',
                                action='store_true',
                                default=True,
                                dest='activate',
                                help='Activate a feature flag')
    feature_parser.set_defaults(func=use_feature_flag)
    return parser


def add_use_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the use parser to a subparser

    Args:
        subparser: the Subparser to add the Use parser to
    """
    use_parser: argparse.ArgumentParser = subparser.add_parser(
        'use',
        aliases=['u'],
        help='Configure your local flags',
    )
    use_parser = configure_argparser(parser=use_parser)
    return use_parser
