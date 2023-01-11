"""Bids Import Module"""
import flywheel

from .. import util


def add_command(subparsers, parents):
    """Add bids import commands"""
    parser = subparsers.add_parser(
        "bids", parents=parents, help="Import a structured folder"
    )
    parser.add_argument(
        "folder", metavar="[folder]", help="The path to the folder to import"
    )
    parser.add_argument(
        "group", metavar="[group]", help="The id of the group", type=util.group_id
    )
    parser.add_argument(
        "--project", "-p", metavar="<label>", help="Label of project to import into"
    )
    parser.add_argument(
        "--subject",
        default=None,
        help="Only upload data from single subject folder (e.g. sub-01)",
    )
    parser.add_argument(
        "--session",
        default=None,
        help="Only upload data from single session folder (e.g. ses-01)",
    )

    parser.set_defaults(func=import_bids)
    parser.set_defaults(parser=parser)

    return parser


def import_bids(args):
    """Bids import"""
    import flywheel_bids.upload_bids  # pylint: disable=import-outside-toplevel

    fw = util.get_sdk_client_for_current_user()
    try:
        fw.lookup(args.group)
    except flywheel.ApiException as exc:
        if exc.status == 404:
            print(f"Group {args.group} was not found, creating...")
            group = {"_id": args.group, "label": args.group}
            fw.add_group(group)
        else:
            print(exc.detail)

    flywheel_bids.upload_bids.upload_bids(
        fw,
        args.folder,
        args.group,
        project_label=args.project,
        validate=False,
        subject_label=args.subject,
        session_label=args.session,
    )
