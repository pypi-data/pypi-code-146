"""Import Parrec Module"""
from .. import util
from ..importers import ParRecScannerImporter


def add_command(subparsers, parents):
    """Add parrec import commands"""
    parser = subparsers.add_parser(
        "parrec", parents=parents, help="Import a folder of parrec files"
    )
    parser.add_argument("folder", help="The path to the folder to import")
    parser.add_argument(
        "group", metavar="group_id", help="The id of the group", type=util.group_id
    )
    parser.add_argument(
        "project", metavar="project_label", help="The label of the project"
    )

    parser.add_argument(
        "--subject",
        metavar="subject_label",
        help="Override value for the subject label",
    )
    parser.add_argument(
        "--session",
        metavar="session_label",
        help="Override value for the session label",
    )

    parser.set_defaults(func=import_parrec)
    parser.set_defaults(parser=parser)

    return parser


def import_parrec(args):
    """Parrec import"""
    if args.config.output_folder is None:
        util.get_sdk_client_for_current_user().is_logged_in()

    # Build the importer instance
    importer = ParRecScannerImporter(
        group=args.group,
        project=args.project,
        config=args.config,
        subject_label=args.subject,
        session_label=args.session,
    )

    # Perform the import
    importer.interactive_import(args.folder)
