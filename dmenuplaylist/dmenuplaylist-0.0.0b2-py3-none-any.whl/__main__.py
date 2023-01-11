#!/usr/bin/env python3
import sys

from .config import NoBaseDir, NoBaseDirExists, get_user_settings
from .options import get_opts
from .utils import add_files, delete_item, display_playlist, delete_item, remove_item


__license__ = "GPL-v3.0"
__program__ = "dmenuplaylist"


def process_opts(user, args):
    """
    Opts handler for main
    """
    if args.add is not None:
        return add_files(user=user, add=args.add)
    elif args.delete is not None:
        return delete_item(user=user, item=args.delete)
    elif args.list:
        return display_playlist(user=user)
    elif args.remove:
        return remove_item(user=user)
    else:
        return display_playlist(user=user, ask=False)


def main():
    """
    Command line application to view and track media
    """
    # Set and get command line args
    args = get_opts(__program__)

    try:
        # Creates a UserSettings object. This will be used by various function
        # to access file paths, settings, filters, and command line args
        user, args = get_user_settings(program=__program__, args=args)
    except (NoBaseDir, NoBaseDirExists) as err:
        print(err, file=sys.stderr)
        return 1

    # Execute the appropriate function based on command line options
    return process_opts(user, args=args)


if __name__ == "__main__":
    sys.exit(main())
