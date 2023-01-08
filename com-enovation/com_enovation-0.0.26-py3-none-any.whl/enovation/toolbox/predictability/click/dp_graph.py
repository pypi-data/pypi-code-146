import logging
from inspect import stack

import click
from click import BadParameter

from com.enovation.toolbox.predictability.bean import PredictabilityBean
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher import DpGrapher_DashApplication

_logger: logging.Logger = logging.getLogger(__name__)


@click.command('dp-graph')
@click.pass_context
@click.argument('alias', type=str)
def dp_graph_to_dash_date_predictability(ctx_context, alias):
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot graph '{alias}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively computed a date predictability bean, and labelled it with the alias "
                       f"'{alias}'.",
            ctx=ctx_context
        )

    if not isinstance(ctx_context.obj[alias], PredictabilityBean):
        raise BadParameter(
            message=f"Cannot graph '{alias}', as this alias is of type '{type(ctx_context.obj[alias])}' while "
                    f"'PredictabilityBean' is expected.",
            param_hint=f"Ensure you effectively provide an instance of 'PredictabilityBean' to graph.",
            ctx=ctx_context
        )

    obj_the_data: PredictabilityBean = ctx_context.obj[alias]

    DpGrapher_DashApplication(obj_predictability=obj_the_data).graph_predictability()

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
