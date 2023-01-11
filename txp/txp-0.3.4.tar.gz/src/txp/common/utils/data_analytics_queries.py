"""
    This file contains utitilies that process data from persistence into
    information for the vibration data analysis reports.
"""
from typing import Tuple
from google.cloud import bigquery
import datetime
from txp.common.config import settings
import txp.common.utils.bigquery_utils as bq_utils
import pandas as pd
import logging
import pytz
import time
import streamlit as st

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


def get_rpm_counts_for_machine(
    db: bigquery.Client,
    tenant_id: str,
    asset_id: str,
    start_datetime: datetime.datetime,
    end_datetime: datetime.datetime,
    table_name: str,
    rpm_grouping_error: int = 5,
) -> Tuple[pd.DataFrame, pd.Series]:
    """Returns the number of counted signals per RPM ranges,
    in the specified interval.

    Returns:
        A tuple with elements:
            - The pandas Dataframe of the signals with columns:
                ['asset_id', 'edge_logical_id', 'rpm', 'rpm_int', 'observation_timestamp']
            - pd.Series with the range value counts for the RPM of each machine.
    """
    start_time = int(start_datetime.timestamp() * 1e9)
    end_time = int(end_datetime.timestamp() * 1e9)
    start_partition_timestamp = bq_utils.get_partition_utc_date(start_time)
    end_partition_timestamp = bq_utils.get_partition_utc_date(end_time + 3.6e12)

    query = f"""
        SELECT asset_id, edge_logical_id, rpm, observation_timestamp 
        FROM `{table_name}` WHERE
        tenant_id = "{tenant_id}" AND
        asset_id = "{asset_id}"
        AND partition_timestamp >= "{start_partition_timestamp}"
        AND partition_timestamp < "{end_partition_timestamp}"
        ORDER BY observation_timestamp ASC;
    """
    start = time.time()
    df = db.query(query).result().to_dataframe()
    end = time.time()
    log.info(f"Pulling RPM of machine took: {end - start} seconds.")

    # Transform column from a list of RPM to a single RPM value
    df["rpm"] = df["rpm"].map(lambda l: l[0])

    # Drops possible rows with 0 RPM (engine off)
    index_off = df[df["rpm"] == 0.0].index
    df.drop(index_off, inplace=True)

    # Adds a new column for rpm integer value
    df["rpm_int"] = df["rpm"].map(lambda f: int(f))

    # Compute the intervals to group by given a +/- error integer value
    max_rpm = df["rpm_int"].max()
    rpm_bins = list(range(0, max_rpm + rpm_grouping_error, rpm_grouping_error))
    df["rpm_bin"] = pd.cut(df["rpm_int"], bins=rpm_bins)

    # Counts the number of elements per RPM
    return df, df["rpm_bin"].value_counts().where(lambda x: x > 0).dropna()
