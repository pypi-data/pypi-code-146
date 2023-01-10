from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.commands.users.utils import get_or_prompt_service
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(name="update", short_help="Update an existing service")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--service-type",
    "_service_type",
    help="The service to update",
)
@click.option(
    "--external-id",
    "_external_id",
    help="The identifier for the service",
)
@click.option(
    "--label",
    "_label",
    help="The label for the service",
)
def services_update(
    options: GlobalOptions, _service_type: Optional[str], _external_id: Optional[str], _label: Optional[str]
) -> None:
    service = get_or_prompt_service(options.sym_api, _service_type, _external_id)
    options.sym_api.update_service(service.service_type, service.external_id, _label)
    cli_output.success(f"Successfully updated 1 service!")
