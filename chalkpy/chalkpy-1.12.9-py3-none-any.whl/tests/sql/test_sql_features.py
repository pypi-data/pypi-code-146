from typing import Callable, cast

import pytest
from sqlalchemy import text

from chalk import realtime
from chalk.features import DataFrame, features
from chalk.sql import BaseSQLSourceProtocol
from chalk.testing import assert_frame_equal

try:
    import polars as pl
except ImportError:
    pl = None

seed_db = """
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS friends;

CREATE TABLE users (
    id TEXT,
    name TEXT
);

CREATE TABLE friends_with (
    id INT PRIMARY KEY,
    -- maps to `u_from` feature
    ufrom TEXT,
    -- maps to `u_to` feature
    uto TEXT
);

INSERT INTO users VALUES ('0', 'Wendy'), ('1', 'Shelby');
INSERT INTO friends_with(id, ufrom, uto) VALUES (0, '0', '1'), (1, '1', '2');
"""


@pytest.fixture(scope="module")
def init_db(temp_sqlite_source: BaseSQLSourceProtocol):
    eng = temp_sqlite_source.get_engine()
    with eng.connect() as cnx, cnx.begin():
        for statement in seed_db.split(";"):
            if statement != "":
                cnx.execute(text(statement))


@features
class SQLUserFeatures:
    id: str
    name: str


@features
class SQLFriendsWithRow:
    id: int
    u_from: str
    u_to: str


@pytest.fixture
def resolve_friends_with(temp_sqlite_source: BaseSQLSourceProtocol):
    @realtime
    def resolve_friends_with() -> DataFrame[SQLFriendsWithRow]:
        return cast(
            DataFrame,
            temp_sqlite_source.query_string(
                """
            SELECT * FROM friends_with;
            """
            ).all(),
        )

    return resolve_friends_with


@pytest.fixture
def resolve_sql_users_with_fields(temp_sqlite_source: BaseSQLSourceProtocol):
    @realtime
    def resolve_sql_users_with_fields() -> DataFrame[SQLUserFeatures.id, SQLUserFeatures.name]:
        return cast(
            DataFrame,
            temp_sqlite_source.query_string(
                """
            SELECT id, name FROM users;
            """,
                fields={"id": SQLUserFeatures.id, "name": SQLUserFeatures.name},
            ).all(),
        )

    return resolve_sql_users_with_fields


@pytest.fixture
def resolve_sql_users_without_fields(temp_sqlite_source: BaseSQLSourceProtocol):
    @realtime
    def resolve_sql_users_without_fields() -> DataFrame[SQLUserFeatures.id, SQLUserFeatures.name]:
        return cast(
            DataFrame,
            temp_sqlite_source.query_string(
                """
            SELECT id, name FROM users;
            """
            ).all(),
        )

    return resolve_sql_users_without_fields


@pytest.fixture
def resolve_sql_users_without_fields_all(temp_sqlite_source: BaseSQLSourceProtocol):
    @realtime
    def resolve_sql_users_without_fields_all() -> DataFrame[SQLUserFeatures]:
        return cast(
            DataFrame,
            temp_sqlite_source.query_string(
                """
            SELECT id, name FROM users;
            """
            ).all(),
        )

    return resolve_sql_users_without_fields_all


@pytest.mark.skipif(pl is None, reason="polars is not installed")
def test_sql_resolver_callable(init_db: None, resolve_sql_users_with_fields: Callable[[], DataFrame]):
    users = resolve_sql_users_with_fields()
    assert_frame_equal(users, DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}))


@pytest.mark.skipif(pl is None, reason="polars is not installed")
def test_sql_resolver_no_fields_callable(init_db: None, resolve_sql_users_without_fields: Callable[[], DataFrame]):
    users = resolve_sql_users_without_fields()
    assert_frame_equal(
        users,
        DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}),
    )


@pytest.mark.skipif(pl is None, reason="polars is not installed")
def test_sql_resolver_no_fields_all_callable(
    init_db: None, resolve_sql_users_without_fields_all: Callable[[], DataFrame]
):
    users = resolve_sql_users_without_fields_all()
    assert_frame_equal(
        users,
        DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}),
    )


@pytest.mark.skipif(pl is None, reason="polars is not installed")
def test_sql_resolver_inexact_implicit_mappings(init_db: None, resolve_friends_with: Callable[[], DataFrame]):
    friends_with = resolve_friends_with()
    assert_frame_equal(
        friends_with,
        DataFrame([SQLFriendsWithRow(id=0, u_from="0", u_to="1"), SQLFriendsWithRow(id=1, u_from="1", u_to="2")]),
    )
