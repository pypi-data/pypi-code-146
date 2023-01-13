import json
import pathlib
import subprocess
from typing import Callable, Dict, Iterator

import psycopg
import pytest
import yaml


@pytest.fixture
def postgresql_socket_directory(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "pgsql"


@pytest.fixture
def call_playbook(
    tmp_path: pathlib.Path,
    ansible_env: Dict[str, str],
    ansible_vault: Callable[[Dict[str, str]], pathlib.Path],
    postgresql_socket_directory: pathlib.Path,
) -> Iterator[Callable[[pathlib.Path], None]]:
    env = ansible_env.copy()
    settings = {
        "prefix": str(tmp_path),
        "postgresql": {
            "socket_directory": str(postgresql_socket_directory),
        },
    }
    with (tmp_path / "config.json").open("w") as f:
        json.dump(settings, f)
    env["SETTINGS"] = f"@{tmp_path / 'config.json'}"

    vault = ansible_vault({"replication_role_password": "r3pl1c@t"})

    teardown_play = tmp_path / "teardown.yml"
    with teardown_play.open("w") as f:
        yaml.safe_dump(
            [
                {
                    "name": "teardown standby setup",
                    "hosts": "localhost",
                    "tasks": [
                        {
                            "name": "drop standby",
                            "dalibo.pglift.instance": {
                                "name": "pg2",
                                "state": "absent",
                            },
                        },
                        {
                            "name": "drop primary",
                            "dalibo.pglift.instance": {
                                "name": "pg1",
                                "state": "absent",
                            },
                        },
                    ],
                }
            ],
            f,
        )

    def call(playfile: pathlib.Path) -> None:
        subprocess.check_call(
            [
                "ansible-playbook",
                "--extra-vars",
                f"@{vault}",
                str(playfile),
            ],
            env=env,
        )

    yield call
    call(teardown_play)


def test(
    playdir: pathlib.Path,
    call_playbook: Callable[[pathlib.Path], None],
    postgresql_socket_directory: pathlib.Path,
) -> None:
    call_playbook(playdir / "play4.yml")

    primary_conninfo = f"host={postgresql_socket_directory} user=replication password=r3pl1c@t dbname=postgres port=5433"
    with psycopg.connect(primary_conninfo) as conn:
        rows = conn.execute("SELECT * FROM pg_is_in_recovery()").fetchall()
    assert rows == [(True,)]

    call_playbook(playdir / "play5.yml")

    primary_conninfo = f"host={postgresql_socket_directory} user=replication password=r3pl1c@t dbname=postgres port=5432"
    with psycopg.connect(primary_conninfo) as conn:
        rows = conn.execute("SELECT * FROM pg_is_in_recovery()").fetchall()
    assert rows == [(True,)]
    primary_conninfo = f"host={postgresql_socket_directory} user=postgres port=5433"
    with psycopg.connect(primary_conninfo) as conn:
        rows = conn.execute("SELECT * FROM pg_is_in_recovery()").fetchall()
    assert rows == [(False,)]
