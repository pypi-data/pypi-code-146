import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(name="add", short_help="Add a domain")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("domain")
def domains_add(options: GlobalOptions, domain: str) -> None:
    """Add a new domain to your organization."""

    options.sym_api.add_domain(domain)
    cli_output.success(f"{domain} successfully added as a domain.")
