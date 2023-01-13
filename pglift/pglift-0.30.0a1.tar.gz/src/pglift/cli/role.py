import functools
from typing import IO, Any, Sequence

import click
from pydantic.utils import deep_update

from .. import postgresql, privileges, roles
from ..ctx import Context
from ..models import helpers, interface, system
from .util import (
    Group,
    OutputFormat,
    dry_run_option,
    instance_identifier_option,
    output_format_option,
    pass_ctx,
    pass_instance,
    print_argspec,
    print_json_for,
    print_schema,
    print_table_for,
)


@click.group("role", cls=Group)
@instance_identifier_option
@click.option(
    "--schema",
    is_flag=True,
    callback=functools.partial(print_schema, model=interface.Role),
    expose_value=False,
    is_eager=True,
    help="Print the JSON schema of role model and exit.",
)
@click.option(
    "--ansible-argspec",
    is_flag=True,
    callback=functools.partial(
        print_argspec, model=interface.Role, result=interface.ApplyResult
    ),
    expose_value=False,
    is_eager=True,
    hidden=True,
    help="Print the Ansible argspec of role model and exit.",
)
def cli(instance: system.Instance) -> None:
    """Manage roles."""


@cli.command("create")
@helpers.parameters_from_model(interface.Role, "create")
@pass_instance
@pass_ctx
def role_create(ctx: Context, instance: system.Instance, role: interface.Role) -> None:
    """Create a role in a PostgreSQL instance"""
    with postgresql.running(ctx, instance):
        if roles.exists(ctx, instance, role.name):
            raise click.ClickException("role already exists")
        roles.apply(ctx, instance, role)


@cli.command("alter")
@helpers.parameters_from_model(interface.Role, "update", parse_model=False)
@click.argument("rolname")
@pass_instance
@pass_ctx
def role_alter(
    ctx: Context, instance: system.Instance, rolname: str, **changes: Any
) -> None:
    """Alter a role in a PostgreSQL instance"""
    with postgresql.running(ctx, instance):
        values = roles.get(ctx, instance, rolname).dict()
        values = deep_update(values, changes)
        altered = interface.Role.parse_obj(values)
        roles.apply(ctx, instance, altered)


@cli.command("apply", hidden=True)
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@output_format_option
@dry_run_option
@pass_instance
@pass_ctx
def role_apply(
    ctx: Context,
    instance: system.Instance,
    file: IO[str],
    output_format: OutputFormat,
    dry_run: bool,
) -> None:
    """Apply manifest as a role"""
    role = interface.Role.parse_yaml(file)
    if dry_run:
        ret = interface.ApplyResult(change_state=None)
    else:
        with postgresql.running(ctx, instance):
            ret = roles.apply(ctx, instance, role)
    if output_format == OutputFormat.json:
        print_json_for(ret)


@cli.command("list")
@output_format_option
@pass_instance
@pass_ctx
def role_list(
    ctx: Context,
    instance: system.Instance,
    output_format: OutputFormat,
) -> None:
    """List roles in instance"""

    with postgresql.running(ctx, instance):
        rls = [r.dict(by_alias=True) for r in roles.list(ctx, instance)]

    if output_format == OutputFormat.json:
        print_json_for(rls)
    else:
        print_table_for(rls)


@cli.command("get")
@output_format_option
@click.argument("name")
@pass_instance
@pass_ctx
def role_get(
    ctx: Context,
    instance: system.Instance,
    name: str,
    output_format: OutputFormat,
) -> None:
    """Get the description of a role"""
    with postgresql.running(ctx, instance):
        m = roles.get(ctx, instance, name).dict(by_alias=True)
    if output_format == OutputFormat.json:
        print_json_for(m)
    else:
        print_table_for([m], box=None)


@cli.command("drop")
@helpers.parameters_from_model(interface.RoleDropped, "create")
@pass_instance
@pass_ctx
def role_drop(
    ctx: Context, instance: system.Instance, roledropped: interface.RoleDropped
) -> None:
    """Drop a role"""
    with postgresql.running(ctx, instance):
        roles.drop(ctx, instance, roledropped)


@cli.command("privileges")
@click.argument("name")
@click.option(
    "-d", "--database", "databases", multiple=True, help="Database to inspect"
)
@click.option("--default", "defaults", is_flag=True, help="Display default privileges")
@output_format_option
@pass_instance
@pass_ctx
def role_privileges(
    ctx: Context,
    instance: system.Instance,
    name: str,
    databases: Sequence[str],
    defaults: bool,
    output_format: OutputFormat,
) -> None:
    """List privileges of a role."""
    with postgresql.running(ctx, instance):
        roles.get(ctx, instance, name)  # check existence
        try:
            prvlgs = privileges.get(
                ctx, instance, databases=databases, roles=(name,), defaults=defaults
            )
        except ValueError as e:
            raise click.ClickException(str(e))
    if output_format == OutputFormat.json:
        print_json_for((i.dict(by_alias=True) for i in prvlgs))
    else:
        print_table_for((i.dict(by_alias=True) for i in prvlgs))
