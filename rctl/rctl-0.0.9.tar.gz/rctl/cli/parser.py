import argparse
import logging

from rctl.commands import (
    get,
    put,
    repo,
)

from . import RctlParserError
logger = logging.getLogger(__name__)

COMMANDS = [
    repo,
    put,
    get,
]

def _find_parser(parser, cmd_cls):
    defaults = parser._defaults
    if not cmd_cls or cmd_cls == defaults.get("func"):
        parser.print_help()
        raise RctlParserError

    actions = parser._actions
    for action in actions:
        if not isinstance(action.choices, dict):
            # NOTE: we are only interested in subparsers
            continue
        for subparser in action.choices.values():
            _find_parser(subparser, cmd_cls)

class RctlParser(argparse.ArgumentParser):
    def error(self, message, cmd_cls=None):
        logger.error(message)
        _find_parser(self, cmd_cls)

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = "unrecognized arguments: %s"
            self.error(msg % " ".join(argv), getattr(args, "func", None))
        return args

def get_parent_parser():
    parent_parser = argparse.ArgumentParser(add_help=False)
    return parent_parser

def get_main_parser():
    parent_parser = get_parent_parser()

    # Main parser
    desc = "Data Version Control"
    parser = RctlParser(
        prog="rctl",
        description=desc,
        parents=[parent_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version='0.0.9',
        help="Show program's version.",
    )

    # Sub commands
    subparsers = parser.add_subparsers(
        title="Available Commands",
        metavar="COMMAND",
        dest="cmd",
        help="Use `rctl COMMAND --help` for command-specific help.",
    )

    from .utils import fix_subparsers

    fix_subparsers(subparsers)

    for cmd in COMMANDS:
        cmd.add_parser(subparsers, parent_parser)

    return parser