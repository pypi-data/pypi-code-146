from dataclasses import dataclass
from datetime import datetime

from dbt.adapters.bigquery.connections import BigQueryAdapterResponse


@dataclass
class AlvinBigQueryAdapterResponse(BigQueryAdapterResponse):
    job_id: str = None
    alvin_platform_id: str = None
    event_time: datetime = None
    started: datetime = None
    ended: datetime = None
