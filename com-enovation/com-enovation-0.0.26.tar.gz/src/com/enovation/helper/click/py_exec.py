from inspect import stack

import click
from click import BadParameter
import logging

_logger: logging.Logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
@click.command('py-exec-file')
@click.pass_context
@click.argument('file', type=click.Path(exists=True))
def py_exec_file(ctx_context, file):
    """
    Load the content of FILE as text, and execute it.

    Raises BadParameter exception in case:
     - The file cannot be read a text
     - The text cannot be executed.

    :param ctx_context:
    :param file: text file to load the python code from
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    try:
        with open(file, 'r') as _io_the_file:
            _lst_the_lines: list[str] = _io_the_file.readlines()
    except Exception as _the_exception:
        raise BadParameter(f"Exception thrown from function '{stack()[0].filename} - {stack()[0].function}'.") \
            from _the_exception

    try:
        exec("\n".join(_lst_the_lines))
    except Exception as _the_exception:
        raise BadParameter(f"Exception thrown from function '{stack()[0].filename} - {stack()[0].function}'.") \
            from _the_exception

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
