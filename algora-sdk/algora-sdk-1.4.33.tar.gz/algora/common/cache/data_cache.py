"""
Data request cache implementation. Data requests are stored as a key in the cache using format:
{timestamp}.{request hash}. Cache supports single and start/end date requests.

Cache 'put' cases:
    date:
    1. Query data
    2. Create key with single date and hashed request
    3. Store in cache

    start_date and end_date:
    1. Query data.
    2. Parse response to get all individuals dates (assume column is 'date', but allow column to be overwritten).
       Currently only supports DataFrame
    3. Group the response by date and store in cache
"""
from datetime import date
from functools import partial
from typing import Dict, Tuple

import pandas as pd

from algora.common.decorators import partitioned_cached
from algora.common.date import date_to_timestamp, create_dates_between
from algora.common.model import DataRequest


def __get_request(*args, **kwargs):
    for arg in args:
        if isinstance(arg, DataRequest):
            return arg

    for arg in kwargs.values():
        if isinstance(arg, DataRequest):
            return arg


def __partition_key_mapping(request: DataRequest) -> Tuple[date, str]:
    if isinstance(request.as_of_date, date):
        timestamp = date_to_timestamp(request.as_of_date)
        return request.as_of_date, build_partition_key(timestamp, request)
    else:
        timestamp = date_to_timestamp(request.as_of_date.date())
        return request.as_of_date.date(), build_partition_key(timestamp, request)


def build_partition_key(timestamp: int, request: DataRequest) -> str:
    excluded_keys = {'as_of_date', 'start_date', 'end_date', 'as_of'}
    return f"{timestamp}.{request.base64_encoded(exclude=excluded_keys)}"


def get_key_partitions(request: DataRequest) -> Dict[date, str]:
    partitions = []
    if request.as_of_date:
        partitions.append(__partition_key_mapping(request))
    elif request.start_date and request.end_date:
        start = request.start_date.date()
        end = request.end_date.date()

        for _date in create_dates_between(start=start, end=end, frequency='D'):
            base_request = request.copy(deep=True)
            base_request.as_of_date = _date
            base_request.start_date = None
            base_request.end_date = None
            partitions.append(__partition_key_mapping(base_request))

    return dict(partitions)


def partition_dataframe(df: pd.DataFrame):
    if df.empty:
        return {}

    return {dt.date(): data for dt, data in df.groupby(pd.Grouper(key='date', freq='D'))}


day_partition_cache = partial(
    partitioned_cached,
    get_key_partitions=get_key_partitions,
    combine_partitions=pd.concat,
    partition_value=partition_dataframe,
    cache_lookup_criterion=lambda key: key.as_of_date is not None,
    key=__get_request
)
