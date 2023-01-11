"""
    This module provides functions and classes that helps with
    programmatic interaction with the BigQuery service.
"""
import txp.common
import txp.common.utils.signals_utils
from google.cloud import bigquery
from datetime import datetime, timedelta
from txp.common.config import settings
import PIL
from PIL import Image
import io
import numpy as np
import time
from scipy.fft import fft
import logging
from typing import List

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


def get_partition_utc_date(observation_timestamp):
    partition_timestamp = datetime.utcfromtimestamp(observation_timestamp // 1e9)
    partition_timestamp = partition_timestamp - timedelta(minutes=partition_timestamp.minute,
                                                          seconds=partition_timestamp.second)
    return partition_timestamp


def get_image_from_raw_data(data, lower_quality: bool = True):
    image = [int(x) for x in data[0]["values"]]
    image = np.frombuffer(bytes(image), dtype=np.uint8)
    image_b = bytes(image)
    try:
        image_pil: Image = Image.open(io.BytesIO(image_b))

        if not lower_quality:
            return image_pil

        with io.BytesIO() as output:
            image_pil.save(output, format="JPEG", quality=30, optimize=True)
            new_image = Image.open(io.BytesIO(output.getvalue()))

        return new_image

    except PIL.UnidentifiedImageError as e:
        log.info(f"Found a corrupted image: {e}")
        return None
    except Exception as e:
        log.info(f"Found a corrupted image: {e}")
        return None


def get_authenticated_client(service_account_credentials) -> bigquery.Client:
    """Returns a bigquery.Client, authenticated with the provided credentials.

    Args:
        service_account_credentials: A service_account.Credentials object with the
            appropriate permissions to use Bigquery.
    """
    return bigquery.Client(credentials=service_account_credentials)


def get_all_records_for_observation_timestamp(
        tenant_id: str,
        table_name: str,
        edge_logical_ids: List[str],
        perception_names: List[str],
        observation_timestamp: int,
        start_datetime: datetime,
        end_datetime: datetime,
        order_key: str,
        client: bigquery.Client
):
    """Gets all records using given an observation_timestamp for all the specified
    edges and the given perception_names.

        Args:
            tenant_id: id of tenant
            table_name: bigquery table name
            edge_logical_ids: logical id for edges of interest in the sampling window
            perception_names: perception names to request for the edges
            start_datetime: interval lower bound
            end_datetime: interval upper bound
            order_key: resulting dataframe will be ordered by this key
            client: bigquery client
        Returns:
            A pandas dataframe
    """
    start_time = int(start_datetime.timestamp() * 1e9)
    end_time = int(end_datetime.timestamp() * 1e9)
    start_partition_timestamp = get_partition_utc_date(start_time)
    end_partition_timestamp = get_partition_utc_date(end_time + 3.6e12)

    select_query = f"""
               SELECT * FROM `{table_name}` 
               WHERE tenant_id = "{tenant_id}"
                     AND edge_logical_id IN UNNEST({edge_logical_ids})
                     AND perception_name IN UNNEST({perception_names})
                     AND observation_timestamp = {observation_timestamp}
                     AND partition_timestamp >= "{start_partition_timestamp}"
                     AND partition_timestamp < "{end_partition_timestamp}"
               ORDER BY {order_key} DESC;
               """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    print(select_query)
    log.info(f"This query took: {end - start} seconds for perception: {perception_names}")

    return df

    # grouped_df = df.groupby("signal_timestamp")
    #
    # res = []
    #
    # for signal_timestamp, signal_df in grouped_df:
    #     all_chunks = signal_df.to_dict('records')
    #     signal = txp.common.utils.signals_utils.merge_signal_chunks(all_chunks)
    #     res.append(signal)
    #
    # return res


def get_all_records_within_interval_for_asset(
    tenant_id: str,
    table_name: str,
    asset_id: str,
    perception_name: str,
    start_datetime: datetime,
    end_datetime: datetime,
    client: bigquery.Client,
    columns: List[str]
):
    select_query = f"""
               SELECT {", ".join(columns)} FROM `{table_name}` 
               WHERE tenant_id = "{tenant_id}"
                     AND asset_id = "{asset_id}" 
                     AND perception_name = "{perception_name}"
                     AND partition_timestamp >= "{start_datetime}"
                     AND partition_timestamp < "{end_datetime}"
               ORDER BY observation_timestamp ASC;
               """
    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    print(select_query)
    log.info(f"This query took: {end - start} seconds for perception: {perception_name}")

    return df


def get_all_records_within_interval(
        tenant_id: str,
        table_name: str,
        edge_logical_id: str,
        perception_name: str,
        start_datetime: datetime,
        end_datetime: datetime,
        order_key: str,
        client: bigquery.Client
):
    """Gets all records within interval [start_datetime, end_datetime]
        Args:
            tenant_id: id of tenant
            table_name: bigquery table name
            edge_logical_id: logical id for edge
            perception_name: perception name for given edge
            start_datetime: interval lower bound
            end_datetime: interval upper bound
            order_key: resulting dataframe will be ordered by this key
            client: bigquery client
        Returns:
            List of signals, each element of the list is a dictionary
    """

    start_time = int(start_datetime.timestamp() * 1e9)
    end_time = int(end_datetime.timestamp() * 1e9)
    start_partition_timestamp = get_partition_utc_date(start_time)
    end_partition_timestamp = get_partition_utc_date(end_time + 3.6e12)

    select_query = f"""
           SELECT * FROM `{table_name}` 
           WHERE tenant_id = "{tenant_id}"
                 AND edge_logical_id = "{edge_logical_id}" 
                 AND perception_name = "{perception_name}"
                 AND observation_timestamp >= {start_time}
                 AND observation_timestamp <= {end_time}
                 AND partition_timestamp >= "{start_partition_timestamp}"
                 AND partition_timestamp < "{end_partition_timestamp}"
           ORDER BY {order_key} DESC;
           """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    print(select_query)
    log.info(f"This query took: {end - start} seconds for perception: {perception_name}")

    return df


def get_all_task_predictions_within_interval(
        tenant_id: str,
        table_name: str,
        asset_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
        client: bigquery.Client
):
    """Gets all records within interval [start_datetime, end_datetime]
        Args:
            tenant_id: id of tenant
            table_name: bigquery table name
            asset_id: logical id for asset
            start_datetime: interval lower bound
            end_datetime: interval upper bound
            client: bigquery client
        Returns:
            List of predictions (events or states), df containing all events
    """

    start_time = int(start_datetime.timestamp() * 1e9)
    end_time = int(end_datetime.timestamp() * 1e9)
    start_partition_timestamp = get_partition_utc_date(start_time)
    end_partition_timestamp = get_partition_utc_date(end_time + 3.6e12)

    select_query = f"""
           SELECT * FROM `{table_name}` 
           WHERE tenant_id = "{tenant_id}"
                 AND asset_id = "{asset_id}" 
                 AND partition_timestamp >= "{start_partition_timestamp}"
                 AND partition_timestamp < "{end_partition_timestamp}"
           ORDER BY observation_timestamp ASC;
           """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    log.info(f"This query took: {end - start} seconds")
    return df


def get_all_task_predictions_for_tenant_within_interval(
        tenant_id: str,
        table_name: str,
        asset_ids,
        start_datetime: datetime,
        end_datetime: datetime,
        client: bigquery.Client
):
    """Gets all records within interval [start_datetime, end_datetime]
        Args:
            tenant_id: id of tenant
            table_name: bigquery table name
            asset_ids: logical ids for asset of a tenant, it does not have to be all of them
            asset_ids: logical ids for asset of a tenant, it does not have to be all of them
            start_datetime: interval lower bound
            end_datetime: interval upper bound
            client: bigquery client
        Returns:
            List of predictions (events or states), df containing all events
    """

    start_time = int(start_datetime.timestamp() * 1e9)
    end_time = int(end_datetime.timestamp() * 1e9)
    start_partition_timestamp = get_partition_utc_date(start_time)
    end_partition_timestamp = get_partition_utc_date(end_time + 3.6e12)

    select_query = f"""
           SELECT * FROM `{table_name}` 
           WHERE tenant_id = "{tenant_id}"
                 AND asset_id IN UNNEST({asset_ids})
                 AND partition_timestamp >= "{start_partition_timestamp}"
                 AND partition_timestamp < "{end_partition_timestamp}"
           ORDER BY observation_timestamp ASC;
           """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    log.info(f"This query took: {end - start} seconds to download {df.size} registries")
    return df


def get_events_for_state(
        tenant_id,
        table_name: str,
        asset_id: str,
        events_id: list,
        days: int,
        client: bigquery.Client
):
    offset = days * 86400
    end = time.time_ns() // 1e9
    start = end - offset
    start_date = str(datetime.utcfromtimestamp(start))
    end_date = str(datetime.utcfromtimestamp(end))

    select_query = f""" 
       SELECT * FROM `{table_name}` 
       WHERE tenant_id = "{tenant_id}" 
             AND asset_id = "{asset_id}"
             AND event_id IN UNNEST({events_id})
             AND partition_timestamp <= "{end_date}"
             AND partition_timestamp >= "{start_date}"
       """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    log.info(f"This query took: {end - start} seconds")
    return df.to_dict('records')


def get_all_sections_within_interval(
        client,
        table_name,
        tenant_id: str,
        start_datetime: datetime,  # utc
        end_datetime: datetime,  # utc
        section_id: str,

):
    start = str(start_datetime)
    end = str(end_datetime)

    select_query = f""" 
           SELECT * FROM `{table_name}` 
           WHERE tenant_id = "{tenant_id}" 
                 AND section_id = "{section_id}"
                 AND creation_timestamp	<= "{end}"
                 AND creation_timestamp >= "{start}"
           ORDER BY creation_timestamp DESC
    """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    log.info(f"This query took: {end - start} seconds")
    return df.to_dict('records')


def get_all_signals_within_interval(
        tenant_id: str,
        table_name: str,
        edge_logical_id: str,
        perception_name: str,
        start_datetime: datetime,
        end_datetime: datetime,
        client: bigquery.Client
):
    """Gets all time signals within interval [start_datetime, end_datetime]
        Args:
            tenant_id: id of tenant
            table_name: bigquery table name
            edge_logical_id: logical id for edge
            perception_name: perception name for given edge
            start_datetime: interval lower bound
            end_datetime: interval upper bound
            client: bigquery client
        Returns:
            List of signals, each element of the list is a dictionary
    """

    df = get_all_records_within_interval(tenant_id, table_name, edge_logical_id, perception_name, start_datetime,
                                         end_datetime, "signal_timestamp", client)

    grouped_df = df.groupby("signal_timestamp")

    res = []

    for signal_timestamp, signal_df in grouped_df:
        all_chunks = signal_df.to_dict('records')
        signal = txp.common.utils.signals_utils.merge_signal_chunks(all_chunks)
        res.append(signal)
    return res


def get_last_task_prediction_for_asset(
        tenant_id,
        table_name: str,
        asset_id: str,
        days: int,
        client: bigquery.Client
):
    offset = days * 86400
    end = time.time_ns() // 1e9
    start = end - offset
    start_date = str(datetime.utcfromtimestamp(start))
    end_date = str(datetime.utcfromtimestamp(end))
    select_query = f""" 
       SELECT * FROM `{table_name}` 
       WHERE tenant_id = "{tenant_id}" 
             AND asset_id = "{asset_id}"
             AND partition_timestamp <= "{end_date}"
             AND partition_timestamp >= "{start_date}"
       ORDER BY observation_timestamp DESC
       LIMIT 1
       """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    log.info(f"This query took: {end - start} seconds")

    if not len(df):
        return None

    return df.iloc[0].to_dict()


def get_fft_from_raw_data(data):
    fft_per_dimensions = []
    for index, dimension in enumerate(data):
        fft_per_dimensions.append(fft(dimension["values"]))
    return np.array(fft_per_dimensions)


def get_last_signal_from_bigquery(tenant_id, table_name, edge_logical_id, perception_name, start_time, end_time,
                                  client):
    """Gets the latest signal  in the interval [start_time, end_time) that is store in bigquery given an
    edge_logical_id and a perception_name

    Args:
        tenant_id: id of tenant.
        perception_name: perception name of the signal.
        edge_logical_id: edge that generated the signal.
        start_time: left bound of time interval
        end_time: right bound of time interval
        table_name: table name
        client: BigQuery client
    """
    signals = get_all_signals_within_interval(tenant_id, table_name, edge_logical_id, perception_name, start_time,
                                              end_time, client)
    if not len(signals):
        return None
    return max(signals, key=lambda signal: signal["signal_timestamp"])


def get_all_signals_for_asset(tenant_id, table_name, edge_logical_ids, dataset_versions,
                              start_datetime, end_datetime, client):
    start_time = int(start_datetime.timestamp() * 1e9)
    end_time = int(end_datetime.timestamp() * 1e9)
    start_partition_timestamp = get_partition_utc_date(start_time)
    end_partition_timestamp = get_partition_utc_date(end_time + 3.6e12)

    tags_query = ""
    if dataset_versions:
        for i, version in enumerate(dataset_versions):
            tags_query += f'"{version}" IN UNNEST(dataset_versions) '
            if i + 1 < len(dataset_versions):
                tags_query += "OR "
    tags_query_condition = f"AND ({tags_query})" if tags_query else ""
    select_query = f"""
           SELECT * FROM `{table_name}` 
           WHERE tenant_id = "{tenant_id}"
                 AND edge_logical_id IN UNNEST({edge_logical_ids})
                 {tags_query_condition}
                 AND observation_timestamp >= {start_time}
                 AND observation_timestamp <= {end_time}
                 AND partition_timestamp >= "{start_partition_timestamp}"
                 AND partition_timestamp < "{end_partition_timestamp}";
           """

    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    log.info(f"This query took: {end - start} seconds, with {len(df)} registers")
    log.debug(f"{select_query}")
    return df


def annotate_signal(tenant_id, table_name, edge_logical_id, observation_timestamp, label,
                    dataset_versions, client):
    partition_timestamp = get_partition_utc_date(observation_timestamp)

    label_set_str = f"""label = '''{label}''', """ if table_name.split(".")[1] == "time" else ""

    select_query = f"""
       UPDATE `{table_name}`
       SET {label_set_str}
           dataset_versions = dataset_versions || {dataset_versions}  
       WHERE tenant_id = "{tenant_id}"
             AND edge_logical_id = "{edge_logical_id}"
             AND observation_timestamp = {observation_timestamp}
             AND partition_timestamp = "{partition_timestamp}";
    """
    start = time.time()
    res = client.query(select_query).result()
    end = time.time()
    log.info(f"This query took: {end - start} seconds")
    log.info(f"Table name: {table_name}")
    log.info(f"{select_query}")

    return res


def get_sampling_window_from_bigquery(table_id, edge_logical_id, perception_name, observation_timestamp, tenant_id,
                                      client):
    partition_timestamp = str(get_partition_utc_date(observation_timestamp))
    select_query = f"""
               SELECT * FROM `{table_id}` 
               WHERE tenant_id = "{tenant_id}"
                     AND edge_logical_id = "{edge_logical_id}" 
                     AND observation_timestamp = {observation_timestamp}
                     AND perception_name = "{perception_name}"
                     AND partition_timestamp = "{partition_timestamp}"
               """
    start = time.time()
    df = (client.query(select_query).result().to_dataframe())
    end = time.time()
    log.info(f"This query took: {end - start} seconds")
    return df.to_dict('records')


def get_last_sections_from_bq(
        table_name: str,
        tenant_id: str,
        section_type: str,
        client: bigquery.Client
):
    offset = 5 * 86400  # days in the past
    end = time.time_ns() // 1e9
    start = end - offset
    start_date = str(datetime.utcfromtimestamp(start))
    end_date = str(datetime.utcfromtimestamp(end))
    select_query = f""" 
       SELECT * FROM `{table_name}` 
       WHERE tenant_id = "{tenant_id}" 
             AND type = "{section_type}"
             AND creation_timestamp >= "{start_date}"
             AND creation_timestamp <= "{end_date}"
       ORDER BY creation_timestamp DESC
       LIMIT 1
       """
    df = (client.query(select_query).result().to_dataframe())
    return df


def get_last_worked_time_machine(
    table_name: str,
    tenant_id: str,
    asset_id: str,
    client: bigquery.Client
) -> int:
    """Returns the last worked time for the specified asset_id"""
    offset = 60 * 86400  # 60 days in the past
    end = time.time_ns() // 1e9
    start = end - offset
    start_date = str(datetime.utcfromtimestamp(start))
    end_date = str(datetime.utcfromtimestamp(end))
    select_query = f"""
        SELECT worked_hours
        FROM `{table_name}` WHERE
        tenant_id = "{tenant_id}" AND
        asset_id = "{asset_id}"
        AND partition_timestamp >= "{start_date}"
        AND partition_timestamp < "{end_date}"
        ORDER BY observation_timestamp DESC
        LIMIT 1;
    """
    df = client.query(select_query).result().to_dataframe()

    if df.isnull().values.any():
        return None

    return df.head().values[0][0]
