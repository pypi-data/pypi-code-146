import asyncio
import datetime
import math
from collections.abc import AsyncIterable
from datetime import datetime, timedelta
from typing import Dict, Generator, List, Sequence, Tuple, Union

import dateutil.parser
import pendulum

from aiopi.data.request import handle_request
from aiopi.http import PIClient
from aiopi.constants import TIMEZONE
from aiopi.types import JSONPrimitive



def format_streams_content(
    content: Dict[str, List[Dict[str, JSONPrimitive]]]
) -> Dict[str, List[JSONPrimitive]]:
    """Extract timestamp and value for each item in a stream"""
    formatted = {"timestamp": [], "value": []}
    items = content.get("Items", []) if content is not None else []
    
    for item in items:
        timestamp = item["Timestamp"]
        good = item["Good"]
        if not good:
            value = None
        else:
            # if a stream item returned an error, the value will be None anyway
            # and we're not particularly interested in the errors
            # https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/topics/error-handling.html
            value = item["Value"]
            if isinstance(value, dict):
                value = value["Name"]
        formatted["timestamp"].append(timestamp)
        formatted["value"].append(value)
    
    return formatted


def get_timestamp_index(data: List[Dict[str, JSONPrimitive]]) -> List[str]:
    """Create a single, sorted timestamp index from all timestamps returned
    from streams data. Duplicate timestamps are removed
    """
    index = set()
    for datum in data:
        index.update(datum["timestamp"])
    return sorted(index)


def iter_rows(
    index: List[str],
    data: List[Dict[str, List[JSONPrimitive]]]
) -> Generator[List[JSONPrimitive], None, None]:
    """Iterate through the data for each web_id row by row and produce rows
    which have data aligned on a common timestamp
    """
    for timestamp in index:
        iso_timestamp = pendulum.instance(
            dateutil.parser.isoparse(timestamp)
        ).in_timezone(TIMEZONE).replace(tzinfo=None).isoformat()
        row = [iso_timestamp]
        for datum in data:
            try:
                if datum["timestamp"][0] == timestamp:
                    row.append(datum["value"].pop(0))
                    datum["timestamp"].pop(0)
                else:
                    # Most recent data point is later than current timestamp
                    row.append(None)
            except IndexError:
                # No more data for that web id
                row.append(None)
        yield row


def split_interpolated_range(
    start_time: datetime,
    end_time: datetime,
    interval: timedelta,
    request_chunk_size: int = 5000
) -> Tuple[List[datetime], List[datetime]]:
    """Split a time range into smaller ranges for interpolated requests"""
    td: timedelta = end_time - start_time
    request_time_range = td.total_seconds()
    items_requested = math.ceil(
        request_time_range/interval.total_seconds()
    )
    
    if items_requested <= request_chunk_size:
        return [start_time], [end_time]
    
    # Derive an interval that will produce request_chunk_size items per request
    dt = timedelta(seconds=math.floor(interval.total_seconds()*request_chunk_size))
    return split_range(start_time, end_time, dt)


def split_recorded_range(
    start_time: datetime,
    end_time: datetime,
    request_chunk_size: int = 5000,
    scan_rate: float = 5
) -> Tuple[List[datetime], List[datetime]]:
    """Split a time range into smaller ranges for recorded requests"""
    td: timedelta = end_time - start_time
    request_time_range = td.total_seconds()
    items_requested = math.ceil(request_time_range/scan_rate)
    
    if items_requested <= request_chunk_size:
        return [start_time], [end_time]
    
    # Derive an interval that will produce (at most) request_chunk_size items per
    # request. The total items returned for a recorded request is not determinisitic
    dt = timedelta(seconds=math.floor(request_chunk_size*scan_rate))
    return split_range(start_time, end_time, dt)


def split_range(
    start_time: datetime,
    end_time: datetime,
    dt: timedelta
) -> Tuple[List[datetime], List[datetime]]:
    """Split a time range into smaller ranges"""
    start_times = []
    end_times = []
    
    while start_time < end_time:
        start_times.append(start_time)
        next_timestamp = start_time + dt
        
        if next_timestamp >= end_time:
            start_time = end_time
        
        else:
            start_time = next_timestamp
        end_times.append(start_time)
    
    return start_times, end_times


async def get_interpolated(
    client: PIClient,
    web_ids: Union[str, Sequence[str]],
    start_time: datetime,
    end_time: datetime,
    interval: Union[timedelta, int] = 60,
    request_chunk_size: int = 5000,
    timezone: str = TIMEZONE
) -> AsyncIterable[List[JSONPrimitive], None]:
    """Stream timestamp aligned, interpolated data for a sequence of PI tags
    
    This iterable streams batch data for a sequence of PI tags row by row. The
    first row is the "headers" row specifying the columns for each subsequent
    row returned. Subsequent rows are unlabeled but the indices of the elements
    align with the indices of header row.

    Args:
        web_ids: The web_ids to stream data for
        start_time: The start time of the batch. This will be the timestamp
            in the first row of data
        end_time: The end time of the batch. This will be the timestamp in the
            last row
        interval: The time interval (in seconds) between successive rows
        request_chunk_size: The maximum number of rows to be

    Yields:
        List[JSONPrimitive]: The data for the row. The first row is always the
            index row
    """
    web_ids = [web_ids] if isinstance(web_ids, str) else sorted(set(web_ids))
    start_time = pendulum.instance(start_time, tz=timezone).in_timezone("UTC").replace(tzinfo=None)
    end_time = pendulum.instance(end_time, tz=timezone).in_timezone("UTC").replace(tzinfo=None)
    interval = timedelta(seconds=interval) if isinstance(interval, int) else interval
    
    if not isinstance(interval, timedelta):
        raise ValueError(f"Interval must be timedelta or int. Got {type(interval)}")
    str_interval = f"{interval.total_seconds()} seconds"
    start_times, end_times = split_interpolated_range(start_time, end_time, interval, request_chunk_size)
    
    # The first row is an identifier row. The index of each element in
    # subsequent rows will correspond to the id at the index in this row.
    # The first element is always the timestamp. This significantly reduces
    # the amount of data sent over the wire
    yield ["timestamp", *web_ids]
    
    for start_time, end_time in zip(start_times, end_times):
        dispatch = [
            handle_request(
                client.streams.get_interpolated(
                    web_id,
                    startTime=start_time,
                    endTime=end_time,
                    timeZone="UTC",
                    interval=str_interval,
                    selectedFields="Items.Timestamp;Items.Value;Items.Good"
                ),
                raise_for_status=False
            ) for web_id in web_ids
        ]
        
        contents = await asyncio.gather(*dispatch)
        data = [format_streams_content(content) for content in contents]
        index = get_timestamp_index(data)
        
        for row in iter_rows(index, data):
            yield row


async def get_recorded(
    client: PIClient,
    web_ids: Union[str, Sequence[str]],
    start_time: datetime,
    end_time: datetime,
    request_chunk_size: int = 5000,
    scan_rate: float = 5.0
) -> AsyncIterable[List[JSONPrimitive]]:
    """Stream timestamp aligned, recorded data for a sequence of PI tags
    
    This generator streams batch data for a sequence of PI tags row by row. The
    first row is the "headers" row specifying the columns for each subsequent
    row returned. Subsequent rows are unlabeled but the indices of the elements
    align with the indices of header row.

    Args:
        web_ids: The web_ids to stream data for
        start_time: The start time of the batch. This will be the timestamp
            in the first row of data
        end_time: The end time of the batch. This will be the timestamp in the
            last row
        interval: The time interval (in seconds) between successive rows
        request_chunk_size: The maximum number of rows to be

    Yields:
        List[JSONPrimitive]: The data for the row. The first row is always the
            index row
    """
    web_ids = [web_ids] if isinstance(web_ids, str) else sorted(set(web_ids))
    start_time = pendulum.instance(start_time, tz=TIMEZONE).in_timezone("UTC").replace(tzinfo=None)
    end_time = pendulum.instance(end_time, tz=TIMEZONE).in_timezone("UTC").replace(tzinfo=None)
    start_times, end_times = split_recorded_range(start_time, end_time, request_chunk_size, scan_rate)
    
    # The first row is an identifier row. The index of each element in
    # subsequent rows will correspond to the id at the index in this row.
    # The first element is always the timestamp. This significantly reduces
    # the amount of data sent over the wire
    yield ["timestamp", *web_ids]
    
    for start_time, end_time in zip(start_times, end_times):
        dispatch = [
            handle_request(
                client.streams.get_recorded(
                    web_id,
                    startTime=start_time,
                    endTime=end_time,
                    timeZone="UTC",
                    selectedFields="Items.Timestamp;Items.Value;Items.Good"
                ),
                raise_for_status=False
            ) for web_id in web_ids
        ]
        
        contents = await asyncio.gather(*dispatch)
        data = [format_streams_content(content) for content in contents]
        index = get_timestamp_index(data)
        
        for row in iter_rows(index, data):
            yield row