import logging

import rich_click as click

from servicefoundry.cli.console import console
from servicefoundry.cli.const import COMMAND_CLS
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.io.rich_output_callback import RichOutputCallBack
from servicefoundry.lib.messages import PROMPT_POST_LOGIN
from servicefoundry.lib.session import login

logger = logging.getLogger(__name__)


@click.command(name="login", cls=COMMAND_CLS)
@click.option("--relogin", type=bool, is_flag=True, default=False)
@click.option("--host", type=str, default=None)
@click.option(
    "--api-key",
    type=str,
    default=None,
    prompt=True,
    hide_input=True,
    prompt_required=False,
)
@handle_exception_wrapper
def login_command(relogin: bool, host: str, api_key: str):
    """
    Login to servicefoundry
    """
    # TODO (chiragjn): Add support for non interactive login with API key.
    #                  It is supported indirectly as we always look for `SERVICE_FOUNDRY_API_KEY`
    #                  in the environment
    callback = RichOutputCallBack()
    login(api_key=api_key, host=host, relogin=relogin, output_hook=callback)
    console.print(PROMPT_POST_LOGIN)


def get_login_command():
    return login_command
