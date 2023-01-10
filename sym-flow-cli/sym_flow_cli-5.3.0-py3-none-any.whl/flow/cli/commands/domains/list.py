import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(name="list", short_help="List all domains")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def domains_list(options: GlobalOptions) -> None:
    """List your organization's configured domains.

    Domains are used to decide who can join your organization. For example,
    when an unknown user interacts with your Sym Slack App, they will be automatically
    added to your organization (and allowed to run your Flows) if and only if their email
    domain matches one defined for your organization.

    Users may still be added manually using `symflow users create` even if their email does not
    match any of the configured domains.
    """

    org = options.sym_api.get_current_organization()

    if domains := org.domains:
        cli_output.info("Your organization's configured domains:")
        cli_output.info("- " + "\n- ".join(domains))
    else:
        cli_output.info("Your organization does not have any domains configured.")
