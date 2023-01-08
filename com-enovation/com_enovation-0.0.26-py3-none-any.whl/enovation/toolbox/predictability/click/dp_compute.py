import logging
from inspect import stack

import click
from click import BadParameter
from pandas import DataFrame

from com.enovation.toolbox.predictability.bean import PredictabilityBean
from com.enovation.toolbox.predictability.dp_date_predictability.dp_computer import DatePredictabilityComputer


_logger: logging.Logger = logging.getLogger(__name__)


@click.command('dp-compute')
@click.pass_context
@click.argument('alias-in', type=str)
@click.argument('alias-out', type=str)
@click.option(
    '--resample/--no-resample', type=bool, default=False,
    help='To resample daily the measures, to have better graphing.',
)
@click.option('-k', '--key', help="The key column, that will be renamed.", type=str, default=None)
@click.option('-d', '--date', help="The date column, that will be renamed.", type=str, default=None)
@click.option('-m', '--measure', help="The measure column, that will be renamed.", type=str, default=None)
def dp_compute_date_predictability(ctx_context, alias_in, alias_out, resample, key, date, measure):
    """
    Compute date predictability for a dataframe that is to contain 3 columns, and 3 columns only:
    - One column named DatePredictabilityComputer.str__input__column_label__key, aka "key"
    - One column named DatePredictabilityComputer.str__input__column_label__date, aka "date"
    - One column named DatePredictabilityComputer.str__input__column_label__measure, aka "measure".

    The following business rules are checked:
    - BR_001, ALIAS_IN should exist in context
    - BR_002, ALIAS_IN should be a dataframe
    - BR_003, ALIAS_OUT exists in context --> Warning

    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    # BR_001, ALIAS_IN should exist in context
    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"BR_001, no object labelled '{alias_in}' could be found in context, which is not expected.",
            param_hint=f"BR_001, ensure you effectively have an object labelled '{alias_in}' in context.",
            ctx=ctx_context
        )

    # BR_002, ALIAS_IN should be a dataframe
    if not isinstance(ctx_context.obj[alias_in], DataFrame):
        raise BadParameter(
            message=f"BR_002, object labelled '{alias_in}' is of type '{type(ctx_context.obj[alias_in])}', which is not"
                    f" expected.",
            param_hint=f"Ensure to provide an 'DataFrame' instance.",
            ctx=ctx_context
        )

    # BR_003, ALIAS_OUT exists in context --> Warning
    if alias_out in ctx_context.obj:
        _logger.warning(
            f"BR_006, warning: another object with alias '{alias_out}' already exists, of type "
            f"'{type(ctx_context.obj[alias_in])}'. This data will be overridden."
        )

    df_the_input: DataFrame = ctx_context.obj[alias_in]

    if key is not None:
        df_the_input = df_the_input.rename(columns={key: DatePredictabilityComputer.str__input__column_label__key})
    if date is not None:
        df_the_input = df_the_input.rename(columns={date: DatePredictabilityComputer.str__input__column_label__date})
    if measure is not None:
        df_the_input = df_the_input.rename(
            columns={measure: DatePredictabilityComputer.str__input__column_label__measure})

    obj_the_computer: DatePredictabilityComputer = DatePredictabilityComputer()

    obj_the_bean: PredictabilityBean = obj_the_computer.compute_historical_date_predictability(
        df_measures=df_the_input,
        b_resample=resample
    )

    # We refresh the context data store
    if alias_out:
        ctx_context.obj[alias_out] = obj_the_bean
    else:
        ctx_context.obj[alias_in] = obj_the_bean

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
