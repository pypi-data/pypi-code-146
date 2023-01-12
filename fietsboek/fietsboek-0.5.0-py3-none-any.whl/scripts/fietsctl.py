"""Script to do maintenance work on a Fietsboek instance."""
# pylint: disable=consider-using-f-string,unused-argument
import argparse
import getpass
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy import select

from .. import __VERSION__, models

EXIT_OKAY = 0
EXIT_FAILURE = 1


def cmd_useradd(env, args):
    """Create a new user.

    This user creation bypasses the "enable_account_registration" setting. It
    also immediately sets the new user's account to being verified.

    If email, name or password are not given as command line arguments, they
    will be asked for interactively.

    On success, the created user's unique ID will be printed.

    Note that this function does less input validation and should therefore be used with care!
    """
    email = args.email
    if not email:
        email = input("Email address: ")
    name = args.name
    if not name:
        name = input("Name: ")
    password = args.password
    if not password:
        password = getpass.getpass()

    # The UNIQUE constraint only prevents identical emails from being inserted,
    # but does not take into account the case insensitivity. The least we
    # should do here to not brick log ins for the user is to check if the email
    # already exists.
    query = models.User.query_by_email(email)
    with env["request"].tm:
        result = env["request"].dbsession.execute(query).scalar_one_or_none()
        if result is not None:
            print("Error: The given email already exists!", file=sys.stderr)
            return EXIT_FAILURE

    user = models.User(name=name, email=email, is_verified=True, is_admin=args.admin)
    user.set_password(password)

    with env["request"].tm:
        dbsession = env["request"].dbsession
        dbsession.add(user)
        dbsession.flush()
        user_id = user.id

    print(user_id)
    return EXIT_OKAY


def cmd_userdel(env, args):
    """Delete a user.

    This command deletes the user's account as well as any tracks associated
    with it.

    This command is destructive and irreversibly deletes data.
    """
    if args.id:
        query = select(models.User).filter_by(id=args.id)
    else:
        query = models.User.query_by_email(args.email)
    with env["request"].tm:
        dbsession = env["request"].dbsession
        user = dbsession.execute(query).scalar_one_or_none()
        if user is None:
            print("Error: No such user found.", file=sys.stderr)
            return EXIT_FAILURE
        print(user.name)
        print(user.email)
        if not args.force:
            query = input("Really delete this user? [y/N] ")
            if query not in {"Y", "y"}:
                print("Aborted by user.")
                return EXIT_FAILURE
        dbsession.delete(user)
        print("User deleted")
        return EXIT_OKAY


def cmd_userlist(env, args):
    """Prints a listing of all user accounts.

    The format is::

        [av] {ID} - {email} - {Name}

    with one line per user. The 'a' is added for admin accounts, the 'v' is added
    for verified users.
    """
    with env["request"].tm:
        dbsession = env["request"].dbsession
        users = dbsession.execute(select(models.User).order_by(models.User.id)).scalars()
        for user in users:
            tag = "[{}{}]".format(
                "a" if user.is_admin else "-",
                "v" if user.is_verified else "-",
            )
            print(f"{tag} {user.id} - {user.email} - {user.name}")
    return EXIT_OKAY


def cmd_passwd(env, args):
    """Change the password of a user."""
    if args.id:
        query = select(models.User).filter_by(id=args.id)
    else:
        query = models.User.query_by_email(args.email)
    with env["request"].tm:
        dbsession = env["request"].dbsession
        user = dbsession.execute(query).scalar_one_or_none()
        if user is None:
            print("Error: No such user found.", file=sys.stderr)
            return EXIT_FAILURE
        password = args.password
        if not password:
            password = getpass.getpass()
            repeat = getpass.getpass("Repeat password: ")
            if password != repeat:
                print("Error: Mismatched passwords.")
                return EXIT_FAILURE

        user.set_password(password)
        print(f"Changed password of {user.name} ({user.email})")
        return EXIT_OKAY


def cmd_version():
    """Show the installed fietsboek version."""
    name = __name__.split(".", 1)[0]
    print(f"{name} {__VERSION__}")


def parse_args(argv):
    """Parse the given args.

    :param argv: List of arguments.
    :type argv: list[str]
    :return: The parsed arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c",
        "--config",
        dest="config_uri",
        help="configuration file, e.g., development.ini",
    )

    subparsers = parser.add_subparsers(help="available subcommands", required=True)

    p_version = subparsers.add_parser(
        "version",
        help="show the version",
        description=cmd_version.__doc__,
    )
    p_version.set_defaults(func=cmd_version)

    p_useradd = subparsers.add_parser(
        "useradd",
        help="create a new user",
        description=cmd_useradd.__doc__,
    )
    p_useradd.add_argument(
        "--email",
        help="email address of the user",
    )
    p_useradd.add_argument(
        "--name",
        help="name of the user",
    )
    p_useradd.add_argument(
        "--password",
        help="password of the user",
    )
    p_useradd.add_argument(
        "--admin",
        action="store_true",
        help="make the new user an admin",
    )
    p_useradd.set_defaults(func=cmd_useradd)

    p_userdel = subparsers.add_parser(
        "userdel",
        help="delete a user account",
        description=cmd_userdel.__doc__,
    )
    p_userdel.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="override the safety check",
    )
    group = p_userdel.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--id",
        "-i",
        type=int,
        help="database ID of the user",
    )
    group.add_argument(
        "--email",
        "-e",
        help="email of the user",
    )
    p_userdel.set_defaults(func=cmd_userdel)

    p_userlist = subparsers.add_parser(
        "userlist",
        help="list user accounts",
        description=cmd_userlist.__doc__,
    )
    p_userlist.set_defaults(func=cmd_userlist)

    p_passwd = subparsers.add_parser(
        "passwd",
        help="change user password",
        description=cmd_passwd.__doc__,
    )
    p_passwd.add_argument(
        "--password",
        help="password of the user",
    )
    group = p_passwd.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--id",
        "-i",
        type=int,
        help="database ID of the user",
    )
    group.add_argument(
        "--email",
        "-e",
        help="email of the user",
    )
    p_passwd.set_defaults(func=cmd_passwd)

    return parser.parse_args(argv[1:]), parser


def main(argv=None):
    """Main entry point."""
    if argv is None:
        argv = sys.argv
    args, parser = parse_args(argv)

    if args.func == cmd_version:  # pylint: disable=comparison-with-callable
        cmd_version()
        sys.exit(EXIT_OKAY)

    if not args.config_uri:
        parser.error("the following arguments are required: -c/--config")

    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    sys.exit(args.func(env, args))
