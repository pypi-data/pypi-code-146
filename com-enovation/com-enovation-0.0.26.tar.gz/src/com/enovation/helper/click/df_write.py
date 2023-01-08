import json

import click
from click import BadParameter
from pandas import DataFrame

from com.enovation.helper.json_encoder import JSONEncoder

import logging
from inspect import stack


_logger: logging.Logger = logging.getLogger(__name__)


@click.command('df-to-stdout')
@click.pass_context
@click.argument('alias-in', type=str)
def df_to_stdout(ctx_context, alias_in):
    """
    Print the predictabilities.

    :param ctx_context: the context
    :param alias_in: alias to a dataframe to print.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot print '{alias_in}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively loaded some data, and labelled these with the alias '{alias_in}'.",
            ctx=ctx_context
        )

    str_to_print: str = ""
    try:
        str_to_print = ctx_context.obj[alias_in].to_string()
    except Exception as exception:
        _logger.debug(f"ctx_context.obj[{alias_in}].to_string() raised an exception: "+str(exception))
        try:
            str_to_print = json.dumps(
                obj=ctx_context.obj[alias_in],
                skipkeys=True,
                cls=JSONEncoder
            )
        except BaseException as exception:
            _logger.error(f"[DBG] json.dumps(obj=ctx_context.obj[{alias_in}], skipkeys=True, cls=JSONEncoder) raised "
                          f"an exception: " + str(exception))

    if len(str_to_print) > 0:
        click.echo_via_pager(text_or_generator=str_to_print)
    else:
        click.echo("Nothing to print")

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")


@click.command('df-to-xlsx')
@click.pass_context
@click.argument('alias', type=str)
@click.argument('file', type=click.Path(exists=False))
def df_to_xlsx(ctx_context, alias, file):
    """
    Print the predictabilities.

    :param ctx_context: the context.
    :param alias: alias to a dataframe to persist.
    :param file: the file to persist.
    """
    _logger.info(f"\n"
                 f"\n**************************************************************************************************"
                 f"\n**************************************************************************************************"
                 f"\nCommand df-to-xlsx called with parameters:"
                 f"\n\t- file: {file}"
                 f"\n\t- alias: {alias}")

    if alias not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot persist '{alias}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively loaded some data, and labelled these with the alias '{alias}'.",
            ctx=ctx_context
        )

    if not isinstance(ctx_context.obj[alias], DataFrame):
        raise BadParameter(
            message=f"Cannot persist '{alias}', as this alias is of type '{type(ctx_context.obj[alias])}' while "
                    f"'DataFrame' is expected.",
            param_hint=f"Ensure you effectively used operands to generate data as a DataFrame.",
            ctx=ctx_context
        )

    df_the_data: DataFrame = ctx_context.obj[alias]

    df_the_data.to_excel(excel_writer=file)

    _logger.info(f"\nCommand df-to-xlsx is returning"
                 f"\n**************************************************************************************************"
                 f"\n**************************************************************************************************"
                 f"\n"
                 )
