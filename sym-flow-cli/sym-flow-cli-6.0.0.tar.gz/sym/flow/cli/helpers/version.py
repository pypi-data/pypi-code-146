from typing import Optional

import requests
from semver import VersionInfo
from sentry_sdk import capture_exception

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.version import __version__

from .constants import CLI_PACKAGE_NAME


def get_current_version() -> VersionInfo:
    """Returns the current version of the CLI."""

    try:
        return VersionInfo.parse(__version__)
    except ValueError as e:
        # Log the error in Sentry but don't crash the CLI.
        capture_exception(e)
        return VersionInfo.parse("0.0.0")


def get_latest_version() -> Optional[VersionInfo]:
    """Retrieves the latest version of the CLI from PyPI."""

    try:
        response = requests.get(f"https://pypi.org/pypi/{CLI_PACKAGE_NAME}/json").json()
    except Exception as e:
        # Log the error in Sentry but don't crash the CLI.
        capture_exception(e)
        return None

    try:
        return VersionInfo.parse(response["info"]["version"])
    except (KeyError, ValueError) as e:
        # Log the error in Sentry but don't crash the CLI.
        capture_exception(e)
        return None


def maybe_display_update_message() -> None:
    """If there is a newer version of the CLI available, displays a message to
    the user. Otherwise, does nothing.
    """
    if get_current_version() == VersionInfo.parse("0.0.0"):
        # Don't print the update message if local testing
        return

    if (latest_version := get_latest_version()) and latest_version > get_current_version():
        cli_output.error(
            message=f"Your version of symflow is out of date! The latest version is {latest_version}."
            + "\n"
            + "If you're using Homebrew, you can update by running `brew update && brew upgrade symopsio/tap/symflow`.\n"
            + "Otherwise, please see https://docs.symops.com/docs/install-sym-flow-cli",
            color="yellow",
        )
