import logging
from typing import TYPE_CHECKING, Any, List

import psycopg.pq
import psycopg.rows
from pgtoolkit import pgpass
from psycopg import sql

from . import databases, db, exceptions
from .models import interface
from .types import Role

if TYPE_CHECKING:
    from .ctx import Context
    from .models import system

logger = logging.getLogger(__name__)


def apply(
    ctx: "Context", instance: "system.PostgreSQLInstance", role: interface.Role
) -> interface.ApplyResult:
    """Apply state described by specified interface model as a PostgreSQL role.

    In case it's not possible to inspect changed role, possibly due to the super-user
    password being modified, change_state attribute within the returned object
    is set to interface.ApplyResult.changed with a warning logged.

    The instance should be running.

    :raises ~pglift.exceptions.DependencyError: if the role cannot be dropped due some database dependency.
    """
    name = role.name
    if role.state == interface.PresenceState.absent:
        dropped = False
        if exists(ctx, instance, name):
            drop(ctx, instance, role)
            dropped = True
        return interface.ApplyResult(
            change_state=interface.ApplyChangeState.dropped if dropped else None
        )

    if not exists(ctx, instance, name):
        create(ctx, instance, role)
        ctx.hook.role_change(ctx=ctx, role=role, instance=instance)
        return interface.ApplyResult(change_state=interface.ApplyChangeState.created)
    else:
        actual = get(ctx, instance, name, password=False)
        alter(ctx, instance, role)
        if any(ctx.hook.role_change(ctx=ctx, role=role, instance=instance)):
            return interface.ApplyResult(
                change_state=interface.ApplyChangeState.changed
            )
        try:
            return interface.ApplyResult(
                change_state=(
                    interface.ApplyChangeState.changed
                    if (get(ctx, instance, name, password=False) != actual)
                    else None
                )
            )
        except psycopg.OperationalError as e:
            logger.warning(
                "failed to retrieve new role %s, possibly due to password being modified: %s",
                name,
                e,
            )
            return interface.ApplyResult(
                change_state=interface.ApplyChangeState.changed
            )


def get(
    ctx: "Context",
    instance: "system.PostgreSQLInstance",
    name: str,
    *,
    password: bool = True,
) -> interface.Role:
    """Return the role object with specified name.

    :raises ~pglift.exceptions.RoleNotFound: if no role with specified 'name' exists.
    """
    if not exists(ctx, instance, name):
        raise exceptions.RoleNotFound(name)
    with db.connect(ctx, instance) as cnx:
        values = cnx.execute(db.query("role_inspect"), {"username": name}).fetchone()
        assert values is not None
    if in_pgpass(ctx, instance, name):
        values["pgpass"] = True
    if not password:
        values["password"] = None
    return interface.Role(**values)


def list(ctx: "Context", instance: "system.PostgreSQLInstance") -> List[interface.Role]:
    """Return the list of roles for an instance."""
    with db.connect(ctx, instance) as cnx:
        rows = cnx.execute(db.query("role_list")).fetchall()
        return [
            interface.Role(**r, pgpass=in_pgpass(ctx, instance, r["name"]))
            for r in rows
        ]


def drop(
    ctx: "Context",
    instance: "system.PostgreSQLInstance",
    role: interface.RoleDropped,
) -> None:
    """Drop a role from instance.

    :raises ~pglift.exceptions.RoleNotFound: if no role with specified 'role.name' exists.
    :raises ~pglift.exceptions.RoleNotFound: if no role with specified 'role.reassign_owned' exists.
    :raises ~pglift.exceptions.DependencyError: if the role cannot be dropped due some database dependency.
    """
    logger.info("dropping role '%s' from instance %s", role.name, instance)
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    if not exists(ctx, instance, role.name):
        raise exceptions.RoleNotFound(role.name)
    if role.reassign_owned and not exists(ctx, instance, role.reassign_owned):
        raise exceptions.RoleNotFound(role.reassign_owned)

    dbs_to_drop: List[str] = []
    if role.drop_owned or role.reassign_owned:
        for database in databases.list(ctx, instance):
            if role.drop_owned and database.owner == role.name:
                dbs_to_drop.append(database.name)
            else:
                if role.drop_owned:
                    query = db.query(
                        "role_drop_owned", username=sql.Identifier(role.name)
                    )
                elif role.reassign_owned:
                    query = db.query(
                        "role_drop_reassign",
                        oldowner=sql.Identifier(role.name),
                        newowner=sql.Identifier(role.reassign_owned),
                    )
                with db.connect(ctx, instance, dbname=database.name) as cnx:
                    cnx.execute(query)

    with db.connect(ctx, instance) as cnx:
        for dbname in dbs_to_drop:
            cnx.execute(
                db.query(
                    "database_drop",
                    database=sql.Identifier(dbname),
                    options=sql.SQL(""),
                )
            )
        try:
            cnx.execute(db.query("role_drop", username=sql.Identifier(role.name)))
        except psycopg.errors.DependentObjectsStillExist as e:
            assert (
                not role.drop_owned and not role.reassign_owned
            ), f"unexpected {e!r} while dropping {role}"
            raise exceptions.DependencyError(
                f"{e.diag.message_primary} (detail: {e.diag.message_detail})"
            ) from None

    ctx.hook.role_change(ctx=ctx, role=role, instance=instance)


def exists(ctx: "Context", instance: "system.PostgreSQLInstance", name: str) -> bool:
    """Return True if named role exists in 'instance'.

    The instance should be running.
    """
    with db.connect(ctx, instance) as cnx:
        cur = cnx.execute(db.query("role_exists"), {"username": name})
        return cur.rowcount == 1


def encrypt_password(cnx: psycopg.Connection[Any], role: Role) -> str:
    assert role.password is not None, "role has no password to encrypt"
    encoding = cnx.info.encoding
    return cnx.pgconn.encrypt_password(
        role.password.get_secret_value().encode(encoding), role.name.encode(encoding)
    ).decode(encoding)


def options(
    cnx: psycopg.Connection[Any],
    role: interface.Role,
    *,
    in_roles: bool = True,
) -> sql.Composable:
    """Return the "options" part of CREATE ROLE or ALTER ROLE SQL commands
    based on 'role' model.
    """
    opts: List[sql.Composable] = [
        sql.SQL("INHERIT" if role.inherit else "NOINHERIT"),
        sql.SQL("LOGIN" if role.login else "NOLOGIN"),
        sql.SQL("SUPERUSER" if role.superuser else "NOSUPERUSER"),
        sql.SQL("REPLICATION" if role.replication else "NOREPLICATION"),
    ]
    if role.password is not None:
        opts.append(sql.SQL("PASSWORD {}").format(encrypt_password(cnx, role)))
    if role.validity is not None:
        opts.append(sql.SQL("VALID UNTIL {}").format(role.validity.isoformat()))
    opts.append(
        sql.SQL(
            "CONNECTION LIMIT {}".format(
                role.connection_limit if role.connection_limit is not None else -1
            )
        )
    )
    if in_roles and role.in_roles:
        opts.append(
            sql.SQL(" ").join(
                [
                    sql.SQL("IN ROLE"),
                    sql.SQL(", ").join(
                        sql.Identifier(in_role) for in_role in role.in_roles
                    ),
                ]
            )
        )
    return sql.SQL(" ").join(opts)


def create(
    ctx: "Context", instance: "system.PostgreSQLInstance", role: interface.Role
) -> None:
    """Create 'role' in 'instance'.

    The instance should be a running primary and the role should not exist already.
    """
    logger.info("creating role '%s' on instance %s", role.name, instance)
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    with db.connect(ctx, instance) as cnx:
        opts = options(cnx, role)
        cnx.execute(
            db.query("role_create", username=sql.Identifier(role.name), options=opts)
        )


def alter(
    ctx: "Context", instance: "system.PostgreSQLInstance", role: interface.Role
) -> None:
    """Alter 'role' in 'instance'.

    The instance should be running primary and the role should exist already.
    """
    logger.info("altering role '%s' on instance %s", role.name, instance)
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    actual_role = get(ctx, instance, role.name)
    in_roles = {
        "grant": set(role.in_roles) - set(actual_role.in_roles),
        "revoke": set(actual_role.in_roles) - set(role.in_roles),
    }
    with db.connect(ctx, instance) as cnx, cnx.transaction():
        opts = options(cnx, role, in_roles=False)
        cnx.execute(
            db.query(
                "role_alter",
                username=sql.Identifier(role.name),
                options=opts,
            ),
        )
        for action, values in in_roles.items():
            if values:
                cnx.execute(
                    db.query(
                        f"role_{action}",
                        rolname=sql.SQL(", ").join(sql.Identifier(r) for r in values),
                        rolspec=sql.Identifier(role.name),
                    )
                )


def set_password_for(
    ctx: "Context", instance: "system.PostgreSQLInstance", role: Role
) -> None:
    """Set password for a PostgreSQL role on a primary instance."""
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    if role.password is None:
        return

    logger.info("setting password for '%(username)s' role", {"username": role.name})
    with db.connect(ctx, instance) as conn:
        options = sql.SQL("PASSWORD {}").format(encrypt_password(conn, role))
        conn.execute(
            db.query("role_alter", username=sql.Identifier(role.name), options=options),
        )


def in_pgpass(ctx: "Context", instance: "system.PostgreSQLInstance", name: str) -> bool:
    """Return True if a role with 'name' is present in password file for
    'instance'.
    """
    passfile_path = ctx.settings.postgresql.auth.passfile
    if not passfile_path.exists():
        return False
    port = int(instance.config().port)  # type: ignore[arg-type]
    passfile = pgpass.parse(passfile_path)
    return any(entry.matches(username=name, port=port) for entry in passfile)
