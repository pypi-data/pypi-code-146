import functools
import importlib.resources
import logging
import re
import sys
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Iterator, Optional, Tuple

import psycopg.conninfo
import psycopg.errors
import psycopg.rows
from psycopg import sql

from . import __name__ as pkgname

if TYPE_CHECKING:  # pragma: nocover
    from .ctx import Context
    from .models.system import PostgreSQLInstance, Standby
    from .settings import PostgreSQLSettings

Connection = psycopg.Connection[psycopg.rows.DictRow]
logger = logging.getLogger(__name__)


def query(name: str, **kwargs: sql.Composable) -> sql.Composed:
    for qname, qstr in queries():
        if qname == name:
            return sql.SQL(qstr).format(**kwargs)
    raise ValueError(name)


def queries() -> Iterator[Tuple[str, str]]:
    content = importlib.resources.read_text(pkgname, "queries.sql")
    for block in re.split("-- name:", content):
        block = block.strip()
        if not block:
            continue
        qname, query = block.split("\n", 1)
        yield qname.strip(), query.strip()


def dsn(
    instance: "PostgreSQLInstance", settings: "PostgreSQLSettings", **kwargs: Any
) -> str:
    for badarg in ("port", "passfile", "host"):
        if badarg in kwargs:
            raise TypeError(f"unexpected '{badarg}' argument")

    kwargs["port"] = instance.port
    config = instance.config()
    if config.unix_socket_directories:
        kwargs["host"] = config.unix_socket_directories
    passfile = settings.auth.passfile
    if passfile.exists():
        kwargs["passfile"] = str(passfile)

    assert "dsn" not in kwargs
    return psycopg.conninfo.make_conninfo(**kwargs)


def obfuscate_conninfo(conninfo: str, **kwargs: Any) -> str:
    """Return an obfuscated connection string with password hidden.

    >>> obfuscate_conninfo("user=postgres password=foo")
    'user=postgres password=********'
    >>> obfuscate_conninfo("user=postgres", password="secret")
    'user=postgres password=********'
    >>> obfuscate_conninfo("port=5444")
    'port=5444'
    """
    params = psycopg.conninfo.conninfo_to_dict(conninfo, **kwargs)
    if "password" in params:
        params["password"] = "*" * 8
    return psycopg.conninfo.make_conninfo(**params)


@contextmanager
def connect_dsn(conninfo: str, **kwargs: Any) -> Iterator[Connection]:
    """Connect to specified database of `conninfo` dsn string"""
    logger.debug(
        "connecting to PostgreSQL instance with: %s",
        obfuscate_conninfo(conninfo, **kwargs),
    )
    with psycopg.connect(
        conninfo, autocommit=True, row_factory=psycopg.rows.dict_row, **kwargs
    ) as conn:
        yield conn


@contextmanager
def connect(
    ctx: "Context",
    instance: "PostgreSQLInstance",
    *,
    user: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs: Any,
) -> Iterator[Connection]:
    postgresql_settings = ctx.settings.postgresql
    if user is None:
        user = postgresql_settings.surole.name
        if password is None:
            password = postgresql_settings.libpq_environ(ctx, instance, user).get(
                "PGPASSWORD"
            )

    build_conninfo = functools.partial(
        dsn, instance, postgresql_settings, user=user, **kwargs
    )

    conninfo = build_conninfo(password=password)
    try:
        with connect_dsn(conninfo) as cnx:
            yield cnx
    except psycopg.OperationalError as e:
        if not e.pgconn:
            raise
        if e.pgconn.needs_password:
            password = ctx.prompt(f"Password for user {user}", hide_input=True)
        elif e.pgconn.used_password:
            password = ctx.prompt(
                f"Password for user {user} is incorrect, re-enter a valid one",
                hide_input=True,
            )
        if not password:
            raise
        conninfo = build_conninfo(password=password)
        with connect_dsn(conninfo) as cnx:
            yield cnx


@contextmanager
def primary_connect(
    standby: "Standby", *, dbname: str = "template1", **kwargs: Any
) -> Iterator[Connection]:
    """Connect to the primary of standby."""
    if standby.password:
        kwargs.setdefault("password", standby.password.get_secret_value())
    with connect_dsn(standby.primary_conninfo, dbname=dbname, **kwargs) as cnx:
        yield cnx


def default_notice_handler(diag: psycopg.errors.Diagnostic) -> None:
    if diag.message_primary is not None:
        sys.stderr.write(diag.message_primary + "\n")
