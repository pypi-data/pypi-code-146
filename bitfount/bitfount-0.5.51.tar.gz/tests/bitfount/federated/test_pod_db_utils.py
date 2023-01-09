"""Tests pod_db_utils.py."""
import hashlib
import json
import os
import platform
import sqlite3

import numpy as np
import pandas as pd
import pytest
from pytest import fixture

from bitfount.federated.pod_db_utils import (
    _map_task_to_hash_add_to_db,
    _save_results_to_db,
)
from bitfount.types import _JSONDict
from tests.utils.helper import create_datasource, unit_test


@fixture
def serialized_protocol_with_model() -> _JSONDict:
    """Serialized protocol dict with model (and aggregator)."""
    return {
        "algorithm": {
            "class_name": "alg",
            "model": {
                "class_name": "model",
                "schema": "mock_schema",
                "datastructure": {"table": "testpod"},
            },
        },
        "aggregator": {"class_name": "aggregator"},
        "class_name": "FederatedAveraging",
    }


@unit_test
@pytest.mark.skipif(
    condition=platform.system() == "Windows",
    reason=(
        "Only works intermittently on Windows. "
        "Connection to database not always closed properly,"
        "leading to PermissionError."
    ),
)
def test_worker_map_task_to_hash_multiple_alg(
    serialized_protocol_with_model: _JSONDict,
) -> None:
    """Tests that mapping task to hash works as expected."""
    if os.path.exists("testpod.db"):
        os.remove("testpod.db")
    con = sqlite3.connect("testpod.db")
    task_hash = hashlib.sha256(
        json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
    ).hexdigest()
    _map_task_to_hash_add_to_db(serialized_protocol_with_model, task_hash, con)  # type: ignore[arg-type] # reason: testing purposes only # noqa: B950
    task_defs = pd.read_sql("SELECT * FROM 'task_definitions' ", con)
    assert sorted(set(task_defs.columns)) == [
        "algorithm",
        "index",
        "protocol",
        "taskhash",
    ]
    assert task_hash in task_defs["taskhash"].values
    con.close()
    os.remove("testpod.db")


@unit_test
@pytest.mark.skipif(
    condition=platform.system() == "Windows",
    reason=(
        "Only works intermittently on Windows. "
        "Connection to database not always closed properly,"
        "leading to PermissionError."
    ),
)
def test_worker_save_results_to_db_no_datapoints(
    serialized_protocol_with_model: _JSONDict,
) -> None:
    """Tests that only results are saved to db."""
    pod_name = "testpod"
    if os.path.exists(f"{pod_name}.db"):
        os.remove(f"{pod_name}.db")
    pod_identifier = f"user/{pod_name}"
    task_hash = hashlib.sha256(
        json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
    ).hexdigest()
    con = sqlite3.connect(f"{pod_name}.db")
    cur = con.cursor()
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{pod_name}"
        ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""
    )
    datasource = create_datasource(classification=True)
    datasource._ignore_cols = ["Date"]
    datasource.load_data()
    datasource._test_idxs = [234, 21, 19]  # type: ignore[assignment] # reason: testing purposes only # noqa: B950
    new_data = datasource._data.copy()
    hashed_list = []
    for _, row in new_data.iterrows():
        hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    for col in new_data.columns:
        cur.execute(
            f"ALTER TABLE '{pod_name}' ADD COLUMN '{col}' {new_data[col].dtype}"  # noqa: B950
        )
    new_data["datapoint_hash"] = hashed_list
    new_data.to_sql(pod_name, con=con, if_exists="append", index=False)
    con.commit()
    serialized_protocol_with_model["algorithm"] = [
        serialized_protocol_with_model["algorithm"]
    ]

    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{task_hash}"
        (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""
    )

    _save_results_to_db(
        results=[np.array([1]), np.array([2]), np.array([3])],
        pod_identifier=pod_identifier,
        datasource=datasource,
        show_datapoints_in_results_db=False,
        run_on_new_data_only=True,
        task_hash=task_hash,
        con=con,
        table=pod_name,
    )
    task_data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
    assert task_data.shape == (
        3,
        3,
    )  # 3 rows corresponding to the test_idxs ,
    # 3 columns (rowID, datapoint_hash, result)
    con.close()
    os.remove(f"{pod_name}.db")


@unit_test
@pytest.mark.skipif(
    condition=platform.system() == "Windows",
    reason=(
        "Only works intermittently on Windows. "
        "Connection to database not always closed properly,"
        "leading to PermissionError."
    ),
)
def test_save_results_to_db(
    serialized_protocol_with_model: _JSONDict,
) -> None:
    """Tests that only results are saved to db."""
    pod_name = "testpod"
    if os.path.exists(f"{pod_name}.db"):
        os.remove(f"{pod_name}.db")
    pod_identifier = f"user/{pod_name}"
    task_hash = hashlib.sha256(
        json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
    ).hexdigest()
    con = sqlite3.connect(f"{pod_name}.db")
    cur = con.cursor()
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{pod_name}"
        ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""
    )
    datasource = create_datasource(classification=True)
    datasource._ignore_cols = ["Date"]
    datasource.load_data()
    datasource._test_idxs = [234, 21, 19]  # type: ignore[assignment] # reason: testing purposes only # noqa: B950
    new_data = datasource._data.copy()
    hashed_list = []
    for _, row in new_data.iterrows():
        hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    for col in new_data.columns:
        cur.execute(
            f"ALTER TABLE '{pod_name}' ADD COLUMN '{col}' {new_data[col].dtype}"  # noqa: B950
        )
    new_data["datapoint_hash"] = hashed_list
    new_data.to_sql(pod_name, con=con, if_exists="append", index=False)
    con.commit()
    serialized_protocol_with_model["algorithm"] = [
        serialized_protocol_with_model["algorithm"]
    ]

    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{task_hash}"
        (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""
    )

    _save_results_to_db(
        results=[np.array([1]), np.array([2]), np.array([3])],
        pod_identifier=pod_identifier,
        datasource=datasource,
        show_datapoints_in_results_db=True,
        run_on_new_data_only=True,
        task_hash=task_hash,
        con=con,
        table=pod_name,
    )
    task_data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
    assert task_data.shape == (
        3,
        20,
    )  # 3 rows corresponding to the test_idxs ,
    # 17 datasource_cols + 3 columns (rowID, datapoint_hash, result)
    con.close()
    os.remove(f"{pod_name}.db")


@unit_test
@pytest.mark.skipif(
    condition=platform.system() == "Windows",
    reason=(
        "Only works intermittently on Windows. "
        "Connection to database not always closed properly,"
        "leading to PermissionError."
    ),
)
def test_save_results_to_db_new_data_only(
    serialized_protocol_with_model: _JSONDict,
) -> None:
    """Tests that only results are saved to db."""
    pod_name = "testpod"
    if os.path.exists(f"{pod_name}.db"):
        os.remove(f"{pod_name}.db")
    pod_identifier = f"user/{pod_name}"
    task_hash = hashlib.sha256(
        json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
    ).hexdigest()
    con = sqlite3.connect(f"{pod_name}.db")
    cur = con.cursor()
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{pod_name}"
        ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""
    )
    datasource = create_datasource(classification=True)
    datasource._ignore_cols = ["Date"]
    datasource.load_data()
    datasource._test_idxs = [234, 21, 19]  # type: ignore[assignment] # reason: testing purposes only # noqa: B950
    new_data = datasource._data.copy()
    hashed_list = []
    for _, row in new_data.iterrows():
        hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    for col in new_data.columns:
        cur.execute(
            f"ALTER TABLE '{pod_name}' ADD COLUMN '{col}' {new_data[col].dtype}"  # noqa: B950
        )
    new_data["datapoint_hash"] = hashed_list
    new_data.to_sql(pod_name, con=con, if_exists="append", index=False)
    con.commit()
    serialized_protocol_with_model["algorithm"] = [
        serialized_protocol_with_model["algorithm"]
    ]

    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{task_hash}"
        (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""
    )

    _save_results_to_db(
        results=[np.array([1]), np.array([2]), np.array([3])],
        pod_identifier=pod_identifier,
        datasource=datasource,
        show_datapoints_in_results_db=True,
        run_on_new_data_only=True,
        task_hash=task_hash,
        con=con,
        table=pod_name,
    )
    task_data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
    assert task_data.shape == (
        3,
        20,
    )  # 3 rows corresponding to the test_idxs ,
    # 17 datasource_cols + 3 columns (rowID, datapoint_hash, result)
    _save_results_to_db(
        results=[np.array([1]), np.array([2]), np.array([3])],
        pod_identifier=pod_identifier,
        datasource=datasource,
        show_datapoints_in_results_db=True,
        run_on_new_data_only=False,
        task_hash=task_hash,
        con=con,
        table=pod_name,
    )
    task_data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
    assert task_data.shape == (
        6,
        20,
    )  # 6 rows corresponding to the 3 test_idxs times 2,
    # 17 datasource_cols + 3 columns (rowID, datapoint_hash, result)
    con.close()
    os.remove(f"{pod_name}.db")
