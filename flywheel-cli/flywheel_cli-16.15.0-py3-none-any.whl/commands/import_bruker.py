"""Bruker Import Module"""
from .. import util
from ..importers.bruker_scan import create_bruker_scanner


def add_command(subparsers, parents):
    """Add bruker import commands"""
    parser = subparsers.add_parser(
        "bruker", parents=parents, help="Import structured bruker data"
    )
    parser.add_argument("folder", help="The path to the folder to import")
    parser.add_argument(
        "group", metavar="group_id", help="The id of the group", type=util.group_id
    )
    parser.add_argument(
        "project", metavar="project_label", help="The label of the project"
    )

    parser.add_argument("--folder-template", help="The optional folder template")

    parser.set_defaults(func=import_bruker_folder)
    parser.set_defaults(parser=parser)

    return parser


def import_bruker_folder(args):
    """Import bruker"""
    if args.config.output_folder is None:
        util.get_sdk_client_for_current_user().is_logged_in()

    # Build the importer instance
    importer = create_bruker_scanner(
        args.group, args.project, args.config, folder_template=args.folder_template
    )

    # Perform the import
    importer.interactive_import(args.folder)
