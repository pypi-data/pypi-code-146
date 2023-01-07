import argparse
import signal
from argcomplete import autocomplete

from zbus_cli.command import add_subparsers_on_demand

addr = {
    "pub": "ipc:///tmp/frontend",
    "sub": "ipc:///tmp/backend",
    "client": "ipc:///tmp/cvte_majordomo_broker_client"
}


def main(*, script_name='zbus', argv=None, description=None, extension=None):
    if description is None:
        description = f'{script_name} is an extensible command-line tool ' \
            'for ZBUS.'

    # top level parser
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # add arguments for command extension(s)

    # get command entry points as needed
    selected_extension_key = '_command'
    add_subparsers_on_demand(
        parser,
        script_name,
        selected_extension_key,
        'zbuscli.command',
        # hide the special commands in the help
        hide_extensions=['extension_points', 'extensions'],
        required=False,
        argv=argv)

    # register argcomplete hook if available
    autocomplete(parser, exclude=['-h', '--help'])

    # parse the command line arguments
    args = parser.parse_args(args=argv)

    if extension is None:
        # get extension identified by the passed command (if available)
        extension = getattr(args, selected_extension_key, None)

    # handle the case that no command was passed
    if extension is None:
        parser.print_help()
        return 0
    # print("args=", args)

    # call the main method of the extension
    try:
        rc = extension.main(parser=parser, args=args, addr=addr)
    except KeyboardInterrupt:
        rc = signal.SIGINT
    except RuntimeError as e:
        rc = str(e)
    return rc
