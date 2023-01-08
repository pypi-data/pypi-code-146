import json
import logging
from inspect import stack

import click
from click import BadParameter

from com.enovation.helper.click.python_literal_argument_and_option import PythonLiteralArgument

_logger: logging.Logger = logging.getLogger(__name__)


@click.command('dict-load-json')
@click.pass_context
@click.argument('file', type=click.Path(exists=True))
@click.argument('alias', type=str, default='json')
def dict_load_json(ctx_context, file, alias):
    """
    Load json file into a dictionary that is labelled using an alias for later use.

    :param alias: name given to the dictionary being loaded, so it can be used later on by other commands.
    :param ctx_context: Click context.
    :param file: json file to load
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias in ctx_context.obj:
        _logger.warning(
            f"Warning: another object with alias '{alias}' already exists, of type {type(alias)}. This data "
            f"will be overridden with the 'json' file '{file}'."
        )

    # We load the json
    with open(file, 'r') as json_file:
        _dict_the_file: dict = json.load(json_file)

    _logger.info(f"json file read as a dictionary containing '{len(_dict_the_file)}' records.")

    # We update the context data store
    ctx_context.obj[alias] = _dict_the_file
    ctx_context.obj["_" + alias] = {
        "path": file,
        "src": "dict_load_json"
    }

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")


@click.command('dict-set-json')
@click.pass_context
@click.argument('dictionary', cls=PythonLiteralArgument, type=dict, default={})
@click.argument('alias', type=str, default={})
def dict_set_json(ctx_context, dictionary, alias):
    """
    Set a DICTIONARY provided as  as an argument as an ALIAS that can be later accessed from other commands
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias in ctx_context.obj:
        _logger.warning(
            f"Warning: another object with alias '{alias}' already exists, of type {type(alias)}. This data "
            f"will be overridden with the 'dictionary' value '{dictionary}'."
        )

    # We update the context data store
    ctx_context.obj[alias] = dictionary
    ctx_context.obj["_" + alias] = {
        "src": "dict_set_json"
    }

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")


@click.command('dict-modif')
@click.pass_context
@click.argument('alias', type=str)
@click.argument('delta', cls=PythonLiteralArgument, type=dict, default={})
def dict_modif(ctx_context, alias, delta):
    """
    Modify the ALIAS dictionary from the context using a DELTA dictionary.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias not in ctx_context.obj:
        raise BadParameter(
            message=f"No object with alias '{alias}' exists in the context. Cannot do any magic here!",
            param_hint=f"Ensure you effectively loaded a dictionary in the context, with alias '{alias}', before "
                       f"trying to modify it.",
            ctx=ctx_context
        )

    _alias_object = ctx_context.obj[alias]

    if not isinstance(_alias_object, dict):
        raise BadParameter(
            message=f"Object with alias '{alias}' in context is of type '{type(_alias_object)}', while 'dict' is "
                    f"expected.",
            param_hint=f"Ensure you effectively try to modify an object in the context which is of type 'dict'.",
            ctx=ctx_context
        )

    _alias_dict: dict = _alias_object

    _alias_dict.update(delta)

    # We update the context data store
    ctx_context.obj[alias] = _alias_dict
    ctx_context.obj["_" + alias] = {
        "src": "dict_modif"
    }

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
