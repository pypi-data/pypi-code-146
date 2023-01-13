"""Dicom Importer Module"""
from .. import util
from ..importers import DicomScannerImporter


def add_command(subparsers, parents):
    """Add dicom import commands"""
    parser = subparsers.add_parser(
        "dicom", parents=parents, help="Import a folder of dicom files"
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

    parser.set_defaults(func=import_dicoms)
    parser.set_defaults(parser=parser)

    return parser


def import_dicoms(args):
    """Import dicoms"""
    if args.config.output_folder is None:
        util.get_sdk_client_for_current_user().is_logged_in()

    # Build the importer instance
    importer = DicomScannerImporter(
        group=args.group,
        project=args.project,
        config=args.config,
        subject_label=args.subject,
        session_label=args.session,
    )
    # Perform the import
    importer.interactive_import(args.folder)
