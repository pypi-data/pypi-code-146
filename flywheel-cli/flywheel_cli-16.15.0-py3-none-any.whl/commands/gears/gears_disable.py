"""Disable Gears"""

from ... import util


def add_command(subparsers):
    """Adds gear search commands"""
    parser = subparsers.add_parser("disable", help="Disable gear")
    parser.add_argument("id", help="ID of the gear")
    parser.add_argument("--debug", action="store_true", help="Turn on debug logging")
    parser.set_defaults(func=disable_gear)

    return parser


def disable_gear(args):
    """Disable gear"""
    gear_id = args.id
    fw = util.get_sdk_client_for_current_user()
    fw.call_api(
        f"/gears/{gear_id}",
        "DELETE",
    )
