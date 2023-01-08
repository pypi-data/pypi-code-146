from inspect import stack

import click
from click import BadParameter
from pandas import DataFrame
import logging

from com.enovation.helper.click.python_literal_argument_and_option import PythonLiteralArgument, PythonLiteralOption
from com.enovation.helper.pandas_dataframe_sampler import PandasDataframeSampler

_logger: logging.Logger = logging.getLogger(__name__)


@click.command('df-rename-columns')
@click.pass_context
@click.argument('alias-in', type=str)
@click.argument('dictionary', type=list, cls=PythonLiteralArgument)
@click.option('-o', '--alias-out', help="Resulting dataframe.", type=str)
def df_rename_columns(ctx_context, alias_in, dictionary, alias_out):
    """
    Rename dataframe columns.

    :param ctx_context: Click context.
    :param alias_in: dataframe to lad from the context, so its columns can be renamed.
    :param dictionary: dictionary to rename columns, in the form '{"col1":"new col1", ... , "col-x":"new col-x"}'.
    :param alias_out: alias to the cleansed dataframe, in case source dataframe should not be altered.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot rename columns from '{alias_in}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively have a dataframe labelled '{alias_in}' loaded in context.",
            ctx=ctx_context
        )
    if alias_out in ctx_context.obj:
        _logger.warning(
            f"Warning: another object with alias '{alias_out}' already exists, of type {type(alias_out)}. This data "
            f"will be overridden."
        )

    df_the_input: DataFrame = ctx_context.obj[alias_in]

    if not isinstance(df_the_input, DataFrame):
        raise BadParameter(
            message=f"Cannot rename columns from '{alias_in}', as this alias is of type '{type(df_the_input)}' while "
                    f"'DataFrame' is expected.",
            param_hint=f"Ensure you effectively assigned a DataFrame to the alias '{alias_in}'.",
            ctx=ctx_context
        )

    # JSG, as of 28-Oct-2021: introduced PythonLiteralArgument
    # So the below is not required anymore...
    # try:
    #     dict_the_dictionary: dict = json.loads(dictionary)
    # except json.decoder.JSONDecodeError as error:
    #     raise BadParameter(
    #         message=f"Cannot transform '{dictionary}' as a dictionary to rename columns.",
    #         param_hint=f"Ensure you effectively provided a string with 'key':'value' assignment that can be used to "
    #                    f"rename columns.",
    #         ctx=ctx_context
    #     ) from error

    # We check the dictionary is a simple set of key:value assignments
    lst_the_errors: list = [
        "'"+k+"'" for k, v in dictionary.items()
        if (
            (not isinstance(k, str))
            | (not isinstance(v, str))
        )
    ]
    if len(lst_the_errors):
        raise BadParameter(
            message=f"Cannot use '{dictionary}' as a dictionary to rename columns.",
            param_hint=f"Ensure you effectively provided a string with simple 'key as string':'value as string' "
                       f"assignment that can be used to rename columns.",
            ctx=ctx_context
        )

    # We check the dictionary only provides keys that effectively exist as columns
    lst_the_errors: list = list({k for k in dictionary}-set(df_the_input.columns))
    if len(lst_the_errors) > 0:
        raise BadParameter(
            message=f"Columns '{', '.join(lst_the_errors)}' are to be renamed, but they do not exist in the dataframe.",
            param_hint=f"Ensure you effectively provide columns to rename that exist in the dataframe.",
            ctx=ctx_context
        )

    df_the_return: DataFrame = df_the_input.rename(columns=dictionary)

    # We refresh the context data store
    if alias_out:
        ctx_context.obj[alias_out] = df_the_return
    else:
        ctx_context.obj[alias_in] = df_the_return

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")


@click.command('df-cleanse-null')
@click.pass_context
@click.argument('alias-in', type=str)
@click.option('-c', '--columns', type=list, cls=PythonLiteralOption, default=None,
              help="The columns to screen for null values.")
@click.option('-v', '--value', help="Value to replace null.", type=str)
@click.option('-o', '--alias-out', help="Resulting dataframe.", type=str)
def df_cleanse_null(ctx_context, alias_in, columns, value, alias_out):
    """
    Cleanses null values from the dataframe:
    - In case VALUE is not set, we drop the rows, or we replace null values with VALUE
    - In case COLUMNS is not set, we process all columns from the dataframe, or we only process the columns listed.
    """
    _logger.info(f"\n"
                 f"\n**************************************************************************************************"
                 f"\n**************************************************************************************************"
                 f"\nCommand mx-sp-pp-load-history called with parameters:"
                 f"\n\t- alias-in: {alias_in}"
                 # f"\n\t- columns: {', '.join(columns)}"
                 f"\n\t- value: {value}"
                 f"\n\t- alias-out: {alias_out}")

    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot cleanse '{alias_in}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively loaded some data, and labelled these with the alias '{alias_in}'.",
            ctx=ctx_context
        )

    if not isinstance(ctx_context.obj[alias_in], DataFrame):
        raise BadParameter(
            message=f"Cannot cleanse '{alias_in}', as this alias is of type '{type(ctx_context.obj[alias_in])}' while "
                    f"'DataFrame' is expected.",
            param_hint=f"Ensure you effectively used operands to generate data as a DataFrame.",
            ctx=ctx_context
        )

    if alias_out in ctx_context.obj:
        _logger.warning(
            f"Warning: another object with alias '{alias_out}' already exists, of type {type(alias_out)}. This data "
            f"will be overridden."
        )

    df_the_measures = ctx_context.obj[alias_in]

    # If the columns are not listed
    if columns is None:
        columns = list(df_the_measures.columns)

    for i_col in columns:
        if i_col not in df_the_measures.columns:
            raise Exception(f"The command cleanse_null_values cannot access column '{i_col}'. First, ensure this "
                            f"column effectively exists (aka. present among the columns of a loaded file, or present "
                            f"among generated data by a command), then call this function to cleanse null values.")

        if value:
            df_the_measures = df_the_measures[i_col].fillna(value)
        else:
            df_the_measures = df_the_measures[df_the_measures[i_col].notna()]
            _logger.info(f"Rows containing null value in column '{i_col}' deleted, shape '{df_the_measures.shape}'.")

    # We refresh the context data store
    if alias_out:
        ctx_context.obj[alias_out] = df_the_measures
    else:
        ctx_context.obj[alias_in] = df_the_measures

    _logger.info(f"\nCommand df-cleanse-null is returning, after having enriched the context with:"
                 f"\n\t- '{alias_out}' dataframe: {df_the_measures.shape}"
                 f"\n\t- containing columns: {', '.join(df_the_measures.columns)}"
                 f"\n**************************************************************************************************"
                 f"\n**************************************************************************************************"
                 f"\n"
                 )


@click.option('-k', '--key-columns', type=list, cls=PythonLiteralOption, default='[]',
              help="Columns labels to isolate independent universes.")
@click.option('-r', '--ordering-columns', type=list, cls=PythonLiteralOption, default='[]',
              help="Columns labels to order the dataframe, before comparing rows in the right order.")
@click.option('-v', '--value-columns', type=list, cls=PythonLiteralOption, default=None,
              help="Columns labels to compare rows, and identify duplicates to drop.")
@click.option('--keep-last/--no-keep-last', type=bool, default=False,
              help='Whether or not we keep the last record, even if duplicate with previous rows.')
@click.argument('alias-in', type=str)
@click.option('-o', '--alias-out', help="Resulting dataframe.", type=str)
@click.command('df-compress')
@click.pass_context
def df_compress(ctx_context, alias_in, alias_out, key_columns, ordering_columns, value_columns, keep_last):
    """
    The function screens the rows from Dataframe ALIAS-IN, universe by universe as defined from KEY-COLUMNS, with
    rows ordered by ORDERING-COLUMNS, and will drop all rows that have all VALUE-COLUMNS identical.

    If argument b_keep_last is set to True, the very last record of each universe is kept, even if it is a duplicate
    with a previous row.

    Several business rules are checked:
    - BR_001, dataframe expected not to contain several columns with the same label
    - BR_002, all columns from lst_key_columns expected to be in the dataframe
    - BR_003, all columns from lst_value_columns expected to be in the dataframe
    - BR_004, all columns from lst_ordering_columns expected to be in the dataframe
    - BR_005, all columns from dataframe should be listed into one of the list: key, value or ordering
    - BR_006, dataframe expected not to contain any duplicate across the ordering columns (within the same universe)
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot rename columns from '{alias_in}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively have a dataframe labelled '{alias_in}' loaded in context.",
            ctx=ctx_context
        )
    if alias_out in ctx_context.obj:
        _logger.warning(
            f"Warning: another object with alias '{alias_out}' already exists, of type {type(alias_out)}. This data "
            f"will be overridden."
        )

    df_the_input: DataFrame = ctx_context.obj[alias_in]

    if not isinstance(df_the_input, DataFrame):
        raise BadParameter(
            message=f"Cannot rename columns from '{alias_in}', as this alias is of type '{type(df_the_input)}' while "
                    f"'DataFrame' is expected.",
            param_hint=f"Ensure you effectively assigned a DataFrame to the alias '{alias_in}'.",
            ctx=ctx_context
        )

    df_the_return: DataFrame = PandasDataframeSampler.compress(
        df_measures=df_the_input,
        lst_key_columns=key_columns,
        lst_value_columns=value_columns,
        lst_ordering_columns=ordering_columns,
        b_keep_last=keep_last,
    )
    _logger.info(f"After dropping duplicates, dataframe is '{df_the_return.shape}'.")

    # We refresh the context data store
    if alias_out:
        ctx_context.obj[alias_out] = df_the_return
    else:
        ctx_context.obj[alias_in] = df_the_return

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
