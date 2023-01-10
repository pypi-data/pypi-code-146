""" m init Entrypoint"""
import logging
import textwrap
from typing import Optional

from mcli import config
from mcli.api.exceptions import MCLIConfigError
from mcli.cli.m_set_unset.api_key import set_api_key
from mcli.config import FeatureFlag, MCLIConfig
from mcli.utils.utils_interactive import choose_one, input_disabled
from mcli.utils.utils_logging import FAIL, INFO, OK

logger = logging.getLogger(__name__)


def initialize_mcli_config() -> MCLIConfig:
    """Initialize the MCLI config directory and file, if necessary

    Returns:
        True if MCLI needed to be initialized. False if initialization was already done.
    """

    if not config.MCLI_CONFIG_DIR.exists():
        config.MCLI_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug(f'{OK} Created MCLI config directory')
    else:
        logger.debug(f'{OK} MCLI config directory already exists')

    # Generate MCLI Config if not existing
    try:
        mcli_config = MCLIConfig.load_config()
        logger.debug(f'{OK} MCLI config file already exists')
    except MCLIConfigError:
        mcli_config = MCLIConfig.empty()
        mcli_config.save_config()
        logger.debug(f'{OK} Created new MCLI config file')

    return mcli_config


def initialize_mcli(
    mcloud_mode: Optional[bool] = None,
    no_input: bool = False,
    **kwargs,
) -> int:
    del kwargs

    welcome = """
    ------------------------------------------------------
    Welcome to the MosaicML CLI (MCLI)
    ------------------------------------------------------
    """
    if mcloud_mode is None and no_input:
        logger.error(f'{FAIL} All required arguments not provided but cannot query user input. '
                     'Please provide --mcloud or --legacy if you want to provide --no-input')
        return 1

    logger.info(textwrap.dedent(welcome))

    conf = initialize_mcli_config()
    logger.info(f'{OK} Config file initialized at [cyan]{config.MCLI_CONFIG_PATH}[/]')

    # If user isn't on mcloud, ask if they should be
    if mcloud_mode is None:
        if not conf.feature_enabled(FeatureFlag.USE_MCLOUD):
            logger.info(f'{INFO} Your administrator should have set you up to use either '
                        '[bright_blue bold]"Legacy"[/] clusters or [green bold]"MCloud"[/] clusters')
            with input_disabled(no_input):
                mcloud_mode = choose_one('Which would you like to setup?', ['MCloud', 'Legacy']) == 'MCloud'

    if mcloud_mode is True:
        conf.feature_flags[FeatureFlag.USE_MCLOUD.value] = True
        conf.save_config()

    logger.info('')

    if conf.feature_enabled(FeatureFlag.USE_MCLOUD):
        first_setup = """
        To setup access, first create your API key at: [green bold]https://cloud.mosaicml.com[/].
        Then, provide your credentials to mcli with:

        [bold]mcli set api-key <value>[/]
        """
    else:
        first_setup = """
        To setup your cluster access, run:

        [bold]mcli init-kube[/]

        And get started launching your runs.

        For more information see the docs at:
        https://mcli.docs.mosaicml.com/getting_started/installation.html#configuring-kubernetes
        """

    logger.info(textwrap.dedent(first_setup).lstrip())
    logger.info('')

    next_steps = """

    For next steps, follow the "Getting Started" section at
    [green bold]https://mcli.docs.mosaicml.com[/] to:

    * [cyan]Quick Start[/] - Run the Hello World example
    * [cyan]First Model[/] - Train your first 1-Billion parameter Language Model
    * [cyan]Environment Setup[/] - Set up your git, docker, and other API keys
    * [cyan]Common Commands[/] - Typical commands for users of MosaicML Cloud

    The MosaicML CLI can also be navigated with:

    [bold]mcli --help[/]

    """

    logger.info(textwrap.dedent(next_steps).lstrip())
    logger.info('')

    return 0


def initialize(api_key: Optional[str] = None):
    """Initialize the MosaicML Cloud

    Arguments:
        api_key: Optional value to set
    """
    initialize_mcli(mcloud_mode=True, no_input=True)

    if api_key:
        set_api_key(api_key)
