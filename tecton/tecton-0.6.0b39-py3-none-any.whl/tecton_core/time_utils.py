import datetime
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pendulum
import pytimeparse
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2
from typeguard import typechecked

from tecton_core.errors import TectonValidationError
from tecton_proto.data import feature_store_pb2


def timedelta_to_duration(td: datetime.timedelta) -> pendulum.Duration:
    return pendulum.duration(days=td.days, seconds=td.seconds, microseconds=td.microseconds)


def proto_to_duration(proto_duration: duration_pb2.Duration) -> pendulum.Duration:
    return timedelta_to_duration(proto_duration.ToTimedelta())


def timedelta_to_proto(td: Optional[datetime.timedelta]) -> Optional[duration_pb2.Duration]:
    if td is None:
        return None

    proto = duration_pb2.Duration()
    proto.FromTimedelta(td)
    return proto


def datetime_to_proto(dt: Optional[datetime.datetime]) -> Optional[timestamp_pb2.Timestamp]:
    if dt is None:
        return None

    proto = timestamp_pb2.Timestamp()
    proto.FromDatetime(dt)
    return proto


@typechecked
def to_human_readable_str(duration: Union[duration_pb2.Duration, datetime.timedelta]) -> str:
    """
    Replicate the backend logic that converts durations to feature strings, e.g. `column_sum_1h30m_30m`.

    Backend logic: https://github.com/tecton-ai/tecton/blob/e3c04e28066c21fa4ed9b459ece458c084766b6e/java/com/tecton/common/utils/TimeUtils.kt#L80
    """

    if isinstance(duration, duration_pb2.Duration):
        duration = proto_to_duration(duration)
    elif isinstance(duration, datetime.timedelta):
        duration = timedelta_to_duration(duration)
    else:
        raise TypeError(f"Invalid input duration type: {type(duration)}")

    duration_str_list = []
    if duration.days > 0:
        duration_str_list.append(f"{duration.days}d")
    if duration.hours > 0:
        duration_str_list.append(f"{duration.hours}h")
    if duration.minutes > 0:
        duration_str_list.append(f"{duration.minutes}m")
    if duration.remaining_seconds > 0:
        duration_str_list.append(f"{duration.remaining_seconds}s")

    return "0s" if len(duration_str_list) == 0 else "".join(duration_str_list)


def assert_is_round_seconds(d: pendulum.Duration) -> pendulum.Duration:
    if d % pendulum.Duration(seconds=1):
        raise ValueError(f"{d.in_words()} is not a round number of seconds")
    return d


def strict_pytimeparse(time_str: str) -> Union[int, float]:
    parsed = pytimeparse.parse(time_str)
    if parsed is None:
        raise TectonValidationError(f'Could not parse time string "{time_str}"')
    else:
        return parsed


def nanos_to_seconds(nanos: int) -> float:
    """
    :param nanos: Nanoseconds
    :return: Converts nanoseconds to seconds
    """
    return nanos / float(1e9)


def seconds_to_nanos(seconds: float) -> int:
    """
    :param seconds: Seconds
    :return: Converts seconds to nanoseconds
    """
    return int(seconds * 1e9)


def convert_duration_to_seconds(duration: int, version: int) -> int:
    """Convert a duration to seconds according to the version.

    If V0, the duration is already in seconds; if V1, the duration must be converted from nanos to seconds.
    """
    if version == feature_store_pb2.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return duration
    else:
        return int(nanos_to_seconds(duration))


def convert_timedelta_for_version(duration: datetime.timedelta, version: int) -> int:
    """
    Convert pendulum duration according to version
    VO -> Return Seconds
    V1 -> Return Nanoseconds
    :param duration: Pendulum Duration
    :param version: Feature Store Format Version
    :return:
    """
    assert duration.microseconds == 0
    interval = duration.total_seconds()
    if version == feature_store_pb2.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return int(interval)
    else:
        return seconds_to_nanos(interval)


def convert_epoch_to_datetime(epoch: int, version: int) -> pendulum.datetime:
    """
    Converts an epoch to a datetime.
    """
    if version == feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return pendulum.from_timestamp(epoch)
    else:
        return pendulum.from_timestamp(epoch / 1e9)


def convert_timestamp_for_version(timestamp: datetime.datetime, version: int) -> int:
    if version == feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return int(timestamp.timestamp())
    else:
        return seconds_to_nanos(timestamp.timestamp())


def convert_proto_duration_for_version(duration: duration_pb2.Duration, version: int) -> int:
    return convert_timedelta_for_version(duration.ToTimedelta(), version)


def align_time_downwards(time: datetime.datetime, alignment: datetime.timedelta) -> datetime.datetime:
    excess_seconds = time.timestamp() % alignment.total_seconds()
    return datetime.datetime.utcfromtimestamp(time.timestamp() - excess_seconds)


def align_epoch_downwards(int_timestamp_col: int, window_size: int) -> int:
    return int_timestamp_col - (int_timestamp_col % window_size)


def align_time_upwards(time: datetime.datetime, alignment: datetime.timedelta) -> datetime.datetime:
    excess_seconds = time.timestamp() % alignment.total_seconds()
    offset = 0 if excess_seconds == 0 else alignment.total_seconds() - excess_seconds
    return datetime.datetime.utcfromtimestamp(time.timestamp() + offset)


def get_timezone_aware_datetime(time: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
    """
    Check and get timezone aware datetime
    :param time: Time to convert to timezone aware
    """
    if time is None:
        return None
    if time.tzinfo is None:
        return time.replace(tzinfo=pendulum.timezone("UTC"))
    else:
        return time


def backfill_jobs_periods(
    start_time: datetime.datetime, end_time: datetime.datetime, interval: datetime.timedelta
) -> List[Tuple[datetime.datetime, datetime.datetime]]:
    """
    Return a list of start/end tuples of size batch_schedule.
    For use of breaking up a large backfill window into incremental sizes.
    """
    jobs = []
    while start_time < end_time:
        jobs.append((start_time, start_time + interval))
        start_time = start_time + interval
    assert start_time == end_time, "Start and end times were not aligned to `interval`"
    return jobs
