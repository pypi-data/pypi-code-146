import click
from sym.shared.cli.helpers.sym_group import SymGroup

from sym.flow.cli.helpers.global_options import GlobalOptions

from .add import domains_add
from .list import domains_list
from .remove import domains_remove


@click.group(name="domains", cls=SymGroup, short_help="Perform operations on domains")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def domains(options: GlobalOptions) -> None:
    """Operations on domains.

    Domains are used to decide who can join your organization. For example,
    when an unknown user interacts with your Sym Slack App, they will be automatically
    added to your organization (and allowed to run your Flows) if and only if their email
    domain matches one defined for your organization.

    Users may still be added manually using `symflow users create` even if their email does not
    match any of the configured domains.
    """


domains.add_command(domains_add)
domains.add_command(domains_list)
domains.add_command(domains_remove)
