from functools import partial
from typing import IO, TYPE_CHECKING

import click

from .. import exceptions, prometheus, task
from ..cli.util import (
    Group,
    OutputFormat,
    dry_run_option,
    foreground_option,
    output_format_option,
    pass_component_settings,
    pass_ctx,
    print_argspec,
    print_json_for,
    print_schema,
)
from ..models import helpers, interface
from . import impl, models

if TYPE_CHECKING:
    from ..ctx import Context
    from ..settings import PrometheusSettings

pass_prometheus_settings = partial(
    pass_component_settings, prometheus, "Prometheus postgres_exporter"
)


@click.group("postgres_exporter", cls=Group)
@click.option(
    "--schema",
    is_flag=True,
    callback=partial(print_schema, model=models.PostgresExporter),
    expose_value=False,
    is_eager=True,
    help="Print the JSON schema of postgres_exporter model and exit.",
)
@click.option(
    "--ansible-argspec",
    is_flag=True,
    callback=partial(
        print_argspec, model=models.PostgresExporter, result=interface.ApplyResult
    ),
    expose_value=False,
    is_eager=True,
    hidden=True,
    help="Print the Ansible argspec of postgres_exporter model and exit.",
)
@pass_ctx
def postgres_exporter(ctx: "Context") -> None:
    """Handle Prometheus postgres_exporter"""


@postgres_exporter.command("apply")
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@output_format_option
@dry_run_option
@pass_prometheus_settings
@pass_ctx
def postgres_exporter_apply(
    ctx: "Context",
    settings: "PrometheusSettings",
    file: IO[str],
    output_format: OutputFormat,
    dry_run: bool,
) -> None:
    """Apply manifest as a Prometheus postgres_exporter."""
    exporter = models.PostgresExporter.parse_yaml(file)
    if dry_run:
        ret = interface.ApplyResult(change_state=None)
    else:
        ret = impl.apply(ctx, exporter, settings)
    if output_format == OutputFormat.json:
        print_json_for(ret)


@postgres_exporter.command("install")
@helpers.parameters_from_model(models.PostgresExporter, "create")
@pass_prometheus_settings
@pass_ctx
def postgres_exporter_install(
    ctx: "Context",
    settings: "PrometheusSettings",
    postgresexporter: models.PostgresExporter,
) -> None:
    """Install the service for a (non-local) instance."""
    with task.transaction():
        impl.apply(ctx, postgresexporter, settings)


@postgres_exporter.command("uninstall")
@click.argument("name")
@pass_ctx
def postgres_exporter_uninstall(ctx: "Context", name: str) -> None:
    """Uninstall the service."""
    impl.drop(ctx, name)


@postgres_exporter.command("start")
@click.argument("name")
@foreground_option
@pass_prometheus_settings
@pass_ctx
def postgres_exporter_start(
    ctx: "Context", settings: "PrometheusSettings", name: str, foreground: bool
) -> None:
    """Start postgres_exporter service NAME.

    The NAME argument is a local identifier for the postgres_exporter
    service. If the service is bound to a local instance, it should be
    <version>-<name>.
    """
    service = impl.system_lookup(ctx, name, settings)
    if service is None:
        raise exceptions.InstanceNotFound(name)
    impl.start(ctx, service, foreground=foreground)


@postgres_exporter.command("stop")
@click.argument("name")
@pass_prometheus_settings
@pass_ctx
def postgres_exporter_stop(
    ctx: "Context", settings: "PrometheusSettings", name: str
) -> None:
    """Stop postgres_exporter service NAME.

    The NAME argument is a local identifier for the postgres_exporter
    service. If the service is bound to a local instance, it should be
    <version>-<name>.
    """
    service = impl.system_lookup(ctx, name, settings)
    if service is None:
        raise exceptions.InstanceNotFound(name)
    impl.stop(ctx, service)
