import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(name="remove", short_help="Remove a domain")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("domain")
def domains_remove(options: GlobalOptions, domain: str) -> None:
    """Remove a domain from your organization.

    Note: this will not affect any existing users in your organization.
    """

    options.sym_api.remove_domain(domain)
    cli_output.success(f"{domain} successfully removed as a domain.")
