#!/usr/bin/env python3

###
# This module implements the [C]-ommand [L]-ine [I]-nterface of ¨jinjaNG.
###


import click

from .jngbuild import *


# --------- #
# -- CLI -- #
# --------- #

###
# prototype::
#     message : this text is to indicate one error.
#
#     :action: an error message is printed, then the script exits
#              with a ``1`` error.
###
def _exit(message: str) -> None:
    print(
f"""
Try 'jinjang --help' for help.

Error: {message}
""".strip()
    )

    exit(1)


###
# prototype::
#     strpath : a path that can used quotes
#
#     :return: the string version of the path without quotes around.
###
def unquotedpath(strpath: str) -> str:
    if len(strpath) <= 2:
        return strpath

    if strpath[0] in ['"', "'"] and strpath[0] == strpath[-1]:
        strpath = strpath[1:-1]

    return strpath


###
# prototype::
#     data     : the path of the file containing the data to feed
#                the template.
#                path::``YAML``, path::``JSON``, and path::``PY``
#                files can be used.
#     template : the path of the template file.
#     output   : the path for the output built by ¨jinjaNG.
#     unsafe   : same usage as the attribut/parameter ``launch_py``
#                of the method ``jngbuild.JNGBuilder.render``,
#                :see: jngbuild.JNGBuilder.render
#     flavour  : :see: jngbuild.JNGBuilder.render
#     config   : :see: jngconfig.build_config.render
#     short    : opposite usage of the attribut/parameter ``verbose``
#                of the method ``jngbuild.JNGBuilder.render``,
#                :see: jngconfig.build_config.render
#
#     :action: :see: :see: jngbuild.JNGBuilder.render
###
@click.command(
    context_settings = dict(
        help_option_names = ['--help', '-h']
    )
)
@click.argument('data')
@click.argument('template')
@click.argument('output')
@click.option('--unsafe', '-u',
              is_flag = True,
              default = False,
              help    = '** TO USE WITH A LOT OF CAUTION! ** '
                        'This flag allows Python file to build data: use '
                        'a dictionary named ``JNGDATA`` for the Jinja '
                        'variables and their value. ')
@click.option('--flavour', '-f',
              default = AUTO_FLAVOUR,
              help    = "A flavour to use if you don't want to let "
                        'jinjaNG detect automatically the dialect '
                        'of the template. '
                        'Possible values: '
                        + ', '.join(ALL_FLAVOURS[:-1])
                        + f', or {ALL_FLAVOURS[-1]}'
                        + '.')
@click.option('--config', '-c',
              default = NO_CONFIG,
              help    = '** TO USE WITH A LOT OF CAUTION! ** '
                        'The value ``auto`` authorizes jinjaNG to use '
                        'a ``cfg.jng.yaml`` file detected automatically '
                        'relatively to the parent folder of the template. '
                        'You can also indicate the path of a specific '
                        'YAML configuration file.')
@click.option('--short', '-s',
              is_flag = True,
              default = False,
              help    = 'This flag is used to hide the output of external '
                        'commands that jinjaNG is asked to run.')

def jng_CLI(
    data    : str,
    template: str,
    output  : str,
    unsafe  : bool,
    flavour : str,
    config  : str,
    short   : bool,
) -> None:
    """
    Produce a file by filling in a Jinja template.

    DATA: the path of the file containing the data.

    TEMPLATE: the path of the template.

    OUTPUT: the path of the output built by jinjaNG.
    """
# Unsafe mode used?
    if unsafe:
        print('WARNING! Using a Python file can be dangerous.')

# Internal tag for auto config.
    if config == 'auto':
        config = AUTO_CONFIG

# Lets' work...
    mybuilder = JNGBuilder(
        flavour   = flavour,
        launch_py = unsafe,
        config    = config,
        verbose   = not short
    )

    try:
        mybuilder.render(
            data     = Path(unquotedpath(data)),
            template = Path(unquotedpath(template)),
            output   = Path(unquotedpath(output))
        )

        print(
             'File successfully built:'
             '\n'
            f'  + {output}'
        )

    except Exception as e:
        _exit(repr(e))
