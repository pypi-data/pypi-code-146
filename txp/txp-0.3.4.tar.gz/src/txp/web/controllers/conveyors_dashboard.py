"""
    This script defines objects and functions to organize the information
    to show in the new interface focused on Conveyors & Transportation systems.
"""
import dataclasses
import datetime

from google.cloud import bigquery
from txp.common.ml.tasks import AssetStateCondition
from txp.common.edge.common import MachineMetadata, EdgeDescriptor
from typing import List, Dict, Any, Tuple
from txp.common.utils.firestore_utils import ProjectModel
import txp.common.utils.iot_core_utils as iot_controller
import txp.common.utils.bigquery_utils as bq_utils
import time
import enum
import pytz
import pandas as pd
import streamlit as st
import logging
from txp.common.config import settings
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class TransportationLineConnectivity(enum.Enum):
    OPTIMAL = 0
    REGULAR = 1
    BAD = 2


@dataclasses.dataclass
class ConveyorMetrics:
    last_temperature_value: float
    last_rpm_value: float
    last_seen_date: Any
    total_worked_seconds: int


@dataclasses.dataclass
class TransportationLine:
    """A Transportation line a machines group.

    This holds the information to show the Transportations Lines table
    on the main dashboard.
    """

    name: str
    num_of_machines: int
    project_model: ProjectModel
    cloud_credentials: Any

    def __post_init__(self):
        self._machines_dict = {}
        self._machine_to_edge_dict = {}
        for machine in self.project_model.machines_table:
            self._machines_dict[machine]: Dict[
                str, MachineMetadata
            ] = self.project_model.machines_table[machine]
            edge = self._machines_dict[machine].edges_ids[0]  # NOTE: Take only 1 edge p/conveyor
            self._machine_to_edge_dict[machine]: Dict[
                str, EdgeDescriptor
            ] = self.project_model.edges_table[edge]

        self._machine_metrics: Dict[str, ConveyorMetrics] = {}
        self._pull_information_from_db()

    def _pull_information_from_db(self):
        big_query_client = bq_utils.get_authenticated_client(
            self.cloud_credentials
        )
        start_time = datetime.datetime.now(tz=pytz.timezone("America/Mexico_City")) - datetime.timedelta(hours=5)
        end_time = datetime.datetime.now(tz=pytz.timezone("America/Mexico_City"))
        for machine in self.project_model.machines_table:
            self._machine_metrics[machine] = get_last_machine_metrics(
                big_query_client,
                st.secrets['tenant_id'],
                machine,
                start_time,
                end_time,
                "telemetry.vibration"
            )
        big_query_client.close()

    def get_machine_by_id(self, mid) -> MachineMetadata:
        return self._machines_dict[mid]

    def get_edge_by_machine(self, machine) -> EdgeDescriptor:
        return self._machine_to_edge_dict[machine]

    def get_connectivity(self) -> TransportationLineConnectivity:
        total_edges = len(self._machine_to_edge_dict)
        total_connected_or_sampling = 0
        total_disconnected_or_recovering = 0
        for edge in self._machine_to_edge_dict.values():
            if (
                self.project_model.edges_states_table[edge.logical_id] == "Disconnected"
                or self.project_model.edges_states_table[edge.logical_id] == "Recovering"
            ):
                total_disconnected_or_recovering += 1
            else:
                total_connected_or_sampling += 1

        if total_edges == total_connected_or_sampling:
            return TransportationLineConnectivity.OPTIMAL
        elif abs(total_edges - total_disconnected_or_recovering) >= total_edges/3:
            return TransportationLineConnectivity.REGULAR
        else:
            return TransportationLineConnectivity.BAD


def change_utc_timezone(timestamp):
    utc = pytz.timezone("UTC")
    timezone = pytz.timezone("America/Mexico_City")
    date_time = pd.to_datetime(timestamp)
    localized_timestamp = utc.localize(date_time)
    new_timezone = localized_timestamp.astimezone(timezone)
    return new_timezone.strftime('%Y-%m-%d %H:%M:%S')


def get_current_total_worked_seconds(machine_id, tenant_id, db):
    query = f"""
        SELECT total_worked_time
        FROM `telemetry.equipments_total_worked_time` WHERE
        asset_id="{machine_id}" AND tenant_id="{tenant_id}";
    """
    log.info(query)
    start = time.time()
    df = db.query(query).result().to_dataframe()
    end = time.time()
    log.info(f"Pulling RPM of machine took: {end - start} seconds.")
    if df.size:
        return df["total_worked_time"].head(1).values[0]
    else:
        return 0


def get_last_machine_metrics(
    db: bigquery.Client,
    tenant_id: str,
    asset_id: str,
    start_datetime: datetime.datetime,
    end_datetime: datetime.datetime,
    table_name: str,
):
    """Returns the number of counted signals per RPM ranges,
    in the specified interval.
    Returns:
        A tuple with elements:
            - The pandas Dataframe of the signals with columns:
                ['asset_id', 'edge_logical_id', 'rpm', 'rpm_int', 'observation_timestamp']
            - pd.Series with the range value counts for the RPM of each machine.

    TODO: We can get the temperature from this same query. Reducing everything to a single
        query operation!.
    """
    start_time = int(start_datetime.timestamp() * 1e9)
    end_time = int(end_datetime.timestamp() * 1e9)
    start_partition_timestamp = bq_utils.get_partition_utc_date(start_time)
    end_partition_timestamp = bq_utils.get_partition_utc_date(end_time + 3.6e12)

    query = f"""
        SELECT asset_id, edge_logical_id, rpm, observation_timestamp, temperature
        FROM `{table_name}` WHERE
        tenant_id = "{tenant_id}" AND
        asset_id = "{asset_id}"
        AND partition_timestamp >= "{start_partition_timestamp}"
        AND partition_timestamp < "{end_partition_timestamp}"
        ORDER BY observation_timestamp DESC
        LIMIT 1;
    """
    log.info(query)
    start = time.time()
    df = db.query(query).result().to_dataframe()
    end = time.time()
    log.info(f"Pulling RPM of machine took: {end - start} seconds.")

    # Transform column from a list of RPM to a single RPM value
    df["rpm"] = df["rpm"].map(lambda l: l[0])

    # pull total worked secs
    total_secs = get_current_total_worked_seconds(asset_id, tenant_id, db)

    if df.size:
        return ConveyorMetrics(
            df['temperature'].head(1).values[0],
            df["rpm"].head(1).values[0],
            change_utc_timezone(df['observation_timestamp'].values[0]),
            int(total_secs)
        )
    else:
        return ConveyorMetrics(0.0, 0.0, None, 0)
