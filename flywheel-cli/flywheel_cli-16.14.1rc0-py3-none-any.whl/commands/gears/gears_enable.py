"""Enable Gears"""

from ... import util


def add_command(subparsers):
    """Adds gear search commands"""
    parser = subparsers.add_parser("enable", help="Enable gear")
    parser.add_argument("id", help="ID of the gear")
    parser.add_argument("--debug", action="store_true", help="Turn on debug logging")
    parser.set_defaults(func=enable_gear)

    return parser


def enable_gear(args):
    """Enable gear"""
    gear_id = args.id
    fw = util.get_sdk_client_for_current_user()
    fw.call_api(
        f"/gears/{gear_id}/enable",
        "POST",
    )
