"""Provide register CLI command."""

import argparse
import sys

import webbrowser


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new parser for register command to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "register", help="Register for a new Steampunk Spotter user account"
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:  # pylint: disable=unused-argument
    """
    Execute callback for register command.

    :param args: Argparse arguments
    """
    register()


def register() -> None:
    """Open the browser at the registration form."""
    try:
        webbrowser.open("https://spotter.steampunk.si/register/pro-plan")
    except webbrowser.Error as e:
        print(f"Cannot open browser at the registration form: {e}")
        sys.exit(1)
