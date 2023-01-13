from typing import IO, Any, Callable, Dict, List, Optional, Sequence, Tuple, Type

import click
from pydantic.utils import deep_update

from .. import instances, pm, postgresql, privileges, task
from ..ctx import Context
from ..models import helpers, interface, system
from ..postgresql import Status
from ..settings import PostgreSQLVersion
from .util import (
    Command,
    Group,
    OutputFormat,
    _list_instances,
    dry_run_option,
    foreground_option,
    instance_lookup,
    output_format_option,
    pass_ctx,
    print_argspec,
    print_json_for,
    print_schema,
    print_table_for,
)

Callback = Callable[..., Any]
CommandFactory = Callable[[Type[interface.Instance]], Callback]


def instance_identifier(nargs: int = 1) -> Callable[[Callback], Callback]:
    def decorator(fn: Callback) -> Callback:
        command = click.argument(
            "instance",
            nargs=nargs,
            required=False,
            callback=instance_lookup,
            shell_complete=_list_instances,
        )(fn)
        assert command.__doc__
        command.__doc__ += (
            "\n\nINSTANCE identifies target instance as <version>/<name> where the "
            "<version>/ prefix may be omitted if there is only one instance "
            "matching <name>. Required if there is more than one instance on "
            "system."
        )
        return command

    return decorator


class InstanceCommands(Group):
    """Group for 'instance' sub-commands handling some of them that require a
    composite interface.Instance model built from registered plugins at
    runtime.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._composite_instance_commands: Dict[str, CommandFactory] = {}
        self._plugin_commands_loaded = False

    def command_with_composite_instance(
        self, name: str
    ) -> Callable[[CommandFactory], None]:
        """Decorator for callback that needs a composite Instance model"""
        assert name not in self._composite_instance_commands, name

        def decorator(factory: CommandFactory) -> None:
            self._composite_instance_commands[name] = factory

        return decorator

    def _load_plugins_commands(self, context: click.Context) -> bool:
        if self._plugin_commands_loaded:
            return False

        obj = context.obj
        if obj is None:
            from . import InvalidSettingsError, Obj

            try:
                obj = context.ensure_object(Obj)
            except InvalidSettingsError:
                return False

        if obj is None:
            return False

        obj.ctx.hook.instance_cli(group=self)
        self._plugin_commands_loaded = True
        return True

    def add_command(self, cmd: click.Command, name: Optional[str] = None) -> None:
        name = name or cmd.name
        assert (
            name not in self.commands
        ), f"instance command '{name}' already registered"
        super().add_command(cmd, name)

    def list_commands(self, context: click.Context) -> List[str]:
        self._load_plugins_commands(context)
        return sorted(
            super().list_commands(context) + list(self._composite_instance_commands)
        )

    def get_command(self, context: click.Context, name: str) -> Optional[click.Command]:
        self._load_plugins_commands(context)
        try:
            factory = self._composite_instance_commands[name]
        except KeyError:
            return super().get_command(context, name)
        else:
            if context.obj is None:  # During shell complete.
                model = interface.Instance
            else:
                model = interface.Instance.composite(context.obj.ctx.pm)
            f = factory(model)
            return click.command(cls=Command)(f)


def print_instance_schema(
    context: click.Context, param: click.Parameter, value: bool
) -> None:
    return print_schema(
        context, param, value, model=interface.Instance.composite(context.obj.ctx.pm)
    )


def print_instance_argspec(
    context: click.Context, param: click.Parameter, value: bool
) -> None:
    p = pm.PluginManager.all()
    model = interface.Instance.composite(p)
    print_argspec(
        context, param, value, model=model, result=interface.InstanceApplyResult
    )


@click.group(cls=InstanceCommands)
@click.option(
    "--schema",
    is_flag=True,
    callback=print_instance_schema,
    expose_value=False,
    is_eager=True,
    help="Print the JSON schema of instance model and exit.",
)
@click.option(
    "--ansible-argspec",
    is_flag=True,
    callback=print_instance_argspec,
    expose_value=False,
    is_eager=True,
    hidden=True,
    help="Print the Ansible argspec of instance model and exit.",
)
def cli() -> None:
    """Manage instances."""


# Help mypy because click.group() looses the type of 'cls' argument.
assert isinstance(cli, InstanceCommands)


@cli.command_with_composite_instance("create")
def _instance_create(
    composite_instance_model: Type[interface.Instance],
) -> Callback:
    @helpers.parameters_from_model(composite_instance_model, "create")
    @click.option(
        "--drop-on-error/--no-drop-on-error",
        default=True,
        help=(
            "On error, drop partially initialized instance by possibly "
            "rolling back operations (true by default)."
        ),
    )
    @pass_ctx
    def command(
        ctx: Context, instance: interface.Instance, drop_on_error: bool
    ) -> None:
        """Initialize a PostgreSQL instance"""
        if instances.exists(ctx, instance.name, instance.version):
            raise click.ClickException("instance already exists")
        with task.transaction(drop_on_error):
            instances.apply(ctx, instance)

    return command


@cli.command_with_composite_instance("alter")
def _instance_alter(
    composite_instance_model: Type[interface.Instance],
) -> Callback:
    @instance_identifier(nargs=1)
    @helpers.parameters_from_model(
        composite_instance_model, "update", parse_model=False
    )
    @pass_ctx
    def command(ctx: Context, instance: system.Instance, **changes: Any) -> None:
        """Alter PostgreSQL INSTANCE"""
        values = instances._get(ctx, instance).dict(exclude={"settings"})
        values = deep_update(values, changes)
        altered = composite_instance_model.parse_obj(values)
        instances.apply(ctx, altered)

    return command


@cli.command("apply", hidden=True)
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@output_format_option
@dry_run_option
@pass_ctx
def instance_apply(
    ctx: Context,
    file: IO[str],
    output_format: OutputFormat,
    dry_run: bool,
) -> None:
    """Apply manifest as a PostgreSQL instance"""
    model = interface.Instance.composite(ctx.pm)
    instance = model.parse_yaml(file)
    if dry_run:
        ret = interface.InstanceApplyResult(change_state=None)
    else:
        ret = instances.apply(ctx, instance)
    if output_format == OutputFormat.json:
        print_json_for(ret)


@cli.command("promote")
@instance_identifier(nargs=1)
@pass_ctx
def instance_promote(ctx: Context, instance: system.Instance) -> None:
    """Promote standby PostgreSQL INSTANCE"""
    instances.promote(ctx, instance)


@cli.command("get")
@output_format_option
@instance_identifier(nargs=1)
@pass_ctx
def instance_get(
    ctx: Context,
    instance: system.Instance,
    output_format: OutputFormat,
) -> None:
    """Get the description of PostgreSQL INSTANCE.

    Unless --output-format is specified, 'settings' and 'state' fields are not
    shown as well as 'standby' information if INSTANCE is not a standby.
    """
    exclude = set()
    if not output_format:
        exclude.update(
            [
                "settings",
                "state",
                "data_directory",
                "wal_directory",
                "powa",
            ]
        )
        if not instance.standby:
            exclude.add("standby")
    m = instances.get(ctx, instance).dict(by_alias=True, exclude=exclude)
    if output_format == OutputFormat.json:
        print_json_for(m)
    else:
        print_table_for([m], box=None)


@cli.command("list")
@click.option(
    "--version",
    type=click.Choice(list(PostgreSQLVersion)),
    help="Only list instances of specified version.",
)
@output_format_option
@pass_ctx
def instance_list(
    ctx: Context,
    version: Optional[PostgreSQLVersion],
    output_format: OutputFormat,
) -> None:
    """List the available instances"""

    insts = instances.list(ctx, version=version)
    if output_format == OutputFormat.json:
        print_json_for((i.dict(by_alias=True) for i in insts))
    else:
        print_table_for((i.dict(by_alias=True) for i in insts))


@cli.command("drop")
@instance_identifier(nargs=-1)
@pass_ctx
def instance_drop(ctx: Context, instance: Tuple[system.Instance, ...]) -> None:
    """Drop PostgreSQL INSTANCE"""
    for i in instance:
        instances.drop(ctx, i)


@cli.command("status")
@instance_identifier(nargs=1)
@click.pass_context
def instance_status(context: click.Context, instance: system.Instance) -> None:
    """Check the status of PostgreSQL INSTANCE.

    Output the status string value ('running', 'not running', 'unspecified
    datadir') and exit with respective status code (0, 3, 4).
    """
    ctx = context.obj.ctx
    status = postgresql.status(ctx, instance)
    click.echo(status.name.replace("_", " "))
    context.exit(status.value)


@cli.command("start")
@instance_identifier(nargs=-1)
@foreground_option
@click.option("--all", "all_instances", is_flag=True, help="Start all instances.")
@pass_ctx
def instance_start(
    ctx: Context,
    instance: Tuple[system.Instance, ...],
    foreground: bool,
    all_instances: bool,
) -> None:
    """Start PostgreSQL INSTANCE"""
    if foreground and len(instance) != 1:
        raise click.UsageError(
            "only one INSTANCE argument may be given with --foreground"
        )
    for i in instance:
        instances.start(ctx, i, foreground=foreground)


@cli.command("stop")
@instance_identifier(nargs=-1)
@click.option("--all", "all_instances", is_flag=True, help="Stop all instances.")
@pass_ctx
def instance_stop(
    ctx: Context, instance: Tuple[system.Instance, ...], all_instances: bool
) -> None:
    """Stop PostgreSQL INSTANCE"""
    for i in instance:
        instances.stop(ctx, i)


@cli.command("reload")
@instance_identifier(nargs=-1)
@click.option("--all", "all_instances", is_flag=True, help="Reload all instances.")
@pass_ctx
def instance_reload(
    ctx: Context, instance: Tuple[system.Instance, ...], all_instances: bool
) -> None:
    """Reload PostgreSQL INSTANCE"""
    for i in instance:
        instances.reload(ctx, i)


@cli.command("restart")
@instance_identifier(nargs=-1)
@click.option("--all", "all_instances", is_flag=True, help="Restart all instances.")
@pass_ctx
def instance_restart(
    ctx: Context, instance: Tuple[system.Instance, ...], all_instances: bool
) -> None:
    """Restart PostgreSQL INSTANCE"""
    for i in instance:
        instances.restart(ctx, i)


@cli.command("exec")
@instance_identifier(nargs=1)
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
@pass_ctx
def instance_exec(
    ctx: Context, instance: system.Instance, command: Tuple[str, ...]
) -> None:
    """Execute command in the libpq environment for PostgreSQL INSTANCE"""
    if not command:
        raise click.ClickException("no command given")
    instances.exec(ctx, instance, command)


@cli.command("env")
@instance_identifier(nargs=1)
@output_format_option
@pass_ctx
def instance_env(
    ctx: Context, instance: system.Instance, output_format: OutputFormat
) -> None:
    """Output environment variables suitable to handle to PostgreSQL INSTANCE.

    This can be injected in shell using:

    export $(pglift instance env myinstance)
    """
    instance_env = instances.env_for(ctx, instance, path=True)
    if output_format == OutputFormat.json:
        print_json_for(instance_env)
    else:
        for key, value in sorted(instance_env.items()):
            click.echo(f"{key}={value}")


@cli.command("logs")
@instance_identifier(nargs=1)
@pass_ctx
def instance_logs(ctx: Context, instance: system.Instance) -> None:
    """Output INSTANCE logs

    This assumes that the PostgreSQL instance is configured to use file-based
    logging (i.e. log_destination amongst 'stderr' or 'csvlog').
    """
    for line in instances.logs(ctx, instance):
        click.echo(line, nl=False)


@cli.command("privileges")
@instance_identifier(nargs=1)
@click.option(
    "-d",
    "--database",
    "databases",
    multiple=True,
    help="Database to inspect. When not provided, all databases are inspected.",
)
@click.option("-r", "--role", "roles", multiple=True, help="Role to inspect")
@click.option("--default", "defaults", is_flag=True, help="Display default privileges")
@output_format_option
@pass_ctx
def instance_privileges(
    ctx: Context,
    instance: system.Instance,
    databases: Sequence[str],
    roles: Sequence[str],
    defaults: bool,
    output_format: OutputFormat,
) -> None:
    """List privileges on INSTANCE's databases."""
    with postgresql.running(ctx, instance):
        try:
            prvlgs = privileges.get(
                ctx, instance, databases=databases, roles=roles, defaults=defaults
            )
        except ValueError as e:
            raise click.ClickException(str(e))
    if output_format == OutputFormat.json:
        print_json_for((i.dict(by_alias=True) for i in prvlgs))
    else:
        if defaults:
            title = f"Default privileges on instance {instance}"
        else:
            title = f"Privileges on instance {instance}"
        print_table_for((i.dict(by_alias=True) for i in prvlgs), title=title)


@cli.command("upgrade")
@instance_identifier(nargs=1)
@click.option(
    "--version",
    "newversion",
    type=click.Choice(list(PostgreSQLVersion)),
    help="PostgreSQL version of the new instance (default to site-configured value).",
)
@click.option(
    "--name", "newname", help="Name of the new instance (default to old instance name)."
)
@click.option(
    "--port", required=False, type=click.INT, help="Port of the new instance."
)
@click.option(
    "--jobs",
    required=False,
    type=click.INT,
    help="Number of simultaneous processes or threads to use (from pg_upgrade).",
)
@pass_ctx
def instance_upgrade(
    ctx: Context,
    instance: system.Instance,
    newversion: Optional[PostgreSQLVersion],
    newname: Optional[str],
    port: Optional[int],
    jobs: Optional[int],
) -> None:
    """Upgrade INSTANCE using pg_upgrade"""
    postgresql.check_status(ctx, instance, Status.not_running)
    new_instance = instances.upgrade(
        ctx, instance, version=newversion, name=newname, port=port, jobs=jobs
    )
    instances.start(ctx, new_instance)
