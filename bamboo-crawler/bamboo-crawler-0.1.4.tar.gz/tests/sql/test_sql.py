import json
import os
import sqlite3
import subprocess
from typing import Any

import pytest

Database = Any


@pytest.fixture
def database() -> None:  # type: ignore
    db_filepath = "/tmp/test1"
    with open(db_filepath, "w"):
        pass
    db = sqlite3.connect(db_filepath)
    c = db.cursor()
    c.execute("CREATE TABLE test_table1 (col1 text, col2 int);")
    c.execute("INSERT INTO test_table1 (col1, col2) VALUES ('test', 1);")
    c.execute("INSERT INTO test_table1 (col1, col2) VALUES ('test', 2);")
    c.execute("INSERT INTO test_table1 (col1, col2) VALUES ('test', 3);")
    db.commit()
    yield db
    db.close()
    os.unlink(db_filepath)


def run_recipe(taskname: str):  # type: ignore
    c = subprocess.run(
        [
            "python",
            "-m",
            "bamboo_crawler",
            "-r",
            "tests/sql/recipe.yml",
            "-t",
            taskname,
        ],
        stdout=subprocess.PIPE,
    )
    return c


def test_test1(database: Database) -> None:
    c = run_recipe("test1")
    j = json.loads(c.stdout)
    assert j["col1"] == "test"
    assert j["col2"] == 1
    assert c.returncode == 0


def test_test2(database: Database) -> None:
    (c1,) = database.execute("SELECT COUNT(*) FROM test_table1").fetchone()
    run_recipe("test2")
    (c2,) = database.execute("SELECT COUNT(*) FROM test_table1").fetchone()
    assert c1 + 1 == c2


def test_test3(database: Database) -> None:
    c = run_recipe("test3")
    j = json.loads(c.stdout)
    assert j["col1"] == "test"
    assert j["col2"] == 1


def test_test4(database: Database) -> None:
    (c1,) = database.execute("SELECT COUNT(*) FROM test_table1").fetchone()
    run_recipe("test4")
    (c2,) = database.execute("SELECT COUNT(*) FROM test_table1").fetchone()
    assert c1 + 1 == c2
