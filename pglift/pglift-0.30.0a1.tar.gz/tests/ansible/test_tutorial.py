import datetime
import json
import os
import pathlib
import socket
import subprocess
from typing import Callable, Dict, Iterator, Optional

import psycopg
import pytest
from psycopg.rows import dict_row


@pytest.fixture
def site_settings(
    tmp_path: pathlib.Path,
    pgbackrest_available: bool,
    prometheus_execpath: Optional[pathlib.Path],
    temboard_execpath: Optional[pathlib.Path],
) -> Iterator[pathlib.Path]:
    settings = {
        "prefix": str(tmp_path),
        "run_prefix": str(tmp_path / "run"),
        "postgresql": {
            "auth": {
                "local": "md5",
                "host": "md5",
                "passfile": str(tmp_path / "pgpass"),
            },
            "surole": {"pgpass": True},
            "backuprole": {"pgpass": True},
        },
    }
    if pgbackrest_available:
        settings["pgbackrest"] = {"repository": {"path": str(tmp_path / "pgbackups")}}
    if prometheus_execpath:
        settings["prometheus"] = {"execpath": str(prometheus_execpath)}
    else:
        pytest.skip("prometheus not available")
    if temboard_execpath:
        temboard_signing_key = (
            tmp_path / "etc" / "temboard-agent" / "signing-public.pem"
        )
        settings["temboard"] = {
            "execpath": str(temboard_execpath),
            "ui_url": "https://0.0.0.0:8888",
            "signing_key": str(temboard_signing_key),
        }
        temboard_signing_key.parent.mkdir(parents=True)
        temboard_signing_key.write_text(
            "-----BEGIN PUBLIC KEY-----\n"
            "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChaZFhzRuFgNDLgAJ2+WQsVQ75\n"
            "G9UswuVxTfltxP4mc+ou8lyj7Ck73+M3HkFE2r623g6DZcNYCXqpyNpInsBo68kD\n"
            "IDgwHKaQBTPyve0VhNjkJyqoKIC6AJKv/wixEwsHUm/rNU8cXnY7WCNGjCV+JrEm\n"
            "ekHBWP1X4hFfPKcvvwIDAQAB\n"
            "-----END PUBLIC KEY-----"
        )

    else:
        pytest.skip("temboard not available")

    settings_f = tmp_path / "config.json"
    with settings_f.open("w") as f:
        json.dump(settings, f)

    env = os.environ.copy()
    env["SETTINGS"] = f"@{settings_f}"
    subprocess.run(
        ["pglift", "site-configure", "install"],
        capture_output=True,
        check=True,
        env=env,
    )
    yield settings_f
    subprocess.run(
        ["pglift", "site-configure", "uninstall"],
        capture_output=True,
        check=True,
        env=env,
    )


@pytest.fixture
def call_playbook(
    tmp_path: pathlib.Path,
    ansible_env: Dict[str, str],
    ansible_vault: Callable[[Dict[str, str]], pathlib.Path],
    playdir: pathlib.Path,
    site_settings: pathlib.Path,
) -> Iterator[Callable[[str], None]]:
    env = ansible_env.copy()

    env["SETTINGS"] = f"@{site_settings}"

    vault = ansible_vault(
        {
            "postgresql_surole_password": "supers3kret",
            "prod_bob_password": "s3kret",
            "backup_role_password": "b4ckup",
            "prometheus_role_password": "pr0m3th3u$",
            "temboard_role_password": "temb0@rd",
        }
    )

    def call(playname: str) -> None:
        subprocess.check_call(
            [
                "ansible-playbook",
                "--extra-vars",
                f"@{vault}",
                playdir / playname,
            ],
            env=env,
        )

    yield call

    call("play3.yml")


def cluster_name(dsn: str) -> str:
    with psycopg.connect(dsn, row_factory=dict_row) as cnx:
        cur = cnx.execute("SELECT setting FROM pg_settings WHERE name = 'cluster_name'")
        row = cur.fetchone()
        assert row
        name = row["setting"]
        assert isinstance(name, str), name
        return name


def test(call_playbook: Callable[[str], None]) -> None:
    call_playbook("play1.yml")

    prod_dsn = "host=/tmp user=postgres password=supers3kret dbname=postgres port=5433"
    assert cluster_name(prod_dsn) == "prod"
    with psycopg.connect(prod_dsn, row_factory=dict_row) as cnx:
        cnx.execute("SET TIME ZONE 'UTC'")
        cur = cnx.execute(
            "SELECT rolname,rolinherit,rolcanlogin,rolconnlimit,rolpassword,rolvaliduntil FROM pg_roles WHERE rolname = 'bob'"
        )
        assert cur.fetchone() == {
            "rolname": "bob",
            "rolinherit": True,
            "rolcanlogin": True,
            "rolconnlimit": 10,
            "rolpassword": "********",
            "rolvaliduntil": datetime.datetime(
                2025, 1, 1, tzinfo=datetime.timezone.utc
            ),
        }
        cur = cnx.execute(
            "SELECT r.rolname AS role, ARRAY_AGG(m.rolname ORDER BY m.rolname) AS member_of FROM pg_auth_members JOIN pg_authid m ON pg_auth_members.roleid = m.oid JOIN pg_authid r ON pg_auth_members.member = r.oid GROUP BY r.rolname"
        )
        assert cur.fetchall() == [
            {"role": "bob", "member_of": ["pg_read_all_stats", "pg_signal_backend"]},
            {"role": "peter", "member_of": ["pg_signal_backend"]},
            {
                "role": "pg_monitor",
                "member_of": [
                    "pg_read_all_settings",
                    "pg_read_all_stats",
                    "pg_stat_scan_tables",
                ],
            },
            {"role": "prometheus", "member_of": ["pg_monitor"]},
            {"role": "replication", "member_of": ["pg_read_all_stats"]},
        ]
        libraries = cnx.execute(
            "SELECT setting FROM pg_settings WHERE name = 'shared_preload_libraries';"
        ).fetchone()

    assert libraries is not None
    assert "pg_stat_statements" in libraries["setting"]

    socket.create_connection(("localhost", 9186), 1)
    socket.create_connection(("localhost", 2344), 1)

    # test connection with bob to the db database
    with psycopg.connect(
        "host=/tmp user=bob password=s3kret dbname=db port=5433", row_factory=dict_row
    ) as cnx:
        row = cnx.execute("SHOW work_mem").fetchone()
        extensions = cnx.execute("SELECT extname FROM pg_extension").fetchall()
    assert row is not None
    assert row["work_mem"] == "3MB"
    installed = [r["extname"] for r in extensions]
    assert "unaccent" in installed

    # check preprod cluster & postgres_exporter
    preprod_dsn = "host=/tmp user=postgres password=supers3kret dbname=test port=5434"
    assert cluster_name(preprod_dsn) == "preprod"
    socket.create_connection(("localhost", 9188), 1)
    socket.create_connection(("localhost", 2346), 1)

    # check dev cluster, postgres_exporter and temboard-agent are stopped
    with pytest.raises(psycopg.OperationalError, match="No such file or directory"):
        cluster_name(
            "host=/tmp user=postgres password=supers3kret dbname=postgres port=5444"
        )
    with pytest.raises(ConnectionRefusedError):
        socket.create_connection(("localhost", 9189), 1)
    with pytest.raises(ConnectionRefusedError):
        socket.create_connection(("localhost", 2347), 1)

    call_playbook("play2.yml")

    # prod running
    assert cluster_name(prod_dsn) == "prod"

    # pg_stat_statements extension is uninstalled
    with psycopg.connect(prod_dsn, row_factory=dict_row) as cnx:
        libraries = cnx.execute(
            "SELECT setting FROM pg_settings WHERE name = 'shared_preload_libraries';"
        ).fetchone()
    assert libraries is not None
    assert "pg_stat_statements" not in libraries["setting"]

    # bob user and db database no longer exists
    with pytest.raises(
        psycopg.OperationalError, match='password authentication failed for user "bob"'
    ):
        with psycopg.connect(
            "host=/tmp user=bob password=s3kret dbname=template1 port=5433"
        ):
            pass
    with pytest.raises(psycopg.OperationalError, match='database "db" does not exist'):
        with psycopg.connect(
            "host=/tmp user=postgres password=supers3kret dbname=db port=5433"
        ):
            pass
    with pytest.raises(psycopg.OperationalError, match='database "db2" does not exist'):
        with psycopg.connect(
            "host=/tmp user=postgres password=supers3kret dbname=db2 port=5433"
        ):
            pass
    with psycopg.connect(prod_dsn, row_factory=dict_row) as cnx:
        row = cnx.execute(
            "SELECT pg_catalog.pg_get_userbyid(d.datdba) as owner FROM pg_catalog.pg_database d WHERE d.datname = 'db3'"
        ).fetchone()
    assert row is not None
    assert row["owner"] == "postgres"

    # preprod stopped
    with pytest.raises(psycopg.OperationalError, match="No such file or directory"):
        assert cluster_name(preprod_dsn) == "preprod"
    with pytest.raises(ConnectionRefusedError):
        socket.create_connection(("localhost", 9188), 1)
    with pytest.raises(ConnectionRefusedError):
        socket.create_connection(("localhost", 2346), 1)

    # dev running
    dev_dsn = "host=/tmp user=postgres password=supers3kret dbname=postgres port=5455"
    assert cluster_name(dev_dsn) == "dev"
    socket.create_connection(("localhost", 9189))
    socket.create_connection(("localhost", 2347))
