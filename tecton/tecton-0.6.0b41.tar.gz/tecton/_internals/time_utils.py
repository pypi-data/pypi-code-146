import pendulum

from tecton_core import time_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition


"""
This file contains a utility used for adjusting time based on
feature view configurations.
"""


def get_feature_data_time_limits(
    fd: FeatureDefinition,
    spine_time_limits: pendulum.Period,
) -> pendulum.Period:
    """Returns the feature data time limits based on the spine time limits, taking aggregations into account.

    To get the raw data time limits, you need to use additional information that is on your FilteredSource or other data source inputs.

    Args:
        fd: The feature view for which to compute feature data time limits.
        spine_time_limits: The time limits of the spine; the start time is inclusive and the end time is exclusive.
    """

    if fd.is_feature_table:
        return _feature_table_get_feature_data_time_limits(fd, spine_time_limits)
    elif fd.is_temporal:
        return _temporal_fv_get_feature_data_time_limits(fd, spine_time_limits)
    elif fd.is_temporal_aggregate:
        return _temporal_agg_fv_get_feature_data_time_limits(fd, spine_time_limits)

    # Should never happen!
    raise Exception("Feature definition must be a feature table, temporal FV, or temporal agg FV")


def _feature_table_get_feature_data_time_limits(
    fd: FeatureDefinition,
    spine_time_limits: pendulum.Period,
) -> pendulum.Period:
    """Feature data time limits for a feature table.

    This is `[spine_start_time - ttl, spine_end_time)`
    """

    start_time = spine_time_limits.start
    end_time = spine_time_limits.end

    # Subtract by `serving_ttl` to accommodate for enough feature data for the feature expiration
    if fd.serving_ttl:
        start_time = start_time - fd.serving_ttl

    return end_time - start_time


def _align_left(timestamp: pendulum.DateTime, min_scheduling_interval: pendulum.Duration) -> pendulum.DateTime:
    # min scheduling interval may be zero for continuous
    if min_scheduling_interval.total_seconds() > 0:
        timestamp = time_utils.align_time_downwards(timestamp, min_scheduling_interval)
    return pendulum.instance(timestamp)


def _align_right(timestamp: pendulum.DateTime, min_scheduling_interval: pendulum.Duration) -> pendulum.DateTime:
    """Aligns timestamp to the end of the scheduling interval. If it's already aligned,
    adds scheduling interval's length.

    This function does not take allowed lateness into account.

    :param timestamp: The timestamp in python datetime format
    :return: The timestamp of the greatest aligned time <= timestamp, in seconds.
    """
    aligned_left = _align_left(timestamp, min_scheduling_interval)
    return aligned_left + min_scheduling_interval


def _temporal_fv_get_feature_data_time_limits(
    fd: FeatureDefinition,
    spine_time_limits: pendulum.Period,
) -> pendulum.Period:
    """Feature data time limits for a non aggregate feature view.

    Accounts for:
      * serving ttl
      * batch schedule

    Does NOT account for:
      * data delay
      * batch vs streaming
    """

    start_time = spine_time_limits.start
    end_time = spine_time_limits.end

    # Subtract by `serving_ttl` to accommodate for enough feature data for the feature expiration
    if fd.serving_ttl:
        start_time = start_time - fd.serving_ttl

    # Respect feature_start_time if it's set.
    if fd.feature_start_timestamp:
        start_time = max(start_time, fd.feature_start_timestamp)

    start_time = _align_left(start_time, fd.min_scheduling_interval)

    # Since feature data time interval is open on the right, we need to always strictly align right so that
    # with `batch_schedule = 1h`, time end `04:00:00` will be aligned to `05:00:00`.
    # NOTE: This may be more permissive than 'allowed_upstream_lateness' would allow,
    # but that's okay from a correctness perspective since our as-of join
    # should account for this.
    end_time = _align_right(end_time, fd.min_scheduling_interval)

    # It is possible for the start time to be greater than the end time, for example if the feature start time is later
    # than the spine end time. If this happens, we simply set the start time to equal the end time.
    if start_time > end_time:
        start_time = end_time
    return pendulum.Period(start_time, end_time)


def _temporal_agg_fv_get_feature_data_time_limits(
    fd: FeatureDefinition,
    spine_time_limits: pendulum.Period,
) -> pendulum.Period:
    """Feature data time limits for an aggregate feature view.

    Accounts for:
      * aggregation tile interval
      * data delay

    Does NOT account for:
      * batch vs streaming
    """

    start_time = spine_time_limits.start
    end_time = spine_time_limits.end

    # Respect feature_start_time if it's set.
    if fd.feature_start_timestamp:
        start_time = max(start_time, fd.feature_start_timestamp)

    start_time = _align_left(start_time - fd.allowed_upstream_lateness, fd.min_scheduling_interval)

    # Account for final aggregation needing aggregation window prior to earliest timestamp
    start_time = start_time - time_utils.proto_to_duration(fd.max_aggregation_window)

    # Since feature data time interval is open on the right, we need to always strictly align right so that
    # with `batch_schedule = 1h`, time end `04:00:00` will be aligned to `05:00:00`.
    # NOTE: This may be more permissive than 'allowed_upstream_lateness' would allow,
    # but that's okay from a correctness perspective since our as-of join
    # should account for this.
    end_time = _align_right(end_time, fd.min_scheduling_interval)

    # It is possible for the start time to be greater than the end time, for example if the feature start time is later
    # than the spine end time. If this happens, we simply set the start time to equal the end time.
    if start_time > end_time:
        start_time = end_time
    return pendulum.Period(start_time, end_time)
