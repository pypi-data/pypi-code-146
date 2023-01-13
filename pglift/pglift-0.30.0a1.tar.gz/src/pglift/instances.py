import contextlib
import logging
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Tuple, Type

import psycopg.rows
import psycopg.sql
from pgtoolkit import conf as pgconf
from pgtoolkit import pgpass
from pydantic import SecretStr

from . import cmd, conf, databases, db, exceptions, postgresql, roles, util
from .models import interface, system
from .postgresql import Standby, Status
from .postgresql.ctl import get_data_checksums, set_data_checksums, show_data_checksums
from .settings import PostgreSQLVersion
from .task import task
from .types import ConfigChanges, PostgreSQLStopMode

if TYPE_CHECKING:
    from .ctx import Context

logger = logging.getLogger(__name__)


@task("initializing PostgreSQL instance")
def init(ctx: "Context", manifest: interface.Instance) -> system.PostgreSQLInstance:
    """Initialize a PostgreSQL instance."""
    try:
        return system.PostgreSQLInstance.system_lookup(
            ctx, (manifest.name, manifest.version)
        )
    except exceptions.InstanceNotFound:
        pass

    postgresql_settings = ctx.settings.postgresql
    postgresql_settings.socket_directory.mkdir(parents=True, exist_ok=True)

    sys_instance = system.BaseInstance.get(manifest.name, manifest.version, ctx)

    ctx.hook.initdb(ctx=ctx, manifest=manifest, instance=sys_instance)

    if ctx.hook.configure_auth(
        settings=ctx.settings, instance=sys_instance, manifest=manifest
    ) and postgresql.is_running(ctx, sys_instance):
        ctx.hook.restart_postgresql(
            ctx=ctx, instance=sys_instance, mode="fast", wait=True
        )

    sys_instance.psqlrc.write_text(
        "\n".join(
            [
                f"\\set PROMPT1 '[{sys_instance}] %n@%~%R%x%# '",
                "\\set PROMPT2 ' %R%x%# '",
            ]
        )
        + "\n"
    )

    ctx.hook.enable_service(
        ctx=ctx,
        service=ctx.hook.postgresql_service_name(ctx=ctx, instance=sys_instance),
        name=sys_instance.qualname,
    )

    return system.PostgreSQLInstance.system_lookup(ctx, sys_instance)


@init.revert("deleting PostgreSQL instance")
def revert_init(ctx: "Context", manifest: interface.Instance) -> None:
    """Un-initialize a PostgreSQL instance."""
    sys_instance = system.BaseInstance.get(manifest.name, manifest.version, ctx)
    ctx.hook.disable_service(
        ctx=ctx,
        service=ctx.hook.postgresql_service_name(ctx=ctx, instance=sys_instance),
        name=sys_instance.qualname,
        now=True,
    )

    for path in (sys_instance.datadir, sys_instance.waldir):
        if path.exists():
            ctx.rmtree(path)


def configure(
    ctx: "Context",
    manifest: interface.Instance,
    *,
    run_hooks: bool = True,
    _creating: bool = False,
) -> ConfigChanges:
    """Write instance's configuration in postgresql.conf."""
    with configure_context(
        ctx, manifest, run_hooks=run_hooks, creating=_creating
    ) as changes:
        return changes


@contextlib.contextmanager
def configure_context(
    ctx: "Context",
    manifest: interface.Instance,
    *,
    run_hooks: bool = True,
    creating: bool = False,
    upgrading_from: Optional[system.Instance] = None,
) -> Iterator[ConfigChanges]:
    """Context manager to write instance's configuration in postgresql.conf
    while pausing for further actions before calling 'instance_configure'
    hooks.

    Also compute changes to the overall PostgreSQL configuration and return it
    as a 'ConfigChanges' dictionary.
    """
    logger.info("configuring PostgreSQL instance")
    instance = system.BaseInstance.get(manifest.name, manifest.version, ctx)

    config = configuration(ctx, manifest, instance)
    changes = ctx.hook.configure_postgresql(
        ctx=ctx, manifest=manifest, configuration=config, instance=instance
    )

    yield changes

    if run_hooks:
        ctx.hook.instance_configure(
            ctx=ctx,
            manifest=manifest,
            config=config,
            changes=changes,
            creating=creating,
            upgrading_from=upgrading_from,
        )

    if not creating:
        instance = system.Instance.system_lookup(ctx, instance)
        check_pending_actions(ctx, instance, changes, manifest.restart_on_changes)


def configure_ssl(
    ctx: "Context",
    configuration: Dict[str, Any],
    name: str,
    directory: Path,
) -> Dict[str, str]:
    """Possibly generate SSL certificate files in 'directory' based on specified 'configuration'."""
    if not configuration.get("ssl"):
        return {}
    try:
        cert, key = Path(configuration["ssl_cert_file"]), Path(
            configuration["ssl_key_file"]
        )
    except KeyError:
        cert, key = Path(f"{name}.crt"), Path(f"{name}.key")
        directory.mkdir(exist_ok=True, parents=True)
    if not cert.is_absolute():
        cert = directory / cert
    if not key.is_absolute():
        key = directory / key
    if not cert.exists() and not key.exists():
        certcontent, keycontent = util.generate_certificate(run_command=ctx.run)
        cert.write_text(certcontent)
        key.touch(mode=0o600)
        key.write_text(keycontent)
    else:
        assert (
            cert.exists() and key.exists()
        ), f"One of SSL certificate files {cert} or {key} exists but the other does not"
    return {"ssl_cert_file": str(cert), "ssl_key_file": str(key)}


def configuration(
    ctx: "Context", manifest: interface.Instance, instance: system.BaseInstance
) -> pgconf.Configuration:
    """Return instance settings from manifest.

    `manifest.settings.ssl`, `manifest.settings.ssl_cert_file` and
    `manifest.settings.ssl_key_file` control the SSL settings.
    If the `ssl` field is:
       - False, SSL is not enabled
       - True (without specifying cert and key), a self-signed certificate is generated
       - True and the ssl_cert_file and ssl_key_file are present, the instance will be
         configured with those files (if they exist)

    'shared_buffers' and 'effective_cache_size' setting, if defined and set to
    a percent-value, will be converted to proper memory value relative to the
    total memory available on the system.
    """
    confitems: Dict[str, pgconf.Value] = {
        "cluster_name": manifest.name,
        "port": manifest.port,
    }

    # Load base configuration from site settings.
    postgresql_conf_template = util.template("postgresql", "postgresql.conf")
    confitems.update(pgconf.parse_string(postgresql_conf_template).as_dict())

    # Transform initdb options as configuration parameters.
    locale = manifest.initdb_options(ctx.settings.postgresql.initdb).locale
    if locale:
        for key in ("lc_messages", "lc_monetary", "lc_numeric", "lc_time"):
            confitems.setdefault(key, locale)

    confitems.update(manifest.settings)

    ssl_cert_directory = ctx.settings.postgresql.ssl_cert_directory
    ssl_config = configure_ssl(
        ctx, manifest.settings, instance.qualname, ssl_cert_directory
    )
    confitems.update(ssl_config)

    try:
        logdir = confitems["log_directory"]
    except KeyError:
        pass
    else:
        assert isinstance(logdir, str)  # per model validation
        conf.log_directory(instance.datadir, Path(logdir)).mkdir(
            exist_ok=True, parents=True
        )

    spl = manifest.settings.get("shared_preload_libraries", "")

    for r in ctx.hook.instance_settings(ctx=ctx, manifest=manifest, instance=instance):
        for k, v in r.entries.items():
            if k == "shared_preload_libraries":
                spl = conf.merge_lists(spl, v.value)
            else:
                confitems[k] = v.value

    if spl:
        confitems["shared_preload_libraries"] = spl

    conf.format_values(confitems, ctx.settings.postgresql)

    return conf.make(manifest.name, **confitems)


@contextlib.contextmanager
def running(ctx: "Context", instance: system.Instance) -> Iterator[None]:
    """Context manager to temporarily start an instance and run hooks."""
    if postgresql.status(ctx, instance) == postgresql.Status.running:
        yield
        return

    start(ctx, instance)
    try:
        yield
    finally:
        stop(ctx, instance)


@contextlib.contextmanager
def stopped(
    ctx: "Context",
    instance: system.Instance,
    *,
    timeout: int = 10,
) -> Iterator[None]:
    """Context manager to temporarily stop an instance.

    :param timeout: delay to wait for instance stop.

    :raises ~exceptions.InstanceStateError: when the instance did stop after
        specified `timeout` (in seconds).
    """
    if postgresql.status(ctx, instance) == Status.not_running:
        yield
        return

    stop(ctx, instance)
    for __ in range(timeout):
        time.sleep(1)
        if postgresql.status(ctx, instance) == Status.not_running:
            break
    else:
        raise exceptions.InstanceStateError(f"{instance} not stopped after {timeout}s")
    try:
        yield
    finally:
        start(ctx, instance)


def start(
    ctx: "Context",
    instance: system.Instance,
    *,
    foreground: bool = False,
    wait: bool = True,
    _warn: bool = True,
) -> None:
    """Start an instance.

    :param wait: possibly wait for PostgreSQL to get ready.
    :param foreground: start postgres in the foreground, replacing the current
        process.

    .. note:: When starting in "foreground", hooks will not be triggered and
        `wait` parameter have no effect.
    """
    _start_postgresql(ctx, instance, foreground=foreground, wait=wait, warn=_warn)
    if wait:
        if foreground:
            logger.debug("not running hooks for a foreground start")
        else:
            ctx.hook.instance_start(ctx=ctx, instance=instance)


def _start_postgresql(
    ctx: "Context",
    instance: system.PostgreSQLInstance,
    *,
    foreground: bool = False,
    wait: bool = True,
    warn: bool = True,
) -> None:
    if postgresql.is_running(ctx, instance):
        if warn:
            logger.warning("instance %s is already started", instance)
        return
    ctx.hook.start_postgresql(
        ctx=ctx, instance=instance, foreground=foreground, wait=wait
    )


def stop(
    ctx: "Context",
    instance: system.Instance,
    *,
    mode: PostgreSQLStopMode = "fast",
    wait: bool = True,
    deleting: bool = False,
) -> None:
    """Stop an instance."""
    if postgresql.status(ctx, instance) == Status.not_running:
        logger.warning("instance %s is already stopped", instance)
    else:
        ctx.hook.stop_postgresql(
            ctx=ctx, instance=instance, mode=mode, wait=wait, deleting=deleting
        )

    if wait:
        ctx.hook.instance_stop(ctx=ctx, instance=instance)


def restart(
    ctx: "Context",
    instance: system.Instance,
    *,
    mode: PostgreSQLStopMode = "fast",
    wait: bool = True,
) -> None:
    """Restart an instance."""
    logger.info("restarting instance %s", instance)
    ctx.hook.instance_stop(ctx=ctx, instance=instance)
    restart_postgresql(ctx, instance, mode=mode, wait=wait)
    ctx.hook.instance_start(ctx=ctx, instance=instance)


def restart_postgresql(
    ctx: "Context",
    instance: system.Instance,
    *,
    mode: PostgreSQLStopMode = "fast",
    wait: bool = True,
) -> None:
    restarted = ctx.hook.restart_service(
        ctx=ctx,
        service=ctx.hook.postgresql_service_name(ctx=ctx, instance=instance),
        name=instance.qualname,
    )
    if restarted:
        postgresql.wait_ready(ctx, instance)
    else:
        ctx.hook.restart_postgresql(ctx=ctx, instance=instance, mode=mode, wait=wait)


def reload(ctx: "Context", instance: system.PostgreSQLInstance) -> None:
    """Reload an instance."""
    ctx.hook.reload_postgresql(ctx=ctx, instance=instance)


def promote(ctx: "Context", instance: system.PostgreSQLInstance) -> None:
    """Promote a standby instance"""
    if not instance.standby:
        raise exceptions.InstanceStateError(f"{instance} is not a standby")
    ctx.hook.promote_postgresql(ctx=ctx, instance=instance)


@task("upgrading PostgreSQL instance")
def upgrade(
    ctx: "Context",
    instance: system.Instance,
    *,
    version: Optional[str] = None,
    name: Optional[str] = None,
    port: Optional[int] = None,
    jobs: Optional[int] = None,
    _instance_model: Optional[Type[interface.Instance]] = None,
) -> system.Instance:
    """Upgrade a primary instance using pg_upgrade"""
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    if version is None:
        version = system.default_postgresql_version(ctx)
    if (name is None or name == instance.name) and version == instance.version:
        raise exceptions.InvalidVersion(
            f"Could not upgrade {instance} using same name and same version"
        )
    # check if target name/version already exists
    if exists(ctx, name=(instance.name if name is None else name), version=version):
        raise exceptions.InstanceAlreadyExists(
            f"Could not upgrade {instance}: target name/version instance already exists"
        )

    if not ctx.confirm(
        f"Confirm upgrade of instance {instance} to version {version}?", True
    ):
        raise exceptions.Cancelled(f"upgrade of instance {instance} cancelled")

    postgresql_settings = ctx.settings.postgresql
    surole = postgresql_settings.surole
    surole_password = postgresql_settings.libpq_environ(ctx, instance, surole.name).get(
        "PGPASSWORD"
    )
    if not surole_password and surole.pgpass:
        passfile = pgpass.parse(ctx.settings.postgresql.auth.passfile)
        for entry in passfile:
            if entry.matches(port=instance.port, username=surole.name):
                surole_password = entry.password
    if _instance_model is None:
        _instance_model = interface.Instance.composite(ctx.pm)
    new_manifest = _instance_model.parse_obj(
        dict(
            _get(ctx, instance),
            name=name or instance.name,
            version=version,
            port=port or instance.port,
            state=interface.InstanceState.stopped,
            surole_password=SecretStr(surole_password) if surole_password else None,
        )
    )
    newinstance = init(ctx, new_manifest)
    configure(ctx, new_manifest, _creating=True, run_hooks=False)
    pg_upgrade = str(newinstance.bindir / "pg_upgrade")
    cmd = [
        pg_upgrade,
        f"--old-bindir={instance.bindir}",
        f"--new-bindir={newinstance.bindir}",
        f"--old-datadir={instance.datadir}",
        f"--new-datadir={newinstance.datadir}",
        f"--username={ctx.settings.postgresql.surole.name}",
    ]
    if jobs is not None:
        cmd.extend(["--jobs", str(jobs)])
    env = postgresql_settings.libpq_environ(
        ctx, instance, ctx.settings.postgresql.surole.name
    )
    if surole_password:
        env.setdefault("PGPASSWORD", surole_password)
    with tempfile.TemporaryDirectory() as tmpdir:
        ctx.run(cmd, check=True, cwd=tmpdir, env=env)
    ctx.hook.instance_upgrade(ctx=ctx, old=instance, new=newinstance)
    apply(ctx, new_manifest, _creating=True, _upgrading_from=instance)
    return system.Instance.system_lookup(ctx, newinstance)


@upgrade.revert("dropping upgraded instance")
def revert_upgrade(
    ctx: "Context",
    instance: system.Instance,
    *,
    version: Optional[str] = None,
    name: Optional[str] = None,
    port: Optional[int] = None,
    jobs: Optional[int] = None,
    _instance_model: Optional[Type[interface.Instance]] = None,
) -> None:
    newinstance = system.Instance.system_lookup(ctx, (name or instance.name, version))
    drop(ctx, newinstance)


def get_locale(cnx: db.Connection) -> Optional[str]:
    """Return the value of instance locale.

    If locale subcategories are set to distinct values, return None.
    """
    locales = {s.name: s.setting for s in settings(cnx) if s.name.startswith("lc_")}
    values = set(locales.values())
    if len(values) == 1:
        return values.pop()
    else:
        logger.debug(
            "cannot determine instance locale, settings are heterogeneous: %s",
            ", ".join(f"{n}: {s}" for n, s in sorted(locales.items())),
        )
        return None


def apply(
    ctx: "Context",
    instance: interface.Instance,
    *,
    _creating: bool = False,
    _upgrading_from: Optional[system.Instance] = None,
) -> interface.InstanceApplyResult:
    """Apply state described by interface model as a PostgreSQL instance.

    Depending on the previous state and existence of the target instance, the
    instance may be created or updated or dropped.

    If configuration changes are detected and the instance was previously
    running, the server will be reloaded automatically; if a restart is
    needed, the user will be prompted in case of interactive usage or this
    will be performed automatically if 'restart_on_changes' is set to True.
    """
    States = interface.InstanceState
    state = instance.state
    if state == States.absent:
        dropped = False
        if exists(ctx, instance.name, instance.version):
            drop(
                ctx,
                system.Instance.system_lookup(ctx, (instance.name, instance.version)),
            )
            dropped = True
        return interface.InstanceApplyResult(
            change_state=interface.ApplyChangeState.dropped if dropped else None,
        )

    changed = False
    try:
        sys_instance = system.PostgreSQLInstance.system_lookup(
            ctx, (instance.name, instance.version)
        )
    except exceptions.InstanceNotFound:
        _creating = True
        interface.validate_ports(instance)
        sys_instance = init(ctx, instance)
        changed = True

    instance_is_running = postgresql.is_running(ctx, sys_instance)

    with configure_context(
        ctx, instance, creating=_creating, upgrading_from=_upgrading_from
    ) as changes:
        if state in (States.started, States.restarted) and not instance_is_running:
            _start_postgresql(ctx, sys_instance)
            instance_is_running = True
        if _creating:
            # Now that PostgreSQL configuration is done, call hooks for
            # super-user role creation (handled by initdb), e.g. to create the
            # .pgpass entry.
            surole = instance.surole(ctx.settings)
            ctx.hook.role_change(ctx=ctx, role=surole, instance=instance)
            if not sys_instance.standby:  # standby instances are read-only
                with postgresql.running(ctx, sys_instance):
                    replrole = instance.replrole(ctx.settings)
                    roles.apply(ctx, sys_instance, replrole)
                    for role in ctx.hook.role(settings=ctx.settings, manifest=instance):
                        roles.apply(ctx, sys_instance, role)
                    for database in ctx.hook.database(
                        settings=ctx.settings, manifest=instance
                    ):
                        databases.apply(ctx, sys_instance, database)
    changed = changed or bool(changes)

    sys_instance = system.Instance.system_lookup(ctx, sys_instance)

    if instance.data_checksums is not None:
        actual_data_checksums = get_data_checksums(ctx, sys_instance)
        if actual_data_checksums != instance.data_checksums:
            if instance.data_checksums:
                logger.info("enabling data checksums")
            else:
                logger.info("disabling data checksums")
            set_data_checksums(ctx, sys_instance, instance.data_checksums)
            changed = True

    if state == States.stopped:
        if instance_is_running:
            stop(ctx, sys_instance)
            changed = True
            instance_is_running = False
    elif state in (States.started, States.restarted):
        if state == States.started:
            start(ctx, sys_instance, _warn=False)
        elif state == States.restarted:
            restart(ctx, sys_instance)
        changed = True
        instance_is_running = True
    else:
        assert False, f"unexpected state: {state}"  # pragma: nocover

    StandbyState = Standby.State
    standby = instance.standby

    if (
        standby
        and standby.status == StandbyState.promoted
        and sys_instance.standby is not None
    ):
        promote(ctx, sys_instance)

    if not sys_instance.standby:
        with postgresql.running(ctx, sys_instance):
            for a_role in instance.roles:
                changed = (
                    roles.apply(ctx, sys_instance, a_role).change_state
                    in (
                        interface.ApplyChangeState.created,
                        interface.ApplyChangeState.changed,
                    )
                    or changed
                )
            for a_database in instance.databases:
                changed = (
                    databases.apply(ctx, sys_instance, a_database).change_state
                    in (
                        interface.ApplyChangeState.changed,
                        interface.ApplyChangeState.created,
                    )
                    or changed
                )
    change_state, p_restart = None, False
    if _creating:
        change_state = interface.ApplyChangeState.created
    elif changed:
        change_state = interface.ApplyChangeState.changed
        if instance_is_running:
            with db.connect(ctx, sys_instance) as cnx:
                p_restart = pending_restart(cnx)
    return interface.InstanceApplyResult(
        change_state=change_state, pending_restart=p_restart
    )


def pending_restart(cnx: db.Connection) -> bool:
    """Return True if the instance is pending a restart to account for configuration changes."""
    with cnx, cnx.cursor(row_factory=psycopg.rows.args_row(bool)) as cur:
        cur.execute("SELECT bool_or(pending_restart) FROM pg_settings")
        row = cur.fetchone()
        assert row is not None
        return row


def check_pending_actions(
    ctx: "Context",
    instance: system.Instance,
    changes: ConfigChanges,
    restart_on_changes: bool,
) -> None:
    """Check if any of the changes require a reload or a restart.

    The instance is automatically reloaded if needed.
    The user is prompted for confirmation if a restart is needed.
    """
    if not postgresql.is_running(ctx, instance):
        return

    if "port" in changes:
        needs_restart = True
    else:
        needs_restart = False
        pending_restart = set()
        pending_reload = set()
        with db.connect(ctx, instance) as cnx:
            for p in settings(cnx):
                pname = p.name
                if pname not in changes:
                    continue
                if p.context == "postmaster":
                    pending_restart.add(pname)
                else:
                    pending_reload.add(pname)

        if pending_reload:
            logger.info(
                "instance %s needs reload due to parameter changes: %s",
                instance,
                ", ".join(sorted(pending_reload)),
            )
            reload(ctx, instance)

        if pending_restart:
            logger.warning(
                "instance %s needs restart due to parameter changes: %s",
                instance,
                ", ".join(sorted(pending_restart)),
            )
            needs_restart = True

    if needs_restart and ctx.confirm(
        "PostgreSQL needs to be restarted; restart now?", restart_on_changes
    ):
        restart_postgresql(ctx, instance)


def get(ctx: "Context", instance: system.Instance) -> interface.Instance:
    """Return a interface Instance model from a system Instance."""
    if not postgresql.is_running(ctx, instance):
        missing_bits = [
            "locale",
            "encoding",
            "passwords",
            "pending_restart",
        ]
        if instance.standby is not None:
            missing_bits.append("replication lag")
        logger.warning(
            "instance %s is not running, information about %s may not be accurate",
            instance,
            f"{', '.join(missing_bits[:-1])} and {missing_bits[-1]}",
        )
    return _get(ctx, instance)


def _get(ctx: "Context", instance: system.Instance) -> interface.Instance:
    config = instance.config()
    managed_config = config.as_dict()
    managed_config.pop("port", None)
    st = postgresql.status(ctx, instance)
    state = interface.InstanceState.from_pg_status(st)
    instance_is_running = st == postgresql.Status.running
    services = {
        s.__class__.__service__: s
        for s in ctx.hook.get(ctx=ctx, instance=instance)
        if s is not None
    }

    standby = None
    if instance.standby:
        try:
            standby = ctx.hook.standby_model(
                ctx=ctx,
                instance=instance,
                standby=instance.standby,
                running=instance_is_running,
            )
        except ValueError:
            pass

    locale = None
    encoding = None
    data_checksums = None
    pending_rst = False
    if instance_is_running:
        with db.connect(ctx, instance, dbname="template1") as cnx:
            locale = get_locale(cnx)
            encoding = databases.encoding(cnx)
            data_checksums = show_data_checksums(cnx)
            pending_rst = pending_restart(cnx)
    else:
        try:
            data_checksums = get_data_checksums(ctx, instance)
        except exceptions.UnsupportedError as e:
            logger.warning(str(e))

    return interface.Instance(
        name=instance.name,
        version=instance.version,
        port=instance.port,
        state=state,
        pending_restart=pending_rst,
        settings=managed_config,
        locale=locale,
        encoding=encoding,
        data_checksums=data_checksums,
        standby=standby,
        data_directory=instance.datadir,
        wal_directory=instance.waldir,
        **services,
    )


def drop(ctx: "Context", instance: system.Instance) -> None:
    """Drop an instance."""
    logger.info("dropping instance %s", instance)
    if not ctx.confirm(f"Confirm complete deletion of instance {instance}?", True):
        raise exceptions.Cancelled(f"deletion of instance {instance} cancelled")

    stop(ctx, instance, mode="immediate", deleting=True)

    ctx.hook.instance_drop(ctx=ctx, instance=instance)
    for rolename in ctx.hook.rolename(settings=ctx.settings):
        ctx.hook.role_change(
            ctx=ctx,
            role=interface.Role(name=rolename, state=interface.PresenceState.absent),
            instance=instance,
        )
    manifest = interface.Instance(name=instance.name, version=instance.version)
    revert_init(ctx, manifest)


def list(
    ctx: "Context", *, version: Optional[PostgreSQLVersion] = None
) -> Iterator[interface.InstanceListItem]:
    """Yield instances found by system lookup.

    :param version: filter instances matching a given version.

    :raises ~exceptions.InvalidVersion: if specified version is unknown.
    """
    for instance in system_list(ctx, version=version):
        yield interface.InstanceListItem(
            name=instance.name,
            datadir=instance.datadir,
            port=instance.port,
            status=postgresql.status(ctx, instance).name,
            version=instance.version,
        )


def system_list(
    ctx: "Context", *, version: Optional[PostgreSQLVersion] = None
) -> Iterator[system.PostgreSQLInstance]:
    if version is not None:
        assert isinstance(version, PostgreSQLVersion)
        versions = [version.value]
    else:
        versions = [v.version for v in ctx.settings.postgresql.versions]

    # Search for directories matching datadir template globing on the {name}
    # part. Since the {version} part may come after or before {name}, we first
    # build a datadir for each known version and split it on {name} for
    # further globbing.
    name_idx = ctx.settings.postgresql.datadir.parts.index("{name}")
    for ver in versions:
        version_path = Path(
            str(ctx.settings.postgresql.datadir).format(name="*", version=ver)
        )
        prefix = Path(*version_path.parts[:name_idx])
        suffix = Path(*version_path.parts[name_idx + 1 :])
        pattern = f"*/{suffix}"
        for d in sorted(prefix.glob(pattern)):
            if not d.is_dir():
                continue
            name = d.relative_to(prefix).parts[0]
            try:
                yield system.PostgreSQLInstance.system_lookup(ctx, (name, ver))
            except exceptions.InstanceNotFound:
                pass


def env_for(
    ctx: "Context", instance: system.Instance, *, path: bool = False
) -> Dict[str, str]:
    """Return libpq environment variables suitable to connect to `instance`.

    If 'path' is True, also inject PostgreSQL binaries directory in PATH.
    """
    postgresql_settings = ctx.settings.postgresql
    env = postgresql_settings.libpq_environ(
        ctx, instance, postgresql_settings.surole.name, base={}
    )
    config = instance.config()
    try:
        host = config.unix_socket_directories.split(",")[0]  # type: ignore[union-attr]
    except (AttributeError, IndexError):
        host = "localhost"
    env.update(
        {
            "PGUSER": ctx.settings.postgresql.surole.name,
            "PGPORT": str(instance.port),
            "PGHOST": host,
            "PGDATA": str(instance.datadir),
            "PSQLRC": str(instance.psqlrc),
            "PSQL_HISTORY": str(instance.psql_history),
        }
    )
    if path:
        env["PATH"] = ":".join(
            [str(instance.bindir)]
            + ([os.environ["PATH"]] if "PATH" in os.environ else [])
        )
    for env_vars in ctx.hook.instance_env(ctx=ctx, instance=instance):
        env.update(env_vars)
    return env


def exec(ctx: "Context", instance: system.Instance, command: Tuple[str, ...]) -> None:
    """Execute given PostgreSQL command in the libpq environment for `instance`.

    The command to be executed is looked up for in PostgreSQL binaries directory.
    """
    env = os.environ.copy()
    env.update(env_for(ctx, instance))
    progname, *args = command
    program = Path(progname)
    if not program.is_absolute():
        program = instance.bindir / program
        if not program.exists():
            ppath = shutil.which(progname)
            if ppath is None:
                raise exceptions.FileNotFoundError(progname)
            program = Path(ppath)
    try:
        cmd.execute_program([str(program)] + args, env=env)
    except FileNotFoundError as e:
        raise exceptions.FileNotFoundError(str(e))


def env(ctx: "Context", instance: system.Instance) -> str:
    return "\n".join(
        [
            f"export {key}={value}"
            for key, value in sorted(env_for(ctx, instance, path=True).items())
        ]
    )


def exists(ctx: "Context", name: str, version: Optional[str]) -> bool:
    """Return true when instance exists"""
    try:
        system.PostgreSQLInstance.system_lookup(ctx, (name, version))
    except exceptions.InstanceNotFound:
        return False
    return True


def settings(cnx: db.Connection) -> List[interface.PGSetting]:
    """Return the list of run-time parameters of the server, as available in
    pg_settings view.
    """
    with cnx.cursor(row_factory=psycopg.rows.class_row(interface.PGSetting)) as cur:
        cur.execute(interface.PGSetting._query)
        return cur.fetchall()


def logs(ctx: "Context", instance: system.PostgreSQLInstance) -> Iterator[str]:
    """Return the content of current log file as an iterator.

    :raises ~exceptions.FileNotFoundError: if the current log file, matching
        configured log_destination, is not found.
    :raises ~exceptions.SystemError: if the current log file cannot be opened
        for reading.
    :raises ValueError: if no record matching configured log_destination is
        found in current_logfiles (this indicates a misconfigured instance).
    """
    config = instance.config()
    log_destination = config.get("log_destination", "stderr")
    current_logfiles = instance.datadir / "current_logfiles"
    if not current_logfiles.exists():
        raise exceptions.FileNotFoundError(
            f"file 'current_logfiles' for instance {instance} not found"
        )
    with current_logfiles.open() as f:
        for line in f:
            destination, logfilelocation = line.strip().split(None, maxsplit=1)
            if destination == log_destination:
                break
        else:
            raise ValueError(
                f"no record matching '{log_destination}' log destination found for instance {instance}"
            )

    logfile = Path(logfilelocation)
    if not logfile.is_absolute():
        logfile = instance.datadir / logfile

    logger.info("reading logs of instance '%s' from %s", instance, logfile)
    try:
        with logfile.open() as f:
            yield from f
    except OSError:
        raise exceptions.SystemError(f"failed to read {logfile} on instance {instance}")
