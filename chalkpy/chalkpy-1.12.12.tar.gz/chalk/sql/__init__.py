from os import PathLike
from typing import Optional, Union, overload

from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.integrations.bigquery import BigQuerySourceImpl
from chalk.sql._internal.integrations.cloudsql import CloudSQLSourceImpl
from chalk.sql._internal.integrations.mysql import MySQLSourceImpl
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.sql._internal.integrations.redshift import RedshiftSourceImpl
from chalk.sql._internal.integrations.snowflake import SnowflakeSourceImpl
from chalk.sql._internal.integrations.sqlite import SQLiteFileSourceImpl, SQLiteInMemorySourceImpl
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import (
    BaseSQLSourceProtocol,
    ChalkQueryProtocol,
    SQLSourceWithTableIngestProtocol,
    StringChalkQueryProtocol,
    TableIngestProtocol,
)


@overload
def SnowflakeSource(*, name: str) -> BaseSQLSourceProtocol:
    ...


@overload
def SnowflakeSource(
    *,
    account_identifier: str = ...,
    warehouse: str = ...,
    user: str = ...,
    password: str = ...,
    db: str = ...,
    schema: str = ...,
    role: str = ...,
) -> BaseSQLSourceProtocol:
    ...


def SnowflakeSource(
    *,
    name: Optional[str] = None,
    account_identifier: Optional[str] = None,
    warehouse: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    db: Optional[str] = None,
    schema: Optional[str] = None,
    role: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return SnowflakeSourceImpl(
        name=name,
        account_identifier=account_identifier,
        warehouse=warehouse,
        user=user,
        password=password,
        db=db,
        schema=schema,
        role=role,
    )


@overload
def PostgreSQLSource(
    *,
    host: str = ...,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
) -> SQLSourceWithTableIngestProtocol:
    ...


@overload
def PostgreSQLSource(*, name: str) -> SQLSourceWithTableIngestProtocol:
    ...


def PostgreSQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
) -> TableIngestProtocol:
    return PostgreSQLSourceImpl(host, port, db, user, password, name)


@overload
def MySQLSource(
    *,
    host: str = ...,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
) -> SQLSourceWithTableIngestProtocol:
    ...


@overload
def MySQLSource(*, name: str) -> SQLSourceWithTableIngestProtocol:
    ...


def MySQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
) -> SQLSourceWithTableIngestProtocol:
    return MySQLSourceImpl(host, port, db, user, password, name)


def SQLiteInMemorySource(name: Optional[str] = None) -> SQLSourceWithTableIngestProtocol:
    return SQLiteInMemorySourceImpl(name)


def SQLiteFileSource(filename: Union[str, PathLike], name: Optional[str] = None) -> SQLSourceWithTableIngestProtocol:
    return SQLiteFileSourceImpl(filename, name)


@overload
def RedshiftSource(
    *,
    host: str = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
) -> BaseSQLSourceProtocol:
    ...


@overload
def RedshiftSource(*, name: str) -> BaseSQLSourceProtocol:
    ...


@overload
def RedshiftSource() -> BaseSQLSourceProtocol:
    ...


def RedshiftSource(
    *,
    host: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return RedshiftSourceImpl(host, db, user, password, name)


@overload
def BigQuerySource() -> BaseSQLSourceProtocol:
    ...


@overload
def BigQuerySource(*, name: str) -> BaseSQLSourceProtocol:
    ...


def BigQuerySource(
    *,
    name: Optional[str] = None,
    project: Optional[str] = None,
    dataset: Optional[str] = None,
    location: Optional[str] = None,
    credentials_base64: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return BigQuerySourceImpl(
        name=name,
        project=project,
        dataset=dataset,
        location=location,
        credentials_base64=credentials_base64,
        credentials_path=credentials_path,
    )


@overload
def CloudSQLSource() -> BaseSQLSourceProtocol:
    ...


@overload
def CloudSQLSource(*, name: str) -> BaseSQLSourceProtocol:
    ...


def CloudSQLSource(
    *,
    name: Optional[str] = None,
    instance_name: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return CloudSQLSourceImpl(
        name=name,
        instance_name=instance_name,
        db=db,
        user=user,
        password=password,
    )


__all__ = [
    "BaseSQLSourceProtocol",
    "BigQuerySource",
    "CloudSQLSource",
    "MySQLSource",
    "PostgreSQLSource",
    "RedshiftSource",
    "SQLiteFileSource",
    "SQLiteInMemorySource",
    "SnowflakeSource",
    "FinalizedChalkQuery",
    "ChalkQueryProtocol",
    "StringChalkQueryProtocol",
    "TableIngestProtocol",
    "SQLSourceWithTableIngestProtocol",
    "IncrementalSettings",
]
