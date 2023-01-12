from typing import List

import click
from tabulate import tabulate

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.utils import human_friendly, utc_to_local


@click.command(name="list", short_help="List all Users")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users_list(options: GlobalOptions) -> None:
    """Lists all Users in your organization."""
    table_data = get_user_data(options.sym_api)
    cli_output.info(tabulate(table_data, headers="firstrow"))


def get_user_data(api: SymAPI) -> List[List[str]]:
    table_data = [["Name", "Email", "Role", "Created At"]]
    for user in api.get_users():
        created_at = human_friendly(utc_to_local(user.created_at))  # type: ignore
        table_data.append([user.sym_name, user.sym_email, user.role, created_at])

    # This makes sure the column names are not sorted, and we sort using only the email in alphabetical order
    table_data[1:] = sorted(table_data[1:], key=lambda row: row[1])
    return table_data
