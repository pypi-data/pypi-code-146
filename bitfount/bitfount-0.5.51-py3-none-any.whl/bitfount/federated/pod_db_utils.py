"""Utilities for the Pod results database."""
import hashlib
import sqlite3
from sqlite3 import Connection
from typing import List, Sequence

import numpy as np
import pandas as pd

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated import _get_federated_logger
from bitfount.federated.types import SerializedProtocol

logger = _get_federated_logger(__name__)


def _add_data_to_pod_db(pod_name: str, data: pd.DataFrame, table_name: str) -> None:
    """Method for adding the data to the pod database.

    Args:
        data: Dataframe to be added to the database.
        table-name: The table from the datasource corresponding to the data.

    Raises:
        ValueError: If there are clashing column names in the datasource
            and the pod database.
    """
    con = sqlite3.connect(f"{pod_name}.db")
    cur = con.cursor()
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{table_name}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
    )
    con.commit()
    if "datapoint_hash" in data.columns:
        raise ValueError(
            "`datapoint_hash` not supported as column name in the datasource."
        )
    # as placeholder column for the hash
    data["datapoint_hash"] = np.nan
    # change type to object so it will match the db type
    data["datapoint_hash"] = data["datapoint_hash"].astype("object")

    # sqlite transforms bool values to int, so we need to make sure that
    # they are the same in the df so the hashes match
    bool_cols = [col for col in data.columns if data[col].dtype == bool]
    # replace bools by their int value, as it will be done by
    # sqlite in the db anyway
    data[bool_cols] *= 1
    # read the db data for the datasource
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    existing_data = pd.read_sql(f'SELECT * FROM "{table_name}"', con)  # nosec
    existing_cols_without_index = set(existing_data.columns)
    existing_cols_without_index.remove("rowID")
    # check if df is empty or if columns all columns are the same,
    # if not all the hashes will have to be recomputed
    if not existing_data.empty and set(data.columns) == existing_cols_without_index:
        data = pd.merge(
            data.drop(columns=["datapoint_hash"]),
            existing_data.drop(columns=["datapoint_hash", "rowID"]),
            how="outer",
            indicator=True,
        ).loc[lambda x: x["_merge"] != "both"]
        data.drop(columns=["_merge"], inplace=True)
        data.drop_duplicates()
        hashed_list = []
        for _, row in data.iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
        data["datapoint_hash"] = hashed_list
        data.to_sql(table_name, con=con, if_exists="append", index=False)
    else:
        cur = con.cursor()
        # replace table if columns are mismatched
        cur.execute(f"DROP TABLE '{table_name}'")
        cur.execute(f"""CREATE TABLE "{table_name}" ('rowID' INTEGER PRIMARY KEY)""")
        for col in data.columns:
            cur.execute(
                f"ALTER TABLE '{table_name}' ADD COLUMN '{col}' {data[col].dtype}"  # noqa: B950
            )

        hashed_list = []
        for _, row in data.iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
        data["datapoint_hash"] = hashed_list
        data.to_sql(table_name, con=con, if_exists="append", index=False)
    con.close()


def _map_task_to_hash_add_to_db(
    serialized_protocol: SerializedProtocol, task_hash: str, con: Connection
) -> None:
    algorithm_ = serialized_protocol["algorithm"]
    if not isinstance(algorithm_, Sequence):
        algorithm_ = [algorithm_]
    for algorithm in algorithm_:
        if "model" in algorithm:
            algorithm["model"].pop("schema")
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS "task_definitions" ('index' INTEGER  PRIMARY KEY AUTOINCREMENT  NOT NULL, 'taskhash' TEXT,'protocol' TEXT,'algorithm' TEXT)"""  # noqa: B950
    )
    data = pd.read_sql("SELECT * FROM 'task_definitions' ", con)
    if task_hash not in data["taskhash"].unique():
        cur.execute(
            """INSERT INTO "task_definitions" ('taskhash',  'protocol', 'algorithm' ) VALUES (?,?,?);""",  # noqa: B950
            (
                task_hash,
                serialized_protocol["class_name"],
                str(algorithm_),
            ),
        )
    con.commit()


def _save_results_to_db(
    con: Connection,
    datasource: BaseSource,
    results: List[np.ndarray],
    run_on_new_data_only: bool,
    pod_identifier: str,
    show_datapoints_in_results_db: bool,
    table: str,
    task_hash: str,
) -> None:
    pod_con = sqlite3.connect(f"{pod_identifier.split('/')[1]}.db")
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    pod_data = pd.read_sql(f'SELECT * FROM "{table}"', pod_con)  # nosec
    pod_con.close()
    # We only care about the test data since we don't log
    # anything in the database for validation or training data
    run_data = datasource.data.iloc[datasource._test_idxs]
    # convert results to string
    results_as_str = [str(item) for item in results]
    run_data["results"] = results_as_str
    columns = list(pod_data.columns)
    columns.remove("rowID")
    columns.remove("datapoint_hash")
    # get the datapoint hashes from the pod db
    data_w_hash = pd.merge(
        pod_data,
        run_data,
        how="outer",
        left_on=columns,
        right_on=columns,
        indicator=True,
    ).loc[lambda x: x["_merge"] == "both"]
    # drop the indicator and index columns
    data_w_hash.drop("_merge", inplace=True, axis=1)
    if "rowID" in data_w_hash.columns:
        data_w_hash.drop("rowID", inplace=True, axis=1)
    data_w_hash.drop_duplicates(inplace=True, keep="last")
    cur = con.cursor()
    # Ignoring the security warning because the sql query is trusted and
    # the task_hash is calculated at __init__.
    task_data = pd.read_sql(f'SELECT "datapoint_hash" FROM "{task_hash}"', con)  # nosec
    # If this is the first time the task is run, it will not
    # have all the columns, so we need to make sure they are
    # added. Otherwise, we don't need to worry about the columns
    # as any alterations to them will be classified as a new task
    if task_data.shape[0] == 0 and show_datapoints_in_results_db:
        for col in columns:
            cur.execute(
                f"ALTER TABLE '{task_hash}' ADD COLUMN '{col}' {data_w_hash[col].dtype}"  # noqa: B950
            )
    if not run_on_new_data_only:
        # save all results to db
        if show_datapoints_in_results_db:
            data_w_hash.to_sql(f"{task_hash}", con=con, if_exists="append", index=False)
        else:
            data_w_hash[["datapoint_hash", "results"]].to_sql(
                f"{task_hash}", con=con, if_exists="append", index=False
            )
    else:
        # do merge and get new datapoints only
        new_task_datapoint = pd.merge(
            data_w_hash,
            task_data,
            how="left",
            indicator=True,
        ).loc[lambda x: x["_merge"] == "left_only"]
        if "rowId" in new_task_datapoint.columns:
            new_task_datapoint.drop("rowID", inplace=True, axis=1)
        # drop the indicator and index columns
        new_task_datapoint.drop("_merge", inplace=True, axis=1)
        logger.info(
            f"The task was run on {new_task_datapoint.shape[0]} "
            f"records from the datasource."
        )
        if show_datapoints_in_results_db:
            new_task_datapoint.to_sql(
                f"{task_hash}", con=con, if_exists="append", index=False
            )
        else:
            new_task_datapoint[["datapoint_hash", "results"]].to_sql(
                f"{task_hash}", con=con, if_exists="append", index=False
            )
