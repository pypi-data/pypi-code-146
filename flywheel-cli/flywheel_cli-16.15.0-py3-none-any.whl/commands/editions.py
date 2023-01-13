"""Enable/disable  edition on group oo project

examples:
  fw admin edition enable lab --group 1234
  fw admin edition disable lab --project deadc0dedeadc0dedeadc0de
"""
import logging

from .. import util

log = logging.getLogger(__name__)


def add_enable_command(subparsers, parents):
    """
    Adds enable command to the edition parser
    """
    parse_enable = subparsers.add_parser(
        "enable", help="Enable an edition", parents=parents
    )
    parse_enable.set_defaults(func=enable_edition)
    _add_edition_types(parse_enable, parents=parents)
    return parse_enable


def add_disable_command(subparsers, parents):
    """
    Adds disable command to the edition parser
    """
    parse_disable = subparsers.add_parser(
        "disable", help="Disable an edition", parents=parents
    )
    parse_disable.set_defaults(func=disable_edition)
    _add_edition_types(parse_disable, parents=parents)
    return parse_disable


def _add_edition_types(parser, parents):
    """
    Creates a subparser that can be filled with additional parsers as editions are added
    """
    edition_subparsers = parser.add_subparsers(
        title="Available editions", metavar="", dest="edition"
    )
    _add_lab_command(edition_subparsers, parents=parents)
    return edition_subparsers


def _add_lab_command(subparsers, parents):
    """
    Adds lab to the edition parsers.
    """

    parser_lab = subparsers.add_parser("lab", help="Lab edition", parents=parents)
    mutex = parser_lab.add_mutually_exclusive_group(required=True)
    mutex.add_argument("--project", required=False, help="Id of project")
    mutex.add_argument("--group", required=False, help="Id of group")


def enable_edition(args):
    """Enable an edition on a group or project"""
    _process_edition(args, True)


def disable_edition(args):
    """Disable an edition on a group or project"""
    _process_edition(args, False)


def _process_edition(args, action=False):
    """
    Updates the project/group with the edition preserving existing settings
    """
    fw = util.get_sdk_client_for_current_user()

    if hasattr(args, "group") and args.group is not None:
        cur_cont = fw.get_group(args.group)
    elif hasattr(args, "project") and args.project is not None:
        cur_cont = fw.get_project(args.project)

    # For some reason empty editions are set to None not {} from the SDK
    editions = cur_cont.get("editions", {})
    if editions is None:
        editions = {}
    data = {"editions": editions}
    data["editions"][args.edition] = action

    if hasattr(args, "group") and args.group is not None:
        fw.modify_group(args.group, data)
    elif hasattr(args, "project") and args.project is not None:
        fw.modify_project(args.project, data)
