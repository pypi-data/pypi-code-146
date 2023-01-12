import re
from datetime import timedelta
from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import InvalidExpiryError
from sym.flow.cli.helpers.global_options import GlobalOptions


def to_timedelta(value: str) -> int:
    """Parses the shorthand expiry and returns a timedelta if it is in an accepted format"""

    # Accepted expiries are an integer (non-zero, non-zero-leading) followed by [s, m, d, or mo]
    expiry_pattern = re.compile(r"^([1-9][0-9]*)(\w{1,2})$")
    value = value.strip()

    if expiry_value := expiry_pattern.match(value):
        duration_value = int(expiry_value.group(1))
        duration_unit = expiry_value.group(2)
        if duration_unit == "s":
            return int(timedelta(seconds=duration_value).total_seconds())
        elif duration_unit == "m":
            return int(timedelta(minutes=duration_value).total_seconds())
        elif duration_unit == "d":
            return int(timedelta(days=duration_value).total_seconds())
        elif duration_unit == "mo":
            return int(timedelta(days=30 * duration_value).total_seconds())

    raise InvalidExpiryError(value)


@click.command(name="issue", short_help="Issue a new Sym Token")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "-u",
    "--username",
    help="The name of the bot-user to issue the token for",
    prompt="Bot username",
    required=True,
)
@click.option(
    "-e",
    "--expiry",
    help="The TTL for the token in shorthand",
    prompt=True,
    required=True,
)
@click.option(
    "-l",
    "--label",
    help="An optional label for the token",
    required=False,
)
@click.option(
    "-n",
    "--no-newline",
    is_flag=True,
    show_default=True,
    default=False,
    help="Do not print a trailing newline character",
)
def tokens_issue(
    options: GlobalOptions,
    username: str,
    expiry: str,
    no_newline: bool,
    label: Optional[str],
) -> None:
    """
    Issues a new token for the bot-user identified by the given username.
    The expiry is a time duration in shorthand, e.g. `30d`

    \b
    Accepted durations are:
        - `s` = seconds
        - `m` = minutes
        - `d` = days
        - `mo` = months (30 days)
    """
    expiry = to_timedelta(expiry)
    access_token = options.sym_api.create_token(username.strip(), expiry, label)
    newline = not no_newline

    cli_output.success(access_token, newline=newline)
