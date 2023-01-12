from typing import List, Optional, Tuple

import click

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.profile_operations import update_full_name


@click.command(name="update-name", short_help="Update a User's name")
@click.argument("email", required=True, type=str)
@click.argument("full_name", required=True, type=str, nargs=-1)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def update_name(
    options: GlobalOptions,
    email: str,
    full_name: Tuple[str],
) -> None:
    """For an existing Sym User, update their full name in their Sym identity

    \b
    Example:
        1. `symflow users update-name beyonce@symops.io Beyonce`
        2. `symflow users update-name anupya@symops.io Anupya Pamidimukkala`
        2. `symflow users update-name neil@symops.io Neil Patrick Harris Martin Sheen`
    """

    api = options.sym_api
    user_to_update = api.get_user(email)
    first_and_middle_name, last_name = split_name(full_name)

    update_full_name(options, user_to_update, first_and_middle_name, last_name)


def split_name(name: Tuple[str]) -> Tuple[List[str], Optional[str]]:
    """Splits a given name into first and last name. If there are more
    than two words, all but the last word are combined into the first name.
    """

    if len(name) == 1:  # mononyms
        return name[0], ""
    else:
        return " ".join(name[:-1]), name[-1]
