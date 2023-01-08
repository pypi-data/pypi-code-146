import logging
from inspect import stack

import click
from click import BadParameter

from com.enovation.toolbox.dash.application import DashApplication

_logger: logging.Logger = logging.getLogger(__name__)


@click.command('ds-dash')
@click.pass_context
@click.argument('configuration')
def ds_dash(ctx_context, configuration):
    """
    Launch dash application according to the CONFIGURATION and consuming DATA.

    CONFIGURATION is a json file that list the widgets to load, along with all the relevant parameters, such as the
    data to get from the context
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if configuration not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot find argument '{configuration}' in context, as the dictionary configuration of the dash "
                    f"application.",
            param_hint=f"Ensure you effectively load in the context a dictionary configuration for the dash "
                       f"application to know what widgets to load, along with their parameters.",
            ctx=ctx_context
        )

    if not isinstance(ctx_context.obj[configuration], dict):
        raise BadParameter(
            message=f"Argument '{configuration}' is of type '{type(ctx_context.obj[configuration])}' while "
                    f"'dict' is expected.",
            param_hint=f"Ensure you effectively provide an argument '{configuration}' of type 'dict'.",
            ctx=ctx_context
        )

    _obj_the_dash_app: DashApplication = DashApplication().launch(
        dict_config=ctx_context.obj[configuration],
        dict_context=ctx_context.obj
    )

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
