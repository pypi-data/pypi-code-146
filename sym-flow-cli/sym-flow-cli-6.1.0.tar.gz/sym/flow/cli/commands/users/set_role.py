from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.utils import get_or_prompt


@click.command(name="set-role", short_help="Update a User's role")
@click.argument("email", required=True, type=str)
@click.option("--role", "role", help="The new role value", type=str)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def set_role(options: GlobalOptions, email: str, role: Optional[str] = None) -> None:
    """For an existing Sym User, set their active role.

    \b
    - Guests may only approve, deny, or revoke access requests for flows that allow guest
    - Members may run any of your organization's flows, as well as do anything a guest can do.
    - Admins may manage other users and flows, as well as do anything a member can do.

    \b
    Example:
        `symflow users set-role user@symops.io --role admin`
    """

    api = options.sym_api
    user = api.get_user(email)
    role = get_or_prompt(role, "Which role?", ["admin", "member", "guest"])
    api.set_user_role(user.id, role)

    cli_output.success(f"Success! {email} now has the role '{role}'.")
