# =========================== Imports ===============================
import google.cloud.bigquery as bigquery
import pandas as pd
import txp.common.utils.bigquery_utils as bq_utils
import datetime
import pytz
import logging


_WORKED_TIME_TABLE_ID = "telemetry.equipments_total_worked_time"
_VIBRATION_TELEMETRY_TABLE_ID = "telemetry.vibration"
_PERCEPTION_QUERY = "VibrationSpeed"
_MAX_DAYS_IN_PAST = 30


# =========================== Cloud function def ===============================
def get_worked_hours_df(client: bigquery.Client):
    """TODO: Eventually we want a more elaborated logic when we have
    enough machines to make linear complexity too slow."""
    select_query = f"""
            SELECT * FROM `{_WORKED_TIME_TABLE_ID}`;
        """
    df = client.query(select_query).result().to_dataframe()
    return df


def get_vibration_table_dataframe(
    client: bigquery.Client, tenant_id: str, asset_id: str, start_datetime, end_datetime
):
    vibration_df = bq_utils.get_all_records_within_interval_for_asset(
        tenant_id,
        _VIBRATION_TELEMETRY_TABLE_ID,
        asset_id,
        _PERCEPTION_QUERY,
        start_datetime,
        end_datetime,
        client,
        ["observation_time_secs"],
    )
    return vibration_df


def get_total_worked_time_in_interval(
    start_datetime, end_datetime, tenant_id, asset_id, bq_client, table
) -> int:
    logging.info(f"Downloading Vibration Data for the asset: {asset_id}")
    logging.info(f"Time interval to download: {start_datetime} - {end_datetime}")
    # iterate Daily to query with minimal costs!
    time_secs = 0
    while start_datetime < end_datetime:
        next_partition_time = start_datetime + datetime.timedelta(hours=1)
        df = get_vibration_table_dataframe(
            bq_client, tenant_id, asset_id, start_datetime, next_partition_time
        )
        time_secs += df.sum(axis=0)["observation_time_secs"]
        start_datetime = next_partition_time

    return time_secs


def write_new_worked_time_value(
    bq_client, tenant_id, asset_id, worked_time, datetime_checkpoint, table_id
):
    update_query = f"""
        UPDATE {table_id} 
        SET last_generation_checkpoint = "{datetime_checkpoint}", total_worked_time = {worked_time}
        WHERE tenant_id="{tenant_id}" AND asset_id="{asset_id}"
    """
    res = bq_client.query(update_query).result()
    logging.info(f"Response from Database when updating total worked time: {res}")


def compute_asset_total_worked_time(event, context):
    print("Computing total worked time for assets")

    print(f"Getting Assets IDs to compute")
    bq = bigquery.Client()
    assets_df = get_worked_hours_df(bq)

    for i, row in assets_df.iterrows():
        tenant_id = row["tenant_id"]
        asset_id = row["asset_id"]
        last_generation_checkpoint = row["last_generation_checkpoint"]
        total_worked_time = row["total_worked_time"]

        current_partition_time = datetime.datetime.now(tz=pytz.timezone(pytz.utc.zone))

        current_partition_time = current_partition_time.replace(
            minute=0, second=0, microsecond=0
        )

        if pd.isnull(last_generation_checkpoint) or pd.isnull(total_worked_time):
            logging.info(
                "No previous working time was found. Will compute for the first time."
            )
            start_partition_time = current_partition_time - datetime.timedelta(days=2)
            start_partition_time = start_partition_time.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            total_worked_time = 0
        else:
            start_partition_time = last_generation_checkpoint.to_pydatetime()
            start_partition_time = start_partition_time.replace(
                minute=0, second=0, microsecond=0
            )
            total_worked_time = int(total_worked_time)

        added_worked_time_secs = get_total_worked_time_in_interval(
            start_partition_time,
            current_partition_time,
            tenant_id,
            asset_id,
            bq,
            _VIBRATION_TELEMETRY_TABLE_ID,
        )
        logging.info(f"Computed new added worked time: {added_worked_time_secs} secs.")
        print(f"Computed new added worked time: {added_worked_time_secs} secs.")

        logging.info(
            f"Computed total worked time: {added_worked_time_secs + total_worked_time} secs."
        )
        print(
            f"Computed total worked time: {added_worked_time_secs + total_worked_time} secs."
        )

        write_new_worked_time_value(
            bq,
            tenant_id,
            asset_id,
            int(added_worked_time_secs + total_worked_time),
            current_partition_time,
            _WORKED_TIME_TABLE_ID,
        )

    return "OK\n", 200


if __name__ == "__main__":
    compute_asset_total_worked_time({}, {})
