from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from deprecated import (
    deprecated,
)
from enum import (
    Enum,
)
from fa_purity.cmd import (
    Cmd,
)
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
from typing import (
    Any,
    cast,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from psycopg2 import (
        connection as ConnectionStub,
    )
else:
    ConnectionStub = Any


@dataclass(frozen=True)
class DatabaseId:
    db_name: str
    host: str
    port: int


@dataclass(frozen=True)
class Credentials:
    user: str
    password: str

    def __repr__(self) -> str:
        return f"Creds(user={self.user})"


class IsolationLvl(Enum):
    AUTOCOMMIT = postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT
    READ_UNCOMMITTED = postgres_extensions.ISOLATION_LEVEL_READ_UNCOMMITTED
    READ_COMMITTED = postgres_extensions.ISOLATION_LEVEL_READ_COMMITTED
    REPEATABLE_READ = postgres_extensions.ISOLATION_LEVEL_REPEATABLE_READ
    SERIALIZABLE = postgres_extensions.ISOLATION_LEVEL_SERIALIZABLE


@dataclass(frozen=True)
class _DbConnection:
    _connection: ConnectionStub


@dataclass(frozen=True)
class DbConnection:
    _inner: _DbConnection

    def close(self) -> Cmd[None]:
        return Cmd.from_cmd(lambda: cast(None, self._inner._connection.close()))  # type: ignore[no-untyped-call]

    def commit(self) -> Cmd[None]:
        return Cmd.from_cmd(lambda: cast(None, self._inner._connection.commit()))  # type: ignore[no-untyped-call]

    @staticmethod
    def connect(
        db_id: DatabaseId,
        creds: Credentials,
        readonly: bool,
        isolation: IsolationLvl,
    ) -> Cmd[DbConnection]:
        def _action() -> DbConnection:
            connection = postgres.connect(
                dbname=db_id.db_name,
                user=creds.user,
                password=creds.password,
                host=db_id.host,
                port=db_id.port,
            )
            connection.set_session(readonly=readonly)  # type: ignore[no-untyped-call]
            connection.set_isolation_level(isolation.value)  # type: ignore[no-untyped-call]
            draft = _DbConnection(connection)
            return DbConnection(draft)

        return Cmd.from_cmd(_action)


connect = deprecated(reason="Use DbConnection.connect instead")(
    DbConnection.connect
)
