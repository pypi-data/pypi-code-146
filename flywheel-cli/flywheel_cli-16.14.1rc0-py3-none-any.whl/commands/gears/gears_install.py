"""Install Gear"""
import sys

from ... import util
from ...exchange import GEAR_CATEGORIES, GearExchangeDB, prepare_manifest_for_upload


def add_command(subparsers):
    """Adds gear install commands"""
    parser = subparsers.add_parser(
        "install", help="Install a gear from the Flywheel Exchange"
    )
    parser.add_argument("name", help="The name of the gear to install")
    parser.add_argument("category", choices=GEAR_CATEGORIES, help="The gear category")
    parser.add_argument("version", nargs="?", help="The version of the gear to install")

    parser.set_defaults(func=install_gear)
    parser.set_defaults(parser=parser)

    return parser


def install_gear(args):
    """Gear install"""
    db = GearExchangeDB()
    db.update()

    # Download the gear spec
    fw = util.get_sdk_client_for_current_user()

    current_gear = None

    # Get the installed gear
    for gear in fw.get_all_gears():
        name = gear.gear.name
        if not args.name or args.name == name:
            if not current_gear or gear.created > current_gear.created:
                current_gear = gear

    # Let's not get into upgrade/downgrade scenarios here
    if current_gear:
        print(
            f'{args.name} {current_gear["gear"]["version"]} is already installed, please use the upgrade command',
            file=sys.stderr,
        )
        sys.exit(1)

    search_str = args.name
    if args.version:
        search_str += " " + args.version
        pending_gear = db.find_version(args.name, args.version)
    else:
        pending_gear = db.find_latest(args.name)

    if not pending_gear:
        print(f"Could not find gear: {search_str}")
        sys.exit(1)

    # Canonical name
    gear_name = pending_gear["gear"]["name"]

    # Perform the install
    site_name = fw.get_site_name()
    if util.confirmation_prompt(
        f'Installing {gear_name} {pending_gear["gear"]["version"]} on {site_name}. Continue?'
    ):
        prepare_manifest_for_upload(pending_gear, category=args.category)
        fw.add_gear(gear_name, pending_gear)
        print("Done!")
    else:
        print("OK then.")
